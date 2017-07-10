import os
import time # TODO: Time how long it takes to solve maze

from PIL import Image

from cropBorder import cropBorder

"""MAZES FROM http://hereandabove.com/maze/mazeorig.form.html"""

class Maze(object):

    BLACK = (0,0,0)
    WHITE = (255,255,255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    class Node(object):

        # TODO: Write a way to access Maze.get_surroundings so we can have surroundings just from
        # the coords
        def __init__(self, x_pos, y_pos, adjacent_nodes={}, surroundings=None, start=False, end=False):

            self.name = 'Node (%s, %s)' % (x_pos, y_pos)
            self.x_pos, self.y_pos = (x_pos, y_pos)
            self.adjacent_nodes = adjacent_nodes
            self.surroundings = surroundings
            self.start = start
            self.end = end

        def __str__(self):
            return self.name

    def __init__(self, filename, to_crop=False):

        self.image = Image.open(filename)
        self.maze = Image.open(cropBorder(self.image)) if to_crop else self.image
        self.height, self.width = self.maze.size
        self.node_dict = self.find_nodes()[0]
        self.node_maze = Image.open(self.find_nodes()[1])
        self.graph = self.make_graph(self.node_dict)

    def get_surroundings(self, x_pos, y_pos):
        """Gets the values of up,down,left,right at given coords."""

        up = (x_pos, y_pos - 1) if y_pos - 1 >= 0 else False
        down = (x_pos, y_pos + 1) if y_pos + 1 < self.height else False
        left = (x_pos - 1, y_pos) if x_pos - 1 > 0 else False
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

                node_dict[node_name] = self.Node(x, 0, surroundings=self.get_surroundings(x,0), start=True)

                maze_copy.putpixel((x, 0), self.RED)

            if self.maze.getpixel((x, self.height-1)) == self.WHITE:

                node_name = 'node_%s_%s' % (x, self.height-1)

                node_dict['node_%s_%s' % (x, self.height-1)] = self.Node(x, self.height-1, surroundings=self.get_surroundings(x, self.height-1), end=True)

                maze_copy.putpixel((x, self.height-1), self.RED)

        # Get the rest of the nodes
        for y in xrange(self.height-1):
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
                        node_dict['node_%s_%s' % (x,y)] = self.Node(x, y, surroundings=self.get_surroundings(x,y))

                        maze_copy.putpixel((x, y), self.RED)

        filename =  self.maze.filename.replace('cropped_', 'nodes_')
        maze_copy.save(filename)

        return node_dict, filename

    def make_graph(self, node_dict):
        """Connects the Nodes"""

        mazeCopy = self.maze.copy()

        for key in node_dict:

            node = node_dict[key]

            surroundings = node.surroundings
            x_pos, y_pos = node.x_pos, node.y_pos

            print '\nORG NODE: ', x_pos, y_pos
            mazeCopy.putpixel((x_pos, y_pos), self.RED)

            def move_to_node(direction, x_pos, y_pos):

                direction_additions = {
                    'up': (0,-1),
                    'down': (0,1),
                    'right': (1,0),
                    'left': (-1,0)
                }

                if surroundings[direction]:
                    # Move the x and y position off of the original node
                    x_pos += direction_additions[direction][0]
                    y_pos += direction_additions[direction][1]

                    while self.node_maze.getpixel((x_pos, y_pos)) == self.WHITE:
                        x_pos += direction_additions[direction][0]
                        y_pos += direction_additions[direction][1]

                    print 'NODE: ', x_pos, y_pos
                    # mazeCopy.putpixel((x_pos, y_pos), self.GREEN)

                    found_node = self.get_node_by_pos(x_pos, y_pos)
                    node.adjacent_nodes[direction] = found_node

                else:
                    node.adjacent_nodes[direction] = None

            move_to_node('up', x_pos, y_pos)
            move_to_node('down', x_pos, y_pos)
            move_to_node('left', x_pos, y_pos)
            move_to_node('right', x_pos, y_pos)
            mazeCopy.save('TEST.png')

    def get_pixel(self, x_pos, y_pos, maze=None):
        """Return pixel RGB Value"""
        if maze is None:
            maze = self.maze

        return maze.getpixel((x_pos, y_pos))

    def get_node_by_pos(self, x_pos, y_pos):
        """Gets node from the x and y position"""

        node_name = 'node_%s_%s' % (x_pos, y_pos)

        return self.node_dict[node_name]

    def print_nodes(self):
        """Prints node names"""
        for node in self.node_dict:
            print self.node_dict[node]

    def mark_position(self, maze, x_pos, y_pos, filename=None, color=(0,255,255)):

        if filename is None:
            filename = maze.filename

        maze = maze.copy()
        maze.putpixel((x_pos, y_pos), color)
        maze.save(filename)

        return filename

    def test_node_locations(self):
        """Confirm that the identified nodes are in the correct location"""
        for key in self.node_dict:
            node = self.node_dict[key]

            for key in node.adjacent_nodes:

                adj_node = node.adjacent_nodes[key]
                pix = maze.get_pixel(node.x_pos, node.y_pos)
                print pix
                # if pix != self.RED:
                #     print 'ADJACENT NODE AT ', node.x_pos, node.y_pos, 'DOESNT EXIST'


if __name__ == '__main__':

    # TODO: Find neater way to acomplish this
    cwd = os.getcwd()
    os.chdir(cwd + '/mazes')

    maze = Maze('smallmaze.png', to_crop=True)

    print 'Surroundings: ', maze.get_node_by_pos(3,1).surroundings
    print 'Adjacent Nodes: ', maze.get_node_by_pos(3,1).adjacent_nodes
    maze.test_node_locations()

    print 'Success'
