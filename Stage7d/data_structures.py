from heapq import heappop, heappush

class Stack: # Stack data structure
    def __init__(self): # constructor
        self.__array = []
    
    def push(self, val): # push item to stack
        self.__array.append(val)
    
    def pop(self): # pop item to stack, return -1 if stack empty
        if not self.is_empty():
            return self.__array.pop(-1)
        else:
            return -1
        
    def peek(self): # peek top item of stack, return -1 if stack empty
        if not self.is_empty():
            return self.__array[-1]
        else:
            return -1
    
    def is_empty(self): # empty check
        return not self.__array

class PriorityQueue: # Priority queue data structure
    def __init__(self, initial_item=None): # Constructor
        if initial_item is not None:
            self.__queue = [initial_item]
    
    def enqueue(self, item): # Enqueue method
        heappush(self.__queue, item)
    
    def dequeue(self): # Dequeue method
        return heappop(self.__queue)

    def is_empty(self): # Is empty method
        return len(self.__queue) == 0

    def __repr__(self): # Used for printing queue contents during debug
        return str(self.__queue)