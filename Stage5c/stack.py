class Stack: # stack class
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