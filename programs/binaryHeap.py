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

        if (parent is not None) and (self.heap[i] < self.heap[parent]):

            self.switch(i, parent)

            self.bubble_up(parent)

    def bubble_down(self, i):
        """Modifies self.heap such that index is a root of a heap (bubble down)"""

        left_child = self.left_child(i)

        right_child = self.right_child(i)

        if left_child and self.heap[left_child] < self.heap[i]:

            smallest = left_child

        else:

            smallest = i

        if right_child and self.heap[right_child] < self.heap[smallest]:

            smallest = right_child

        if smallest != i:

            self.switch(i, smallest)
            
            self.bubble_down(smallest)

    def switch(self, a, b):
        """Switches values positions a and b in array"""

        self.heap[a], self.heap[b] = self.heap[b], self.heap[a]

    def parent(self, n):
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
