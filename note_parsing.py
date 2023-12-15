import re
class Note():
    def __init__(self, string: str):
        assert not "\n" in string
        self.string = string
        self.parse_note()

    def parse_note(self):
        self.get_formatting()
        if self.is_regexable:
            self.regexit()
        else:
            self.parsed = False

    def define_all_attributes(self, lst: list):
        assert len(lst) == 9
        self.type = lst[0]
        self.title = lst[1]
        self.note_text = lst[2]
        self.source_location = lst[3]
        self.tags = lst[4]
        self.notebooks = lst[5]
        self.study_set = lst[6]
        self.last_updated = lst[7]
        self.created = lst[8]
        self.parsed = True

    def get_formatting(self):
        self.get_is_regexable()

    def regexit(self):
        regexable = re.compile(r'^([^,]*),([^,]*),(.*),([^,]*),([^,]*),([^,]*),([^,]*),([^,]*),([^,]*)$')
        search_obj = re.search(regexable, self.string)
        self.define_all_attributes([search_obj.group(1),search_obj.group(2),search_obj.group(3),search_obj.group(4),search_obj.group(5),search_obj.group(6),search_obj.group(7),search_obj.group(8),search_obj.group(9)])

    def get_is_regexable(self):
        regexable = re.compile(r'^([^,]*),([^,]*),(.*),([^,]*),([^,]*),([^,]*),([^,]*),([^,]*),([^,]*)$')
        if re.search(regexable, self.string):
            self.is_regexable = True
        else:
            self.is_regexable = False

    def __add__(self, other):
        assert type(other) == Note
        new_string = self.string + other.string
        return Note(new_string)

    def __bool__(self):
        if self.string:
            return True
        else:
            False

    def __str__(self):
        return self.string

class NotePile():
    def __init__(self, notes: list|Note=[]):
        assert type(notes) == list or type(notes) == Note
        if type(notes) == list and self.verify_notes_lst(notes):
            self.pile = notes
        elif type(notes) == Note:
            self.pile = [notes]
        else:
            raise TypeError("argument must be either a list of Note objects or a single Note object")
        
    def verify_notes_lst(self, lst: list):
        """verifys that all objects in the list are Note objects or that the list is an empty list"""
        if not lst:
            return True
        for item in lst:
            if not type(item) == Note:
                return False
        return True
    
    def add_note(self, note):
        assert type(note) == Note
        self.pile.append(note)

    def cat_unparsed_notes(self):
        """takes all the notes in the pile that are unparsed and concatenates them,
        attempting to fix parsing issues. This works assuming that in the pile of notes,
        that subsequent notes will have the rest of the data needed to parse the Note object,
        which appears to be the case in this situation"""
        i = 0
        while i < len(self.pile):
            if not self.pile[i].parsed:
                if (self.pile[i] + self.pile[i+1]).parsed:
                    self.pile[i] = self.pile[i] + self.pile[i+1]
                    del(self.pile[i+1])
                elif self.pile[i+1].parsed:
                    pass
                else:
                    self.pile[i] = self.pile[i] + self.pile[i+1]
                    del(self.pile[i+1])
                    i -= 1
            i += 1

    def __str__(self):
        big = ""
        if not self.pile:
            return "This is an empty NotePile"
        for note in self.pile:
            big += str(note) + "|"
        return big