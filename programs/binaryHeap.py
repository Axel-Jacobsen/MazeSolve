class BinaryHeap(object):
    """Minimum Binary Heap Object"""

    def __init__(self, array):
        self.heap = array

    def heapify(self):
        """Returns heap"""

        for i in xrange(len(self.heap) // 2 - 1, -1, -1):

            self.bubble_down(i)

    def delete_min(self):
        """deletes and returns minimum value (in this case the root of the heap)"""

        self.switch(0, -1)

        min = self.heap.pop(-1)

        self.bubble_down(0)

        return min

    def insert(self, key):
        """Inserts key into heap and heapifies the heap"""

        self.heap.append(key)

        self.bubble_up(len(self.heap) - 1)

    def bubble_up(self, i):
        """Modifies self.heap to 'heapify' a new node"""

        parent = self.parent(i)

        while (parent is not None) and (self.heap[i][1] < self.heap[parent][1]):

            self.switch(i, parent)

            parent = self.parent(parent)

    def bubble_down(self, i):
        """Modifies self.heap such that index is a root of a heap (bubble down)"""

        smallest = self.find_smallest(i)

        org = i

        while smallest != org:

            self.switch(org, smallest)

            org = smallest

            smallest = self.find_smallest(smallest)

    def find_smallest(self, i):
        """Finds the smallest node of a triplet in a binary tree (i.e. parent and 2 children)"""

        left_child = self.left_child(i)

        right_child = self.right_child(i)

        if left_child and (self.heap[left_child][1] < self.heap[i][1]):

            smallest = left_child

        else:

            smallest = i

        if right_child and (self.heap[right_child][1] < self.heap[smallest][1]):

            smallest = right_child

        return smallest

    def switch(self, a, b):
        """Switches values positions a and b in array"""

        self.heap[a], self.heap[b] = self.heap[b], self.heap[a]

    @staticmethod
    def parent(n):
        """Returns parent of node at n; None if there isn't a parent"""

        return None if n == 0 else (n - 1) // 2

    def left_child(self, n):
        """Returns left child of node at n; None if there isn't a left_child"""

        if 2 * n + 1 >= len(self.heap):
            return None
        else:
            return 2 * n + 1

    def right_child(self, n):
        """Returns right child of node at n; None if there isn't a right_child"""

        if 2 * n + 2 >= len(self.heap):
            return None
        else:
            return 2 * n + 2
