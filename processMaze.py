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
        def __init__(self, x_pos, y_pos, adjacent_nodes={}, surroundings=None):

            self.name = 'Node (%s, %s)' % (x_pos, y_pos)
            self.x_pos, self.y_pos = (x_pos, y_pos)
            self.adjacent_nodes = adjacent_nodes
            self.surroundings = surroundings

        def __str__(self):
            return self.name

    def __init__(self, filename, to_crop=False):

        self.filename = filename
        self.image = Image.open(filename)
        self.maze = Image.open(cropBorder(self.image)) if to_crop else self.image
        self.height, self.width = self.maze.size
        self.nodes = self.find_nodes()
        self.node_maze = None
        self.graph = self.make_graph(self.nodes)

    def get_surroundings(self, x_pos, y_pos):
        """Gets the values of up,down,left,right at given coords."""

        up = (x_pos, y_pos - 1) if y_pos - 1 >= 0 else False
        down = (x_pos, y_pos + 1) if y_pos + 1 <= self.height else False
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

                if pix == self.WHITE:
                    surroundings[direction] = True
                else:
                    surroundings[direction] = False

        return surroundings

    def find_nodes(self):
        """Finds and returns nodes in a maze"""

        self.node_maze = self.maze.copy()
        print type(self.node_maze)
        self.node_maze.save('Nodes_' + self.maze.filename)
        node_dict = {}

        # Get start and end nodes
        for x in xrange(self.width):

            if self.maze.getpixel((x, 0)) == self.WHITE:

                start = self.Node(x, 0, surroundings=self.get_surroundings(x, 0))
                self.node_maze.putpixel((x, 0), self.RED)

            if self.maze.getpixel((x, self.height-1)) == self.WHITE:

                end = self.Node(x, self.height-1, surroundings=self.get_surroundings(x, 0))
                self.node_maze.putpixel((x, self.height-1), self.RED)

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

                        self.node_maze.putpixel((x, y), self.RED)

        filename =  self.maze.filename.replace('cropped_', 'Nodes_')
        self.node_maze.save(filename)

        return node_dict

    def make_graph(self, node_dict):
        """Connects the Nodes"""

        for key in node_dict:

            node = node_dict[key]

            surroundings = node.surroundings
            x_pos, y_pos = node.x_pos, node.y_pos

            # TODO: condense the next 4 if-else statements
            if surroundings['up']:

                while self.node_maze.getpixel((x_pos, y_pos)) == self.WHITE:
                    y_pos -= 1

                found_node = self.get_node_by_pos(x_pos, y_pos)
                node.adjacent_nodes['up'] = found_node

            else:
                node.adjacent_nodes['up'] = None

            if surroundings['down']:

                while self.node_maze.getpixel((x_pos, y_pos)) == self.WHITE:
                    y_pos += 1

                found_node = self.get_node_by_pos(x_pos, y_pos)
                node.adjacent_nodes['down'] = found_node

            else:
                node.adjacent_nodes['down'] = None

            if surroundings['right']:

                while self.node_maze.getpixel((x_pos, y_pos)) == self.WHITE:
                    x_pos += 1

                found_node = self.get_node_by_pos(x_pos, y_pos)
                node.adjacent_nodes['right'] = found_node

            else:
                node.adjacent_nodes['right'] = None

            if surroundings['left']:

                while self.node_maze.getpixel((x_pos, y_pos)) == self.WHITE:
                    x_pos -= 1

                found_node = self.get_node_by_pos(x_pos, y_pos)
                node.adjacent_nodes['left'] = found_node

            else:
                node.adjacent_nodes['left'] = None


    def get_pixel(self, x_pos, y_pos, maze=None):
        """Return pixel RGB Value"""
        if maze is None:
            maze = self.maze

        return maze.getpixel((x_pos, y_pos))

    def get_node_by_pos(self, x_pos, y_pos):
        """Gets node from the x and y position"""

        node_name = 'node_%s_%s' % (x_pos, y_pos)

        return self.nodes[node_name]

    def print_nodes(self,nodes):
        """Prints node names"""
        for node in nodes:
            print node


if __name__ == '__main__':

    # TODO: Find neater way to acomplish this
    cwd = os.getcwd()
    os.chdir(cwd + '/mazes')

    maze = Maze('smallmaze.png', to_crop=True)

    print 'Success'
