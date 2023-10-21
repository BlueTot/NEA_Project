from abc import ABC # importing abstract base class

class BoardAction(ABC):
    def __init__(self, row, col):
        self._row = row
        self._col = col
    
    @property
    def row(self):
        return self._row
    
    @property
    def col(self):
        return self._col
    
    def reverse(self):
        raise NotImplementedError

class SetNumAction(BoardAction):
    def __init__(self, row, col, orig_num, new_num):
        super().__init__(row, col)
        self._orig_num = orig_num
        self._new_num = new_num
    
    @property
    def orig_num(self):
        return self._orig_num
    
    @property
    def new_num(self):
        return self._new_num
    
    def reverse(self):
        return SetNumAction(self._row, self._col, self._new_num, self._orig_num)
    
class EditNoteAction(BoardAction):
    def __init__(self, row, col, num):
        super().__init__(row, col)
        self._num = num
    
    @property
    def num(self):
        return self._num
    
    def reverse(self):
        return EditNoteAction(self._row, self._col, self._num)

class SetNoteAction(BoardAction):
    def __init__(self, row, col, orig_note, new_note):
        super().__init__(row, col)
        self._orig_note = orig_note
        self._new_note = new_note
    
    @property
    def orig_note(self):
        return self._orig_note
    
    @property
    def new_note(self):
        return self._new_note
    
    def reverse(self):
        return SetNoteAction(self._row, self._col, self._new_note, self._orig_note)