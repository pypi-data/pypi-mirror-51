import numpy as np
import scipy.ndimage as ndimage
import matplotlib.pyplot as plt
from matplotlib import patches
from shapely import geometry
import PIL
from PIL import ImageDraw
import math
import scipy.stats as stats
# from matplotlib.colors import NoNorm
import matplotlib.cm as cm
import networkx as nx
from cicada.utils.graph_utils import welsh_powell
from cicada.utils.display.colors import BREWER_COLORS
import matplotlib.colors as plt_colors


class CellsCoord:
    # TODO: adapt it to the ROIs in NWBfile
    def __init__(self, coord, nb_lines=None, nb_col=None,
                 from_suite_2p=False, from_fiji=False):
        """

        Args:
            coord:
            nb_lines: If None, set it using the max coordinate in coord
            nb_col:If None, set it using the max coordinate in coord
            from_suite_2p:
            from_fiji:
        """
        # contour coord
        self.coord = coord

        if (nb_lines is None) or (nb_col is None):
            self.nb_lines = 0
            self.nb_col = 0
            padding = 2
            for cell, c in enumerate(self.coord):

                if (not from_suite_2p) and (not from_fiji):
                    # it is necessary to remove one, as data comes from matlab, starting from 1 and not 0
                    c = c - 1
                c = c.astype(int)
                #
                # if c.shape[0] == 0:
                #     print(f'Error: {cell} c.shape {c.shape}')
                #     continue

                c_filtered = c.astype(int)

                self.nb_col = max(self.nb_col, np.max(c_filtered[0, :]) + padding)
                self.nb_lines = max(self.nb_lines, np.max(c_filtered[1, :]) + padding)
        else:
            self.nb_lines = nb_lines
            self.nb_col = nb_col

        self.n_cells = len(self.coord)
        # dict of tuples, key is the cell #, cell center coord x and y (x and y are inverted for imgshow)
        self.center_coord = dict()
        self.img_filled = None
        self.img_contours = None
        # used in case some cells would be removed, to we can update the centers accordingly
        self.neurons_removed = []
        # compute_center_coord() will be called when a mouseSession will be created
        # self.compute_center_coord()
        self.cells_groups = None
        self.cells_groups_colors = None
        # shapely polygons
        self.cells_polygon = dict()
        # first key is an int representing the number of the cell, and value is a list of cells it interesects
        self.intersect_cells = dict()

        for cell, c in enumerate(self.coord):

            if (not from_suite_2p) and (not from_fiji):
                # it is necessary to remove one, as data comes from matlab, starting from 1 and not 0
                c = c - 1
            c = c.astype(int)
            self.coord[cell] = c

            if c.shape[0] == 0:
                print(f'Error: {cell} c.shape {c.shape}')
                continue

            c_filtered = c.astype(int)
            bw = np.zeros((self.nb_col, self.nb_lines), dtype="int8")
            # morphology.binary_fill_holes(input
            bw[c_filtered[0, :], c_filtered[1, :]] = 1

            n_coord = len(c_filtered[0, :])
            coord_list_tuple = []
            for n in np.arange(n_coord):
                coord_list_tuple.append((c_filtered[0, n], c_filtered[1, n]))

            # buffer(0) or convex_hull could be used if the coord are a list of points not
            # in the right order. However buffer(0) return a MultiPolygon with no coord available.
            if len(coord_list_tuple) < 3:
                list_points = []
                for coord in coord_list_tuple:
                    list_points.append(geometry.Point(coord))
                self.cells_polygon[cell] = geometry.LineString(list_points)
                # print(f"len(coord_list_tuple) {len(coord_list_tuple)}")
            else:
                self.cells_polygon[cell] = geometry.Polygon(coord_list_tuple)  # .convex_hull # buffer(0)
            # self.coord[cell] = np.array(self.cells_polygon[cell].exterior.coords).transpose()

            c_x, c_y = ndimage.center_of_mass(bw)
            self.center_coord[cell] = (c_x, c_y)

            # if (cell == 0) or (cell == 159):
            #     print(f"cell {cell} fig")
            #     fig, ax = plt.subplots(nrows=1, ncols=1,
            #                            gridspec_kw={'height_ratios': [1]},
            #                            figsize=(5, 5))
            #     ax.imshow(bw)
            #     plt.show()
            #     plt.close()

        for cell_1 in np.arange(self.n_cells-1):
            if cell_1 not in self.intersect_cells:
                if cell_1 not in self.cells_polygon:
                    continue
                self.intersect_cells[cell_1] = set()
            for cell_2 in np.arange(cell_1+1, self.n_cells):
                if cell_2 not in self.cells_polygon:
                    continue
                if cell_2 not in self.intersect_cells:
                    self.intersect_cells[cell_2] = set()
                poly_1 = self.cells_polygon[cell_1]
                poly_2 = self.cells_polygon[cell_2]
                # if it intersects and not only touches if adding and (not poly_1.touches(poly_2))
                # try:
                if poly_1.intersects(poly_2):
                    self.intersect_cells[cell_2].add(cell_1)
                    self.intersect_cells[cell_1].add(cell_2)
                # except shapely.errors.TopologicalError:
                #     print(f"cell_1 {cell_1}, cell_2 {cell_2}")
                #     print(f"cell_1 {poly_1.is_valid}, cell_2 {poly_2.is_valid}")
                #     poly_1 = poly_1.buffer(0)
                #     poly_2 = poly_2.buffer(0)
                #     print(f"cell_1 {poly_1.is_valid}, cell_2 {poly_2.is_valid}")
                #     raise Exception("shapely.errors.TopologicalError")

    def get_cell_mask(self, cell, dimensions):
        """
        :param cell:
        :param dimensions: height x width
        :return:
        """
        poly_gon = self.cells_polygon[cell]
        img = PIL.Image.new('1', (dimensions[1], dimensions[0]), 0)
        if isinstance(poly_gon, geometry.LineString):
            ImageDraw.Draw(img).polygon(list(poly_gon.coords), outline=1,
                                        fill=1)
        else:
            ImageDraw.Draw(img).polygon(list(poly_gon.exterior.coords), outline=1,
                                    fill=1)
        return np.array(img)

    def match_cells_indices(self, coord_obj, path_results, plot_title_opt=""):
        """

        :param coord_obj: another instanc of coord_obj
        :return: a 1d array, each index corresponds to the index of a cell of coord_obj, and map it to an index to self
        or -1 if no cell match
        """
        mapping_array = np.zeros(len(coord_obj.coord), dtype='int16')
        for cell in np.arange(len(coord_obj.coord)):
            c_x, c_y = coord_obj.center_coord[cell]
            distances = np.zeros(len(self.coord))
            for self_cell in np.arange(len(self.coord)):
                self_c_x, self_c_y = self.center_coord[self_cell]
                # then we calculte the cartesian distance to all other cells
                distances[self_cell] = math.sqrt((self_c_x - c_x) ** 2 + (self_c_y - c_y) ** 2)
            if np.min(distances) <= 2:
                mapping_array[cell] = np.argmin(distances)
            else:
                mapping_array[cell] = -1
        plot_result = True
        if plot_result:
            fig, ax = plt.subplots(nrows=1, ncols=1,
                                   gridspec_kw={'height_ratios': [1]},
                                   figsize=(20, 20))

            fig.patch.set_facecolor("black")
            ax.set_facecolor("black")

            # dark blue
            other_twin_color = list((0.003, 0.313, 0.678, 1.0))
            n_twins = 0
            # red
            other_orphan_color = list((1, 0, 0, 1.0))
            n_other_orphans = 0
            # light blue
            self_twin_color = list((0.560, 0.764, 1, 1.0))
            # green
            self_orphan_color = list((0.278, 1, 0.101, 1.0))
            n_self_orphans = 0
            with_edge = True
            edge_line_width = 1
            z_order_cells = 12
            for cell in np.arange(len(coord_obj.coord)):
                xy = coord_obj.coord[cell].transpose()
                if with_edge:
                    line_width = edge_line_width
                    edge_color = "white"
                else:
                    edge_color = "white"
                    line_width = 0
                # allow to set alpha of the edge to 1
                if mapping_array[cell] >= 0:
                    # dark blue
                    face_color = other_twin_color
                    n_twins += 1
                else:
                    # red
                    face_color = other_orphan_color
                    n_other_orphans += 1
                face_color[3] = 0.8
                face_color = tuple(face_color)
                cell_contour = patches.Polygon(xy=xy,
                                                    fill=True, linewidth=line_width,
                                                    facecolor=face_color,
                                                    edgecolor=edge_color,
                                                    zorder=z_order_cells)  # lw=2
                ax.add_patch(cell_contour)
            for cell in np.arange(len(self.coord)):
                xy = self.coord[cell].transpose()
                if with_edge:
                    line_width = edge_line_width
                    edge_color = "white"
                else:
                    edge_color = "white"
                    line_width = 0
                # allow to set alpha of the edge to 1
                if cell in mapping_array:
                    # light blue
                    face_color = self_twin_color
                else:
                    # green
                    face_color = self_orphan_color
                    n_self_orphans += 1
                face_color[3] = 0.8
                face_color = tuple(face_color)
                # drawing the cell
                cell_contour = patches.Polygon(xy=xy,
                                               fill=True, linewidth=line_width,
                                               facecolor=face_color,
                                               edgecolor=edge_color,
                                               zorder=z_order_cells)  # lw=2
                ax.add_patch(cell_contour)
                with_cell_numbers = True
                if with_cell_numbers:
                    self.plot_text_cell(cell=cell, cell_numbers_color="black", ax=ax, text_size=6)
            fontsize = 12
            plt.text(x=190, y=180,
                     s=f"{n_twins}", color=self_twin_color, zorder=22,
                     ha='center', va="center", fontsize=fontsize, fontweight='bold')
            plt.text(x=190, y=185,
                     s=f"{n_self_orphans}", color=self_orphan_color, zorder=22,
                     ha='center', va="center", fontsize=fontsize, fontweight='bold')
            plt.text(x=190, y=190,
                     s=f"{n_twins}", color=other_twin_color, zorder=22,
                     ha='center', va="center", fontsize=fontsize, fontweight='bold')
            plt.text(x=190, y=195,
                     s=f"{n_other_orphans}", color=other_orphan_color, zorder=22,
                     ha='center', va="center", fontsize=fontsize, fontweight='bold')
            ax.set_ylim(0, self.nb_lines)
            ax.set_xlim(0, self.nb_col)
            ylim = ax.get_ylim()
            # invert Y
            ax.set_ylim(ylim[::-1])
            plt.setp(ax.spines.values(), color="black")
            frame = plt.gca()
            frame.axes.get_xaxis().set_visible(False)
            frame.axes.get_yaxis().set_visible(False)
            save_format = "png"
            fig.savefig(f'{path_results}/cells_map_{plot_title_opt}.{save_format}',
                        format=f"{save_format}",
                            facecolor=fig.get_facecolor())
            plt.close()
        return mapping_array

    def plot_cells_map(self, path_results, data_id, title_option="", connections_dict=None,
                       background_color=(0, 0, 0, 1), default_cells_color=(1, 1, 1, 1.0),
                       default_edge_color="white",
                       dont_fill_cells_not_in_groups=False,
                       link_connect_color="white", link_line_width=1,
                       cell_numbers_color="dimgray", show_polygons=False,
                       cells_to_link=None, edge_line_width=2, cells_alpha=1.0,
                       fill_polygons=True, cells_groups=None, cells_groups_colors=None,
                       cells_groups_alpha=None,
                       cells_to_hide=None, img_on_background=None,
                       cells_groups_edge_colors=None, with_edge=False,
                       with_cell_numbers=False, text_size=6, save_formats="png",
                       save_plot=True, return_fig=False, ax_to_use=None,
                       use_welsh_powell_coloring=False):
        """

        :param connections_dict: key is an int representing a cell number, and value is a dict representing the cells it
        connects to. The key is a cell is connected too, and the value represent the strength of the connection (like how
        many
        times it connects to it)
        :param plot_option: if 0: plot n_out and n_int, if 1 only n_out, if 2 only n_in, if 3: only n_out with dotted to
        show the commun n_in and n_out, if 4: only n_in with dotted to show the commun n_in and n_out,
        :param use_welsh_powell_coloring: if True, use welsh powell algorithm to color all cells that intersect with
        different color. In that case, cancel cell_groups arguments.
        :return:
        """

        cells_center = self.center_coord
        n_cells = len(self.coord)
        if cells_to_hide is None:
            cells_to_hide = []

        if use_welsh_powell_coloring:
            isolated_cell_color = default_cells_color
            isolated_group = []
            cells_groups_colors = []
            cells_groups_edge_colors = []
            cells_groups_alpha = []
            cells_groups = []

            # building networkx graph
            graphs = []
            cells_added = []
            for cell in np.arange(n_cells):
                if cell in cells_added:
                    continue
                # welsh_powell
                n_intersect = len(self.intersect_cells[cell])
                if n_intersect == 0:
                    isolated_group.append(cell)
                    cells_added.append(cell)
                else:
                    graph = nx.Graph()
                    cells_to_expend = [cell]
                    edges = set()
                    while len(cells_to_expend) > 0:
                        if cells_to_expend[0] not in cells_added:
                            cells_added.append(cells_to_expend[0])
                            n_intersect = len(self.intersect_cells[cells_to_expend[0]])
                            if n_intersect > 0:
                                for inter_cell in self.intersect_cells[cells_to_expend[0]]:
                                    min_c = min(inter_cell, cells_to_expend[0])
                                    max_c = max(inter_cell, cells_to_expend[0])
                                    edges.add((min_c, max_c))
                                    cells_to_expend.append(inter_cell)
                        cells_to_expend = cells_to_expend[1:]
                    graph.add_edges_from(list(edges))
                    graphs.append(graph)
            cells_by_color_code = dict()
            max_color_code = 0
            for graph in graphs:
                # dict that give for each cell a color code
                col_val = welsh_powell(graph)
                for cell, color_code in col_val.items():
                    if color_code not in cells_by_color_code:
                        cells_by_color_code[color_code] = []
                    cells_by_color_code[color_code].append(cell)
                    max_color_code = max(max_color_code, color_code)

            for color_code, cells in cells_by_color_code.items():
                if len(cells) == 0:
                    continue
                cells_groups.append(cells)
                # cells_groups_colors.append(cm.nipy_spectral(float(color_code + 1) / (max_color_code + 1)))
                color_hex = BREWER_COLORS[color_code % len(BREWER_COLORS)]
                # putting it with value from 0.0 to 1.0
                color_rgb = plt_colors.hex2color(color_hex)
                # adding the alpha
                color_rgba = [c for c in color_rgb]
                color_rgba.append(cells_alpha)
                cells_groups_colors.append(color_rgba)
                cells_groups_edge_colors.append(default_edge_color)
                cells_groups_alpha.append(0.8)
            cells_groups.append(isolated_group)
            cells_groups_colors.append(isolated_cell_color)
            cells_groups_alpha.append(1)
            cells_groups_edge_colors.append("white")

        cells_in_groups = []
        if cells_groups is not None:
            for group_id, cells_group in enumerate(cells_groups):
                cells_in_groups.extend(cells_group)
        cells_in_groups = np.array(cells_in_groups)
        cells_not_in_groups = np.setdiff1d(np.arange(n_cells), cells_in_groups)

        if ax_to_use is None:
            fig, ax = plt.subplots(nrows=1, ncols=1,
                                   gridspec_kw={'height_ratios': [1]},
                                   figsize=(20, 20))

            fig.patch.set_facecolor(background_color)
            ax.set_facecolor(background_color)
        else:
            ax = ax_to_use

        if img_on_background is not None:
            print(f"np.mean(img_on_background) {np.mean(img_on_background)}")
            n_bits = 8
            ax.imshow(img_on_background, cmap=plt.get_cmap("gray"), vmin=0,
                      vmax=math.pow(2, n_bits)-1)

        # blue = "cornflowerblue"
        # cmap.set_over('red')
        z_order_cells = 12
        if cells_groups is not None:
            for group_index, cell_group in enumerate(cells_groups):
                for cell in cell_group:
                    if cell in cells_to_hide:
                        continue

                    xy = self.coord[cell].transpose()
                    if with_edge:
                        line_width = edge_line_width
                        if cells_groups_edge_colors is None:
                            edge_color = default_edge_color
                        else:
                            edge_color = cells_groups_edge_colors[group_index]
                    else:
                        edge_color = cells_groups_colors[group_index]
                        line_width = 0
                    # allow to set alpha of the edge to 1
                    face_color = list(cells_groups_colors[group_index])
                    # changing alpha
                    if cells_groups_alpha is not None:
                        face_color[3] = cells_groups_alpha[group_index]
                    else:
                        face_color[3] = cells_alpha
                    face_color = tuple(face_color)
                    # TODO: a solution to explore to plot pixel by pixel and not using the polygon version
                    #  https://stackoverflow.com/questions/39753282/scatter-plot-with-single-pixel-marker-in-matplotlib
                    self.cell_contour = patches.Polygon(xy=xy,
                                                        fill=True, linewidth=line_width,
                                                        facecolor=face_color,
                                                        edgecolor=edge_color,
                                                        zorder=z_order_cells) # lw=2
                    ax.add_patch(self.cell_contour)
                    if with_cell_numbers:
                        self.plot_text_cell(cell=cell, cell_numbers_color=cell_numbers_color, ax=ax,
                                            text_size=text_size)

        for cell in cells_not_in_groups:
            if cell in cells_to_hide:
                continue
            xy = self.coord[cell].transpose()
            # face_color = default_cells_color
            # if dont_fill_cells_not_in_groups:
            #     face_color = None
            self.cell_contour = patches.Polygon(xy=xy,
                                                fill=not dont_fill_cells_not_in_groups,
                                                linewidth=0, facecolor=default_cells_color,
                                                edgecolor=default_edge_color,
                                                zorder=z_order_cells, lw=edge_line_width)
            ax.add_patch(self.cell_contour)

            if with_cell_numbers:
                self.plot_text_cell(cell=cell, cell_numbers_color=cell_numbers_color, ax=ax,
                                    text_size=text_size)

        ax.set_ylim(0, self.nb_lines)
        ax.set_xlim(0, self.nb_col)
        ylim = ax.get_ylim()
        # invert Y
        ax.set_ylim(ylim[::-1])

        if (connections_dict is not None) :
            zorder_lines = 15
            for neuron in connections_dict.keys():
                # plot a line to all out of the neuron
                for connected_neuron, nb_connexion in connections_dict[neuron].items():
                    line_width = link_line_width + np.log(nb_connexion)

                    c_x = cells_center[neuron][0]
                    c_y = cells_center[neuron][1]
                    c_x_c = cells_center[connected_neuron][0]
                    c_y_c = cells_center[connected_neuron][1]

                    line = plt.plot((c_x, c_x_c), (c_y, c_y_c), linewidth=line_width, c=link_connect_color,
                                    zorder=zorder_lines)[0]
        # print(f"(self.cells_groups is not None) {(self.cells_groups is not None)} show_polygons {show_polygons}")
        if (cells_groups is not None) and show_polygons:
            for group_id, cells in enumerate(cells_groups):
                points = np.zeros((2, len(cells)))
                for cell_id, cell in enumerate(cells):
                    c_x, c_y = cells_center[cell]
                    points[0, cell_id] = c_x
                    points[1, cell_id] = c_y
                # finding the convex_hull for each group
                xy = convex_hull(points=points)
                # xy = xy.transpose()
                # print(f"xy {xy}")
                # xy is a numpy array with as many line as polygon point
                # and 2 columns: x and y coord of each point
                face_color = list(cells_groups_colors[group_id])
                # changing alpha
                face_color[3] = 0.3
                face_color = tuple(face_color)
                # edge alpha will be 1
                poly_gon = patches.Polygon(xy=xy,
                                           fill=fill_polygons, linewidth=0, facecolor=face_color,
                                           edgecolor=cells_groups_colors[group_id],
                                           zorder=15, lw=3)
                ax.add_patch(poly_gon)

        # plt.title(f"Cells map {data_id} {title_option}")

        # ax.set_frame_on(False)

        # invert Y
        ax.set_ylim(ylim[::-1])
        plt.setp(ax.spines.values(), color=background_color)
        frame = plt.gca()
        frame.axes.get_xaxis().set_visible(False)
        frame.axes.get_yaxis().set_visible(False)

        plt.tight_layout()
        # ax.xaxis.set_ticks_position('none')
        # ax.yaxis.set_ticks_position('none')
        #  :param plot_option: if 0: plot n_out and n_int, if 1 only n_out, if 2 only n_in, if 3: only n_out with dotted to
        # show the commun n_in and n_out, if 4: only n_in with dotted to show the commun n_in and n_out,
        if ax_to_use is None:
            if save_plot:
                if isinstance(save_formats, str):
                    save_formats = [save_formats]
                for save_format in save_formats:
                    fig.savefig(f'{path_results}/{data_id}_cell_maps_{title_option}.{save_format}',
                                format=f"{save_format}",
                                facecolor=fig.get_facecolor())
            if return_fig:
                return fig
            else:
                plt.close()

    def plot_text_cell(self, cell, ax, cell_numbers_color, text_size):
        """
        Plot the cell number on the cell
        Args:
            cell: integer
            ax: matplolib axis
            cell_numbers_color: color of the text
            text_size: text size (int)

        Returns:

        """
        fontsize = text_size
        if cell >= 100:
            fontsize -= 2
            fontsize = max(0.5, fontsize)
        elif cell >= 10:
            fontsize -= 1
            fontsize = max(1, fontsize)

        c_x_c = self.center_coord[cell][0]
        c_y_c = self.center_coord[cell][1]

        ax.text(x=c_x_c, y=c_y_c,
                 s=f"{cell}", color=cell_numbers_color, zorder=22,
                 ha='center', va="center", fontsize=fontsize, fontweight='bold')

    def get_cell_new_coord_in_source(self, cell, minx, miny):
        coord = self.coord[cell]
        # coord = coord - 1
        coord = coord.astype(int)
        n_coord = len(coord[0, :])
        xy = np.zeros((n_coord, 2))
        for n in np.arange(n_coord):
            # shifting the coordinates in the square size_square+1
            xy[n, 0] = coord[0, n] - minx
            xy[n, 1] = coord[1, n] - miny
        return xy

    def scale_polygon_to_source(self, poly_gon, minx, miny):
        coords = list(poly_gon.exterior.coords)
        scaled_coords = []
        for coord in coords:
            scaled_coords.append((coord[0] - minx, coord[1] - miny))
        # print(f"scaled_coords {scaled_coords}")
        return geometry.Polygon(scaled_coords)


    def get_source_profile(self, cell, tiff_movie, traces, peak_nums, spike_nums,
                           pixels_around=0, bounds=None, buffer=None, with_full_frame=False):
        """
        Return the source profile of a cell
        :param cell:
        :param pixels_around:
        :param bounds: how much padding around the cell pretty much, coordinate of the frame covering the source profile
        4 int list
        :param buffer:
        :param with_full_frame:  Average the full frame
        :return:
        """
        # print("get_source_profile")
        len_frame_x = tiff_movie[0].shape[1]
        len_frame_y = tiff_movie[0].shape[0]

        # determining the size of the square surrounding the cell
        poly_gon = self.cells_polygon[cell]
        if bounds is None:
            minx, miny, maxx, maxy = np.array(list(poly_gon.bounds)).astype(int)
        else:
            minx, miny, maxx, maxy = bounds

        if with_full_frame:
            minx = 0
            miny = 0
            maxx = len_frame_x - 1
            maxy = len_frame_y - 1
        else:
            minx = max(0, minx - pixels_around)
            miny = max(0, miny - pixels_around)
            maxx = min(len_frame_x - 1, maxx + pixels_around)
            maxy = min(len_frame_y - 1, maxy + pixels_around)

        len_x = maxx - minx + 1
        len_y = maxy - miny + 1

        # mask used in order to keep only the cells pixel
        # the mask put all pixels in the polygon, including the pixels on the exterior line to zero
        scaled_poly_gon = self.scale_polygon_to_source(poly_gon=poly_gon, minx=minx, miny=miny)
        img = PIL.Image.new('1', (len_x, len_y), 1)
        if buffer is not None:
            scaled_poly_gon = scaled_poly_gon.buffer(buffer)
        ImageDraw.Draw(img).polygon(list(scaled_poly_gon.exterior.coords), outline=0, fill=0)
        mask = np.array(img)
        # mask = np.ones((len_x, len_y))
        # cv2.fillPoly(mask, scaled_poly_gon, 0)
        # mask = mask.astype(bool)

        source_profile = np.zeros((len_y, len_x))

        # selectionning the best peak to produce the source_profile
        peaks = np.where(peak_nums[cell, :] > 0)[0]
        threshold = np.percentile(traces[cell, peaks], 95)
        selected_peaks = peaks[np.where(traces[cell, peaks] > threshold)[0]]
        # max 10 peaks, min 5 peaks
        if len(selected_peaks) > 10:
            p = 10 / len(peaks)
            threshold = np.percentile(traces[cell, peaks], (1 - p) * 100)
            selected_peaks = peaks[np.where(traces[cell, peaks] > threshold)[0]]
        elif (len(selected_peaks) < 5) and (len(peaks) > 5):
            p = 5 / len(peaks)
            threshold = np.percentile(traces[cell, peaks], (1 - p) * 100)
            selected_peaks = peaks[np.where(traces[cell, peaks] > threshold)[0]]

        # print(f"threshold {threshold}")
        # print(f"n peaks: {len(selected_peaks)}")

        onsets_frames = np.where(spike_nums[cell, :] > 0)[0]
        pos_traces = np.copy(traces)
        pos_traces += abs(np.min(traces))
        for peak in selected_peaks:
            tmp_source_profile = np.zeros((len_y, len_x))
            onsets_before_peak = np.where(onsets_frames <= peak)[0]
            if len(onsets_before_peak) == 0:
                # shouldn't arrive
                continue
            onset = onsets_frames[onsets_before_peak[-1]]
            # print(f"onset {onset}, peak {peak}")
            frames_tiff = tiff_movie[onset:peak + 1]
            for frame_index, frame_tiff in enumerate(frames_tiff):
                tmp_source_profile += (frame_tiff[miny:maxy + 1, minx:maxx + 1] * pos_traces[cell, onset + frame_index])
            # averaging
            tmp_source_profile = tmp_source_profile / (np.sum(pos_traces[cell, onset:peak + 1]))
            source_profile += tmp_source_profile
        if len(selected_peaks) > 0:
            source_profile = source_profile / len(selected_peaks)

        return source_profile, minx, miny, mask

    def get_transient_profile(self, cell, transient, tiff_movie, traces,
                              pixels_around=0, bounds=None):
        len_frame_x = tiff_movie[0].shape[1]
        len_frame_y = tiff_movie[0].shape[0]

        # determining the size of the square surrounding the cell
        if bounds is None:
            poly_gon = self.cells_polygon[cell]
            minx, miny, maxx, maxy = np.array(list(poly_gon.bounds)).astype(int)
        else:
            minx, miny, maxx, maxy = bounds

        minx = max(0, minx - pixels_around)
        miny = max(0, miny - pixels_around)
        maxx = min(len_frame_x - 1, maxx + pixels_around)
        maxy = min(len_frame_y - 1, maxy + pixels_around)

        len_x = maxx - minx + 1
        len_y = maxy - miny + 1

        transient_profile = np.zeros((len_y, len_x))
        frames_tiff = tiff_movie[transient[0]:transient[-1] + 1]
        # print(f"transient[0] {transient[0]}, transient[1] {transient[1]}")
        # now we do the weighted average
        raw_traces = np.copy(traces)
        # so the lowest value is zero
        raw_traces += abs(np.min(raw_traces))

        for frame_index, frame_tiff in enumerate(frames_tiff):
            transient_profile += (
                    frame_tiff[miny:maxy + 1, minx:maxx + 1] * raw_traces[cell, transient[0] + frame_index])
        # averaging
        transient_profile = transient_profile / (np.sum(raw_traces[cell, transient[0]:transient[-1] + 1]))

        return transient_profile, minx, miny

    def corr_between_source_and_transient(self, cell, transient, source_profile_dict, tiff_movie, traces,
                                          source_profile_corr_dict=None,
                                          pixels_around=1):
        """
        Measure the correlation (pearson) between a source and transient profile for a giveb cell
        :param cell:
        :param transient:
        :param source_profile_dict should contains cell as key, and results of get_source_profile avec values
        :param pixels_around:
        :param source_profile_corr_dict: if not None, used to save the correlation of the source profile, f
        for memory and computing proficiency
        :return:
        """
        # print('corr_between_source_and_transient')
        poly_gon = self.cells_polygon[cell]

        # Correlation test
        bounds_corr = np.array(list(poly_gon.bounds)).astype(int)
        # looking if this source has been computed before for correlation
        if (source_profile_corr_dict is not None) and (cell in source_profile_corr_dict):
            source_profile_corr, mask_source_profile = source_profile_corr_dict[cell]
        else:
            source_profile_corr, minx_corr, \
                miny_corr, mask_source_profile, xy_source = source_profile_dict[cell]
            # normalizing
            source_profile_corr = source_profile_corr - np.mean(source_profile_corr)
            # we want the mask to be at ones over the cell
            mask_source_profile = (1 - mask_source_profile).astype(bool)
            if source_profile_corr_dict is not None:
                source_profile_corr_dict[cell] = (source_profile_corr, mask_source_profile)

        transient_profile_corr, minx_corr, miny_corr = self.get_transient_profile(cell=cell,
                                                                                  transient=transient,
                                                                                  tiff_movie=tiff_movie, traces=traces,
                                                                                  pixels_around=pixels_around,
                                                                                  bounds=bounds_corr)
        transient_profile_corr = transient_profile_corr - np.mean(transient_profile_corr)

        pearson_corr, pearson_p_value = stats.pearsonr(source_profile_corr[mask_source_profile],
                                                       transient_profile_corr[mask_source_profile])

        return pearson_corr

def _angle_to_point(point, centre):
    '''calculate angle in 2-D between points and x axis'''
    delta = point - centre
    res = np.arctan(delta[1] / delta[0])
    if delta[0] < 0:
        res += np.pi
    return res


def area_of_triangle(p1, p2, p3):
    '''calculate area of any triangle given co-ordinates of the corners'''
    return np.linalg.norm(np.cross((p2 - p1), (p3 - p1))) / 2.


def convex_hull(points, smidgen=0.0075):
    '''
    from: https://stackoverflow.com/questions/17553035/draw-a-smooth-polygon-around-data-points-in-a-scatter-plot-in-matplotlib
    Calculate subset of points that make a convex hull around points
    Recursively eliminates points that lie inside two neighbouring points until only convex hull is remaining.

    :Parameters:
    points : ndarray (2 x m)
    array of points for which to find hull
    use pylab to show progress?
    smidgen : float
    offset for graphic number labels - useful values depend on your data range

    :Returns:
    hull_points : ndarray (2 x n)
    convex hull surrounding points
    '''

    n_pts = points.shape[1]
    # assert(n_pts > 5)
    centre = points.mean(1)

    angles = np.apply_along_axis(_angle_to_point, 0, points, centre)
    pts_ord = points[:, angles.argsort()]

    pts = [x[0] for x in zip(pts_ord.transpose())]
    prev_pts = len(pts) + 1
    k = 0
    while prev_pts > n_pts:
        prev_pts = n_pts
        n_pts = len(pts)
        i = -2
        while i < (n_pts - 2):
            Aij = area_of_triangle(centre, pts[i], pts[(i + 1) % n_pts])
            Ajk = area_of_triangle(centre, pts[(i + 1) % n_pts], pts[(i + 2) % n_pts])
            Aik = area_of_triangle(centre, pts[i], pts[(i + 2) % n_pts])
            if Aij + Ajk < Aik:
                del pts[i + 1]
            i += 1
            n_pts = len(pts)
        k += 1
    return np.asarray(pts)
