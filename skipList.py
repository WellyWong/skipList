"""
Skip list is a data structure used to store sorted list of items, very much like Binary Search Tree.
The main advantage of using Skip list over BST is that it is best suited for concurrent access.

One of the most common implementations of BST is Red Black Tree. The problem of accessing this tree concurrently
comes when a data element has been modified and tree needs to re-balance, which would require mutex lock on
large part of tree. On the other hand, when inserting/deleting/updating a node in a Skip list,
only nodes directly connected to the affected nodes needs locking.

Skip Lists: A probabilistic alternative to Balanced Trees:
https://15721.courses.cs.cmu.edu/spring2018/papers/08-oltpindexes1/pugh-skiplists-cacm1990.pdf

Code from: https://github.com/jhomswk/Skip_List/blob/master/skip_list.py
"""
import random

class SkipList:

    class Element:
        def __init__(self, value, height):
            """
            Generates a skip-list element.
            """
            self.value = value
            self.quantity = 1  #to handle duplicates: if a value is already exist when adding another one, just increment quantity
            self.next = [None] * height


    def __init__(self):
        """
        Generates an empty skip-list.
        """
        self.head = self.Element(float("-inf"), height=0)
        self.tail = self.Element(float("inf"), height=0)
        self.num_elements = 0    #number of elements in the skip list, excluding head and tail
        self.head.next.append(self.tail)

    @staticmethod
    def random_height():
        """
        Generates a random height with distribution
        Prob(h = k) = 2^(-k).
        """
        height = 1
        while random.randint(0, 1) != 1:
            height += 1
        return height

    def search_path(self, value):
        """
        Return path[]. path[h] stores the last node Element visited at height h (with value < value of the argument)
        during the search of value through the skip list.
        """
        element = self.head
        path = [None] * len(self.head.next)   #len(self.head.next) == height of Skip list
        for h in range(len(self.head.next) - 1, -1, -1):
            while element.next[h].value < value:
                element = element.next[h]
            path[h] = element
        return path

    def search(self, value):
        """
        Returns the element containing value, if value is present in the skip-list.
        Returns None otherwise.
        """
        predecessor = self.search_path(value)
        target = predecessor[0].next[0]
        return target if target.value == value else None

    def __contains__(self, value):
        """
        Checks whether value is present in the skip-list.
        """
        return self.search(value) != None

    def insert(self, value):
        """
        Inserts value into the skip-list.
        """
        predecessor = self.search_path(value)
        target = predecessor[0].next[0]
        self.num_elements += 1

        if target.value == value:   #this will handle duplicates, we'll just increase the quantity
            target.quantity += 1
            return

        height = self.random_height()
        new_element = self.Element(value, height)

        for h in range(len(predecessor), height):  #if the new height is > current skip list height, run the loop until height matches
            self.head.next.append(self.tail)
            predecessor.append(self.head)

        for h in range(height):
            new_element.next[h] = predecessor[h].next[h]
            predecessor[h].next[h] = new_element

    def delete(self, value):
        """
        Deletes one entry of value in the skip-list.
        """
        predecessor = self.search_path(value)
        target = predecessor[0].next[0]

        if target.value != value:   #can't find the value in the skip list, return
            return

        self.num_elements -= 1

        if target.quantity > 1:     #reduce quantity (if quantity > 1), we have more than 1 duplicates in skip list, then return
            target.quantity -= 1
            return

        for h in range(len(target.next)):
            predecessor[h].next[h] = target.next[h]
            if predecessor[h] is self.head and predecessor[h].next[h] is self.tail:
                del self.head.next[max(1, h):]
                break

    def __iter__(self):
        """
        Iterator over the element in the skip-list.
        """
        element = self.head.next[0]
        while len(element.next) > 0:
            yield element
            element = element.next[0]

    def __len__(self):
        """
        Returns the number of unique elements in
        the skip-list.
        """
        return self.num_elements

    def _repr_level(self, l):
        """
        Represents the l-th level in the skip-list.
        """
        return " ".join([str(self.head.value)] #we step through all element at each level (for x in self --> calling __iter__(self)),
                    # if for current level l, current element's height less l, print out '-' * len(str(x.value))
                    # ex: if x.value = 1: print('-'), if x.value = 10: print('--'). print(x.value) otherwise.
                        + ["-" * len(str(x.value)) if l > len(x.next) - 1 else str(x.value) for x in self]
                        + [str(self.tail.value)])

    def __repr__(self):
        """
        Represents the skip-list.
        len(self.head.next) == height of Skip list
        """
        return "\n".join(self._repr_level(l) for l in range(len(self.head.next) - 1, -1, -1))


my_skip_list = SkipList()

for i in reversed(range(20)):
    my_skip_list.insert(random.randint(1, 1000))

print(my_skip_list)

"""
output:
-inf - -- 73 -- -- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- inf
-inf - -- 73 90 -- --- --- --- --- 456 --- --- --- 789 --- --- --- --- --- --- inf
-inf 8 -- 73 90 -- --- --- --- --- 456 --- --- --- 789 --- --- 856 --- --- 996 inf
-inf 8 -- 73 90 95 --- --- --- --- 456 --- --- --- 789 793 --- 856 --- --- 996 inf
-inf 8 12 73 90 95 --- --- --- 318 456 --- --- --- 789 793 835 856 --- --- 996 inf
-inf 8 12 73 90 95 274 283 293 318 456 521 683 695 789 793 835 856 991 994 996 inf
"""
