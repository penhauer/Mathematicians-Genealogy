

class Mathmatician:

    def __init__(self, *, identifier=None, first_name=None, last_name=None, full_name=None, university=None):
        self.identifier = identifier
        self.first_name = first_name
        self.last_name = last_name
        self.full_name = full_name
        self.university = university

    def __lt__(self, mat):
        if mat.last_name != self.last_name:
            return self.first_name < mat.first_name
        return self.last_name < mat.last_name
    
    def __str__(self):
        return f"{self.full_name}\t\t{self.university}"
