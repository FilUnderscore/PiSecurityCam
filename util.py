### Comma Separated String Builder
class CSSBuilder:
    values = 0
    str = ""

    def add_entry(self, value):
        if self.values == 0:
            self.str = value
        else:
            self.str += ", " + value

        self.values += 1
        return self
    
    def extend_entry(self, extension):
        self.str += " " + extension
        return self

    def build(self):
        return self.str