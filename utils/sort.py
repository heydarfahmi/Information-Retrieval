import sys


class Node:
    def __init__(self, index: int, value: int):
        self.index = index
        self.value = value


class MaxHeap:

    def __init__(self, maxsize):

        self.maxsize = maxsize
        self.size = 0
        self.Heap = [Node(0, 0)] * (self.maxsize + 1)
        self.Heap[0] = Node(0, sys.maxsize)
        self.ROOT = 1

    def get_parent(self, pos):

        return pos // 2

    def get_right_child(self, pos):

        return (2 * pos) + 1

    def get_left_child(self, pos):

        return 2 * pos

    def check_if_leaf(self, pos):

        if pos >= (self.size // 2) and pos <= self.size:
            return True
        return False

    def swap_nodes(self, fpos, spos):
        self.Heap[fpos], self.Heap[spos] = (self.Heap[spos],
                                            self.Heap[fpos])

    def max_heapify(self, pos):

        if not self.check_if_leaf(pos):
            if (self.Heap[pos].value < self.Heap[self.get_left_child(pos)].value or
                    self.Heap[pos].value < self.Heap[self.get_right_child(pos)].value):

                if (self.Heap[self.get_left_child(pos)].value >
                        self.Heap[self.get_right_child(pos)].value):
                    self.swap_nodes(pos, self.get_left_child(pos))
                    self.max_heapify(self.get_left_child(pos))

                else:
                    self.swap_nodes(pos, self.get_right_child(pos))
                    self.max_heapify(self.get_right_child(pos))

    def insert_node(self, element):
        print(element)

        if self.size >= self.maxsize:
            return
        self.size += 1
        self.Heap[self.size] = element

        current = self.size

        while (self.Heap[current].value >
               self.Heap[self.get_parent(current)].value):
            self.swap_nodes(current, self.get_parent(current))
            current = self.get_parent(current)

    def extract_root(self):

        popped = self.Heap[self.ROOT]
        self.Heap[self.ROOT] = self.Heap[self.size]
        self.size -= 1
        self.max_heapify(self.ROOT)

        return popped


def heapify_array(array):
    size = len(array)
    heap = MaxHeap(size)
    for index, value in enumerate(array):
        node = Node(index, value)
        heap.insert_node(node)
    return heap


def k_max(array, k, treshold=0):
    heap = heapify_array(array)
    best = []
    for i in range(min(len(array), k)):
        next_best = heap.extract_root()
        if next_best.value <= treshold:
            break
        best.append(next_best.index)
        print(best)
        print(next_best.value)
    return best
