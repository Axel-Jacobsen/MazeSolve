from PIL import Image
from cropBorder import cropBorder
import os
import time

"""MAZES FROM http://hereandabove.com/maze/mazeorig.form.html"""

class Maze(object):

    BLACK = (0,0,0)
    WHITE = (255,255,255)

    class Node(object):

        def __init__(self, x_pos, y_pos):

            self.coords = (x_pos, y_pos)

            self.directions = {
                'up': False,
                'down': False,
                'left': False,
                'right': False
            }


    def __init__(self, filename, toCrop=True):

        self.image = Image.open(filename)

        if toCrop:
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

        directions = {
            'up': up,
            'down': down,
            'left': left,
            'right': right
        }

        for key in directions:
            if directions[key]:

                pix = self.maze.getpixel(directions[key])

                if pix == self.WHITE:
                    directions[key] = True
                else:
                    directions[key] = False

        return directions

    def get_graph(self):

        colorMaze = self.maze.copy()

        for x in xrange(self.width):

            if self.maze.getpixel((x, 0)) == self.WHITE:
                start = self.Node(x,0)
                colorMaze.putpixel((x, 0), (255, 0, 0))


            if self.maze.getpixel((x, self.height-1)) == self.WHITE:
                end = self.Node(x, self.height-1)
                colorMaze.putpixel((x, self.height-1), (255, 0, 0))


        for y in xrange(self.height-1):
            for x in xrange(1, self.width):
                if self.maze.getpixel((x,y)) == self.WHITE:

                    isNode = True
                    directions = self.get_surroundings(x,y)

                    up_and_down = directions['up'] and directions['down']
                    up_or_down = directions['up'] or directions['down']

                    left_and_right = directions['left'] and directions['right']
                    left_or_right = directions['left'] or directions['right']


                    if up_and_down and not left_or_right:
                        isNode = False

                    elif left_and_right and not up_or_down:
                        isNode = False




                    if isNode:
                        colorMaze.putpixel((x, y), (255, 0, 0))

        filename = 'color' + self.maze.filename
        colorMaze.save(filename)

if __name__ == '__main__':

    cwd = os.getcwd()
    os.chdir(cwd + '/mazes')

    maze = Maze('smallmaze.png')

    print 'Success'
