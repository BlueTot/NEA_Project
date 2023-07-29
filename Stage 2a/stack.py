class Stack:
    def __init__(self):
        self.__array = []
    
    def push(self, val):
        self.__array.append(val)
    
    def pop(self):
        if not self.is_empty():
            return self.__array.pop(-1)
        else:
            return -1
        
    def peek(self):
        if not self.is_empty():
            return self.__array[-1]
        else:
            return -1
    
    def is_empty(self):
        return not self.__array