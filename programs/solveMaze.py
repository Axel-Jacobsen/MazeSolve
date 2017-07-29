import os

from processMaze import Maze
from binaryHeap import BinaryHeap

class mazeSolve(object):
    """Takes in a maze, makes a graph, and solves it"""

    def __init__(self, filename, to_crop=False):

        self.maze = Maze('smallmaze.png', to_crop=True)
        self.nodes = self.maze.node_dict
        self.priority_que = BinaryHeap([list(a) for a in zip(self.nodes.keys(), [float('inf')] * len(self.nodes))])
        # Want to use zip function, but need the item to be mutable. therefore, the `list(a) for a in zip...` notation
        self.path = []

    def solve(self):
        """Connects the nodes from the starting node to the ending node"""

        # Find the starting node of the maze, add it to self.path, and assign
        # the node a distance from the start of 0
        start = self.maze.start_node
        self.path.append(start)
        self.add_value(start, 0)

        adjacent_nodes = self.nodes[start].adjacent_nodes

        for direction, node_dist in adjacent_nodes.items():

            if not node_dist:
                self.add_value(node_dist[0], node_dist[1])

        return self.nodes[start].adjacent_nodes

    # These next two functions are O(n), which is unideal. But the binary heap isn't super fast anyways. TODO: Fix
    def add_value(self, node, value):
        """Finds `node` in priority_que and assigns `value` to it's second value, then calls heapify()"""
        found = False

        for node_dist in self.priority_que.heap:

            # If the node hasn't been discovered yet, assign it's distance `value`. Else add value to it's distance
            if node == node_dist[0]:
                node_dist[1] = value if node_dist[1] == float('inf') else node_dist[1] + value

                found = True
                break

        if not found:
            raise ValueError('Node not in priority_que')

    def get_value(self, node):
        """Finds `node` in priority_que and returns it's value"""

        for node_dist in self.priority_que.heap:

            if node == node_dist[0]:
                return node_dist[1]

        raise ValueError('Node not in priority_que')

    def heapify(self):
        """Shortcut method"""
        self.priority_que.heapify()


if __name__ == '__main__':

    os.chdir('..')
    os.chdir(os.getcwd() + '/mazes')

    dijkstra = mazeSolve('smallmaze.png', to_crop=True)

    print 'Success'
