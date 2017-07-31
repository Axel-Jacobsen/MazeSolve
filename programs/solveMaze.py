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
        self.visited_nodes = set()

    def solve(self):
        """Connects the nodes from the starting node to the ending node"""

        # Find the starting node of the maze, add it to self.visited_nodes, and assign the node a distance from the start of 0
        start = self.maze.start_node

        self.add_value(start, 0)

        return self.process([start, 0])

    def process(self, curr_node):
        """
        Takes in curr_node, which is a
        Does 3 things:
            1. Removes curr_node from the priority_que
            2. Finds the adjacent nodes of curr_node
            3. Adds those nodes to the priority_que
        If the new min node is the end node, you're done. Else, call
        process() on the new min node
        """

        curr_node[0] = self.nodes[curr_node[0]]

        if curr_node[0].end == False:

            # Add min node to path and remove it from the priority_que
            self.visited_nodes.add(curr_node[0].name)
            self.priority_que.delete_min()
            print 'Current node (now removed): ', curr_node[0].name

            # Find the adjacent nodes of curr_node
            adjacent_nodes = curr_node[0].adjacent_nodes

            for direction, node_distance in adjacent_nodes.items():

                if node_distance and not (node_distance[0].name in self.visited_nodes):

                    try:
                        self.add_value(node_distance[0].name, node_distance[1] + curr_node[1])
                    except:
                        print '\n', node_distance[0].name, 'was not in the priority_que'
                        print 'Here is the priority_que:', self.priority_que.heap, '\n'
                        print 'Here is the visited_nodes:', self.visited_nodes
                        break

            self.heapify()

            return self.process(self.priority_que.heap[0])

        else:

            end_node = self.priority_que.delete_min()

            return end_node

    # These next two functions are O(n), which is unideal. But the binary heap isn't super fast anyways. TODO: Fix
    def add_value(self, node, value):
        """Finds `node` in priority_que and assigns `value` to it's second value. If the node hasn't been discovered yet, assign it's distance `value`. Else add value to it's distance"""
        found = False

        for node_dist in self.priority_que.heap:

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

    print 'Initial priority_que:', dijkstra.priority_que.heap
    print dijkstra.solve()

    print 'Success'
