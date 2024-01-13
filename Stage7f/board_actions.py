from abc import ABC # importing abstract base class

class BoardAction(ABC): # Base BoardAction class

    def __init__(self, row, col): # Constructor (takes row, col : ints)
        self._row = row # Set row
        self._col = col # Set col
    
    '''Getters'''
    
    @property
    def row(self): # Gets row
        return self._row
    
    @property
    def col(self): # Gets col
        return self._col
    
    '''Reverse method'''
    
    def reverse(self): # Abstract reverse method, must be implemented by children classes
        raise NotImplementedError

class SetNumAction(BoardAction): # Set Num Action class, inherits from BoardAction class

    def __init__(self, row, col, orig_num, new_num): # Constructor (takes row, col, orig_num, new_num : ints)
        super().__init__(row, col)
        self._orig_num = orig_num # Set original number
        self._new_num = new_num # Set new number
    
    '''Getters'''

    @property
    def orig_num(self): # Gets orig num (before action)
        return self._orig_num
    
    @property
    def new_num(self): # Gets new num (after action)
        return self._new_num
    
    '''Reverse method'''
    
    def reverse(self): # Reverse method so action can be applied in reverse (undo)
        return SetNumAction(self._row, self._col, self._new_num, self._orig_num)
    
class EditNoteAction(BoardAction): # Edit Note Action (inherits from BoardAction class)

    def __init__(self, row, col, num): # Constructor (takes row, col, num : ints)
        super().__init__(row, col)
        self._num = num # Set number to add/remove
    
    '''Getters'''

    @property
    def num(self): # Gets num
        return self._num
    
    '''Reverse method'''
    
    def reverse(self): # Reverse method so action can be applied in reverse (undo)
        return EditNoteAction(self._row, self._col, self._num)

class SetNoteAction(BoardAction): # Set Note Action (inherits from BoardAction class)

    def __init__(self, row, col, orig_note, new_note): # Constructor (takes row, col, orig note, new note : int)
        super().__init__(row, col)
        self._orig_note = orig_note # Original note (list)
        self._new_note = new_note # New note (list)
    
    '''Getters'''
    
    @property
    def orig_note(self): # Gets original note (before action)
        return self._orig_note
    
    @property
    def new_note(self): # Gets new note (after action)
        return self._new_note

    '''Reverse method'''
    
    def reverse(self): # Reverse method so action can be applied in reverse (undo)
        return SetNoteAction(self._row, self._col, self._new_note, self._orig_note)
    