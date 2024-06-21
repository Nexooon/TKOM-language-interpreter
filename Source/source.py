from .source_position import SourcePosition


class SourceReader:
    def __init__(self, source):
        self.source = source

        self.current_position = SourcePosition(1, 1)
        self.current_char = ""
        self.next_char()

    def next_char(self):
        if self.current_char == "\n":
            self.current_position = self.current_position.next_line()
        elif self.current_char:
            self.current_position = self.current_position.advance()

        char = self.source.read(1)

        if not char:
            self.current_char = chr(3)
        else:
            self.current_char = char

    def get_char(self):
        return self.current_char

    def get_position(self):
        return self.current_position
