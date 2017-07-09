import os
import time

from PIL import Image

from cropBorder import cropBorder

"""MAZES FROM http://hereandabove.com/maze/mazeorig.form.html"""

class Maze(object):

    BLACK = (0,0,0)
    WHITE = (255,255,255)


    class Node(object):

        def __init__(self, x_pos, y_pos, connected_nodes):

            self.name = 'Node at (%s, %s)' % (x_pos, y_pos)

            self.coords = (x_pos, y_pos)

            self.connected_nodes = connected_nodes

    def __init__(self, filename, to_crop=False):

        self.image = Image.open(filename)

        if to_crop:
            self.maze = Image.open(cropBorder(self.image))
        else:
            self.maze = self.image

        self.height, self.width = self.maze.size
        self.graph = self.get_graph()

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

        for key in surroundings:

            if surroundings[key]:
                pix = self.maze.getpixel(surroundings[key])

                if pix == self.WHITE:
                    surroundings[key] = True
                else:
                    surroundings[key] = False

        return surroundings

    def find_nodes(self):
        """Finds and returns nodes in a maze"""

        colorMaze = self.maze.copy()
        nodes = dict()

        # Get start and end nodes
        for x in xrange(self.width):

            if self.maze.getpixel((x, 0)) == self.WHITE:

                start = self.Node(x, 0, self.get_surroundings(x, 0))

                colorMaze.putpixel((x, 0), (255, 0, 0))


            if self.maze.getpixel((x, self.height-1)) == self.WHITE:

                end = self.Node(x, self.height-1, self.get_surroundings(x, 0))

                colorMaze.putpixel((x, self.height-1), (255, 0, 0))

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

                    # Color nodes.
                    if isNode:
                        nodes['node_%s_%s' % (x, y)] = self.Node(x, y, directions)
                        colorMaze.putpixel((x, y), (255, 0, 0))

        filename =  self.maze.filename.replace('cropped_', 'Nodes_')
        colorMaze.save(filename)

        return nodes

    def connect_nodes(self):
        """Connects the Nodes"""



    def get_graph(self):
        """Make a graph of the maze"""

        nodes = self.find_nodes()


if __name__ == '__main__':

    # This folder change is because of my lazyness, and because I wanted to keep the repositories seperate
    cwd = os.getcwd()
    os.chdir(cwd + '/mazes')

    maze = Maze('maze.png', to_crop=True)

    print 'Success'
