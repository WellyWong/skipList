# Skip List
Skip list is a data structure used to store sorted list of items, very much like Binary Search Tree.

The main advantage of using Skip list over BST is that it is best suited for concurrent access.

One of the most common implementations of BST is Red Black Tree. The problem of accessing this tree concurrently
comes when a data element has been modified and tree needs to re-balance, which would require mutex lock on
large part of tree. 

On the other hand, when inserting/deleting/updating a node in a Skip list,
only nodes directly connected to the affected nodes needs locking.

#Skip Lists: A probabilistic alternative to Balanced Trees:
https://15721.courses.cs.cmu.edu/spring2018/papers/08-oltpindexes1/pugh-skiplists-cacm1990.pdf

Code from: https://github.com/jhomswk/Skip_List/blob/master/skip_list.py
