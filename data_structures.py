from heapq import heappop, heappush  # Import priority queue operations

'''
#######################################################################################
# GROUP A Skill: Stacks - user defined stack class                                    #                                
#                                                                                     #
# The Game and UI classes both use a user defined class                               #
# called Stack that is an implementation of the stack data structure.                 #
# The stack is used to store the order that moves are played,                         #
# so when the undo operation is used, the item at the top of the stack is popped off. #
#######################################################################################
'''
class Stack:  # Stack data structure
    def __init__(self):  # constructor
        self.__array = []

    def push(self, val):  # push item to stack
        self.__array.append(val)

    def pop(self):  # pop item to stack, return -1 if stack empty
        if not self.is_empty():
            return self.__array.pop(-1)
        else:
            return -1

    def peek(self):  # peek top item of stack, return -1 if stack empty
        if not self.is_empty():
            return self.__array[-1]
        else:
            return -1

    def is_empty(self):  # empty check
        return not self.__array

'''
##########################################################################
# GROUP A Skill: Queues - user defined priority queue class              #
#                                                                        #
# The group colouring algorithm uses a normal queue and a priority       #
# queue to carry out breadth first search to colour in nodes of a graph. #
# The priority queue is used to ensure that nodes with the               #
# most coloured neighbours are coloured first.                           #
##########################################################################
'''
class PriorityQueue:  # Priority queue data structure
    def __init__(self, initial_item=None):  # Constructor
        if initial_item is not None:
            self.__queue = [initial_item]

    def enqueue(self, item):  # Enqueue method
        heappush(self.__queue, item)

    def dequeue(self):  # Dequeue method
        return heappop(self.__queue)

    def is_empty(self):  # Is empty method
        return len(self.__queue) == 0

    def __repr__(self):  # Used for printing queue contents during debug
        return str(self.__queue)
