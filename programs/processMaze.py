import os

from PIL import Image

from cleanMaze import cropBorder

"""MAZES FROM http://hereandabove.com/maze/mazeorig.form.html"""

class Maze(object):

    # Start of Node Class #

    class Node(object):

        def __init__(self, x_pos, y_pos, surroundings=None, start=False, end=False):

            self.name = 'node_%s_%s' % (x_pos, y_pos)
            self.x_pos, self.y_pos = (x_pos, y_pos)
            self.surroundings = surroundings
            self.start = start
            self.end = end
            self._adjacent_nodes = {}
            self._prev_node = None

        @property
        def adjacent_nodes(self):
            """Adjacent Node Property"""
            return self._adjacent_nodes

        def set_adjacent_nodes(self, key, value):
            """Sets adjacent node"""
            self._adjacent_nodes[key] = value

        @property
        def prev_node(self):
            """Previous Node Property"""
            return self._prev_node

        def set_prev_node(self, value):
            """Set Previous node"""
            self._prev_node = value

    # End of Node Class #

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    start_node = None
    end_node = None

    def __init__(self, filename, to_crop=False):

        self.image = Image.open(filename)
        self.maze = Image.open(cropBorder(self.image)) if to_crop else self.image
        self.height, self.width = self.maze.size
        self.node_dict = self.find_nodes()[0]
        self.node_maze = Image.open(self.find_nodes()[1])
        self.make_graph()
        print "PROCESSING MAZE"

    def get_surroundings(self, x_pos, y_pos):
        """Gets the values of up,down,left,right at given coords."""

        # The x,y coordinates of a given pixel's surorundings at x_pos and y_pos
        up = (x_pos, y_pos - 1) if y_pos - 1 >= 0 else False
        down = (x_pos, y_pos + 1) if y_pos + 1 < self.height else False
        left = (x_pos - 1, y_pos) if x_pos - 1 >= 0 else False
        right = (x_pos + 1, y_pos) if x_pos + 1 < self.width else False

        surroundings = {
            'up': up,
            'down': down,
            'left': left,
            'right': right
        }

        for direction in surroundings:

            if surroundings[direction]:
                pix = self.maze.getpixel(surroundings[direction])

                if not self.check_black(pix):
                    surroundings[direction] = True
                else:
                    surroundings[direction] = False

        return surroundings

    def find_start_end_horizontal(self):
        """Checks top and bottom for for start/end node"""

        maze_copy = self.maze.copy()

        node_dict = {}

        # Get start and end nodes
        for x in xrange(self.width):

            pix = self.maze.getpixel((x, 0))

            if self.check_white(pix) and not self.start_node:

                node_name = 'node_%s_%s' % (x, 0)

                node_dict[node_name] = self.Node(x, 0, surroundings=self.get_surroundings(x,0), start=True)

                self.start_node = node_name

                self.color_pixel(x, 0, self.RED)

            pix = self.maze.getpixel((x, self.height-1))

            if self.check_white(pix) and not self.end_node:

                node_name = 'node_%s_%s' % (x, self.height-1)

                node_dict[node_name] = self.Node(x, self.height-1, surroundings=self.get_surroundings(x, self.height-1), end=True)

                self.end_node = node_name

                self.color_pixel(x, self.height-1, self.RED)

        return node_dict

    def find_start_end_vertical(self):
        """Checks left and right for start/end node"""

        maze_copy = self.maze.copy()

        node_dict = {}

        if not self.start_node:

            for y in xrange(self.height-1):

                pix = self.maze.getpixel((0, y))

                if self.check_white(pix):

                    node_name = 'node_%s_%s' % (0, y)

                    node_dict[node_name] = self.Node(0, y, surroundings=self.get_surroundings(0,y), start=True)

                    self.start_node = node_name

                    self.color_pixel(0, y, self.RED)

        if not self.end_node:

            for y in xrange(self.height-1):

                pix = self.maze.getpixel((self.width-1, self.height-1))

                if self.check_white(pix):

                    node_name = 'node_%s_%s' % (self.width, y)

                    node_dict[node_name] = self.Node(self.width, y, surroundings=self.get_surroundings(self.width, y), end=True)

                    self.end_node = node_name

                    self.color_pixel(self.width, y, self.RED)

        return node_dict

    def find_nodes(self):
        """Finds and returns nodes in a maze"""

        maze_copy = self.maze.copy()

        node_dict_1 = self.find_start_end_horizontal()

        node_dict_2 = self.find_start_end_vertical()

        node_dict = node_dict_1.copy()
        node_dict.update(node_dict_2)

        # Get the rest of the nodes
        for y in xrange(1, self.height-1):
            for x in xrange(1, self.width):

                pix = self.maze.getpixel((x,y))
                if self.check_white(pix):

                    isNode = True
                    directions = self.get_surroundings(x,y)

                    up_and_down = directions['up'] and directions['down']
                    up_or_down = directions['up'] or directions['down']

                    left_and_right = directions['left'] and directions['right']
                    left_or_right = directions['left'] or directions['right']

                    # Rules for a node (a node is where you can / must change direction while following a path)
                    if up_and_down and not left_or_right:
                        isNode = False

                    elif left_and_right and not up_or_down:
                        isNode = False

                    # Color maze, assign nodes
                    if isNode:
                        node_dict['node_%s_%s' % (x,y)] = self.Node(x, y, surroundings=self.get_surroundings(x,y))

                        maze_copy.putpixel((x, y), self.RED)

        filename =  self.maze.filename.replace('cropped_', 'nodes_')

        maze_copy.save(filename)

        return node_dict, filename

    def make_graph(self):
        """Connect the nodes"""

        direction_sums = {
            'up': (0, -1),
            'down': (0, 1),
            'left': (-1, 0),
            'right': (1, 0)
        }

        node_list = self.node_dict.keys()

        # Loop through the nodes
        for key, node in self.node_dict.items():

            # Pull a given node from the dictionary, get some of its attributes
            surroundings = node.surroundings
            x_pos = node.x_pos
            y_pos = node.y_pos

            # Loop through its surroundings, find nodes
            for direction in surroundings:

                path = surroundings[direction]

                if path:

                    # Get the adjacent node and its position in tuple form from check_nodes_in_dir, split them up
                    node_and_pos = self.check_nodes_in_dir(x_pos, y_pos, direction_sums[direction])

                    adj_node = node_and_pos[0]
                    distance = abs((x_pos - node_and_pos[1][0]) + (y_pos - node_and_pos[1][1]))

                    # Set adjacent node in that direction with the distance
                    node.set_adjacent_nodes(direction, (adj_node, distance))

                else:

                    node.set_adjacent_nodes(direction, None)

    def check_nodes_in_dir(self, x_pos, y_pos, direc_sum):
        """
           Checks for nodes in the direction directed by direc_sum.
           Very specified just for the `make_graph()` method.
        """

        # `direc_sum` is `direction_sums` tuple defined above
        x_pos += direc_sum[0]
        y_pos += direc_sum[1]


        node = self.get_node_by_pos(x_pos, y_pos)
        while not node:
            x_pos += direc_sum[0]
            y_pos += direc_sum[1]
            node = self.get_node_by_pos(x_pos, y_pos)

        return node, (x_pos, y_pos)

    def get_pixel(self, x_pos, y_pos):
        """Return pixel RGB Value"""

        return self.maze.getpixel((x_pos, y_pos), 'RGB')

    def get_node_by_pos(self, x_pos, y_pos):
        """Gets node from the x and y position"""

        node_name = 'node_%s_%s' % (x_pos, y_pos)
        return self.node_dict.get(node_name, None)

    def color_pixel(self, x, y, color, filename=None):

        filename = filename if filename else self.maze.filename

        self.maze.putpixel((x, y), color)
        self.maze.save(filename)

    def remove_color(self):

        for x in xrange(self.width):
            for y in xrange(self.height-1):

                pix = self.maze.getpixel((x, y))

                if not self.check_white(pix) and not self.check_black(pix):

                    self.color_pixel(x, y, self.WHITE)

    def check_white(self, rgb_tuple):
        """Checks if rgb_tuple is white"""
        return True if rgb_tuple == (255,255,255) or rgb_tuple == (255,255,255,255) else False

    def check_black(self, rgb_tuple):
        """Checks if rgb_tuple is black"""
        return True if rgb_tuple == (0,0,0) or rgb_tuple == (0,0,0,255) else False

if __name__ == '__main__':

    os.chdir('..')
    os.chdir(os.getcwd() + '/mazes')

    maze = Maze('unbalanced.png', to_crop=True)

    print 'Success'
