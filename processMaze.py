import os
import time # TODO: Time how long it takes to solve maze

from PIL import Image

from cropBorder import cropBorder

"""MAZES FROM http://hereandabove.com/maze/mazeorig.form.html"""

class Node(object):

    def __init__(self, x_pos, y_pos, surroundings=None, start=False, end=False):

        self.name = 'node_%s_%s' % (x_pos, y_pos)
        self.x_pos, self.y_pos = (x_pos, y_pos)
        self.surroundings = surroundings
        self.start = start
        self.end = end
        self._adjacent_nodes = {}

    def __str__(self):
        return self.name

    @property
    def adjacent_nodes(self):
        """Adjacent Node Property"""
        return self._adjacent_nodes

    def set_adjacent_nodes(self, key, value):
        """Sets adjacent node"""
        self._adjacent_nodes[key] = value

class Maze(object):

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    def __init__(self, filename, to_crop=False):

        self.image = Image.open(filename)
        self.maze = Image.open(cropBorder(self.image)) if to_crop else self.image
        self.height, self.width = self.maze.size
        self.node_dict = self.find_nodes()[0]
        self.node_maze = Image.open(self.find_nodes()[1])
        self.graph = self.make_graph()

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

                if pix != self.BLACK:
                    surroundings[direction] = True
                else:
                    surroundings[direction] = False

        return surroundings

    def find_nodes(self):
        """Finds and returns nodes in a maze"""

        maze_copy = self.maze.copy()

        node_dict = {}

        # Get start and end nodes
        for x in xrange(self.width):

            if self.maze.getpixel((x, 0)) == self.WHITE:

                node_name = 'node_%s_%s' % (x, 0)

                node_dict[node_name] = Node(x, 0, surroundings=self.get_surroundings(x,0), start=True)

                maze_copy.putpixel((x, 0), self.RED)

            if self.maze.getpixel((x, self.height-1)) == self.WHITE:

                node_name = 'node_%s_%s' % (x, self.height-1)

                node_dict['node_%s_%s' % (x, self.height-1)] = Node(x, self.height-1, surroundings=self.get_surroundings(x, self.height-1), end=True)

                maze_copy.putpixel((x, self.height-1), self.RED)

        # Get the rest of the nodes
        for y in xrange(1, self.height-1):
            for x in xrange(1, self.width):

                if self.maze.getpixel((x,y)) == self.WHITE:

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
                        node_dict['node_%s_%s' % (x,y)] = Node(x, y, surroundings=self.get_surroundings(x,y))

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

        node_list = self.node_list()

        # Loop through the nodes
        for key in self.node_dict:

            # Pull a given node from the dictionary, get some of its attributes
            node = self.node_dict[key]
            surroundings = node.surroundings
            x_pos = node.x_pos
            y_pos = node.y_pos

            # Loop through its surroundings, find nodes
            for direction in surroundings:

                path = surroundings[direction]

                if path:

                    node_in_dir = self.check_nodes_in_dir(x_pos, y_pos, direction_sums[direction])
                    node.set_adjacent_nodes(direction, node_in_dir)

                else:

                    node.set_adjacent_nodes(direction, None)

    # Define function to check for nodes in given dir
    def check_nodes_in_dir(self, x_pos, y_pos, direc_sum):
        """
           Checks for nodes in the direction directed by direc_sum using recursion.
           Very specified just for the `make_graph()` method. TODO: Make it generalized
        """

        # `direc_sum` is `direction_sums` tuple defined below
        x_pos += direc_sum[0]
        y_pos += direc_sum[1]

        try:
            return self.get_node_by_pos(x_pos, y_pos)
        except KeyError:
            return self.check_nodes_in_dir(x_pos, y_pos, direc_sum)

    def get_pixel(self, x_pos, y_pos, maze=None):
        """Return pixel RGB Value"""
        if maze is None:
            maze = self.maze

        return maze.getpixel((x_pos, y_pos))

    def get_node_by_pos(self, x_pos, y_pos):
        """Gets node from the x and y position"""

        node_name = 'node_%s_%s' % (x_pos, y_pos)
        return self.node_dict[node_name]

    def node_list(self):
        """returns node names"""
        return self.node_dict.keys()

if __name__ == '__main__':

    # TODO: Find neater way to acomplish this
    cwd = os.getcwd()
    os.chdir(cwd + '/mazes')

    maze = Maze('smallmaze.png', to_crop=True)

    print 'Success'
