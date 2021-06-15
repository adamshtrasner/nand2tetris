READ_MODE = "r"

KEYWORD = ["class", "constructor", "function", "method", "field", "static", "var",
           "int", "char", "boolean", "void", "true", "false", "null", "this", "let",
           "do", "if", "else", "while", "return"]

SYMBOL = ["{", "}", "(", ")", "[", "]", "-", ",", ";", '.', '+', "-", "*", "/", "&", "|",
          "<", ">", "=", "~"]

COMMENTS = ["//", "/**", "*", "*/"]

# INT_CONST = a digit number in the range 0 .. 32767

# STRING_CONST = "___ ... _ " where inside  the ' " ' theres a sequence of Unicode
# characters not including double quote or newline

# IDENTIFIER = a sequence of letters, digits, and underscore ('_') not starting
# with a digit


class JackTokenizer:
    def __init__(self, file_name):
        self.jack_file = open(file_name, READ_MODE)

        self.lines = self.jack_file.readlines()
        self.k = 0  # index for lines list

        self.curr_token = None

        self.line = None
        self.i = 0  # index for a line list

        self.advance_line_()
        self.advance()

    def advance_line_(self):
        if self.k == len(self.lines):
            raise StopIteration
        else:
            self.line = self.lines[self.k].split()
            self.k += 1
            self.fix_line_()

    def fix_line_(self):
        if not self.line:
            try:
                self.advance_line_()
            except StopIteration:
                raise StopIteration

        if self.line[0] in COMMENTS:  # if line starts with a comment
            try:
                self.advance_line_()
            except StopIteration:
                raise StopIteration

        if "//" in self.line:  # Comments will not be read
            del self.line[self.line.index("//"):]

    def has_more_tokens(self):
        if self.i == len(self.line):
            try:
                self.advance_line_()
            except StopIteration:
                raise StopIteration
            else:
                self.i = 0
                self.advance()
        else:
            self.advance()

    def advance(self):
        self.curr_token = self.line[self.i]
        self.i += 1

    def token_type(self):
        if self.curr_token in KEYWORD:
            return "keyword"

        if self.curr_token in SYMBOL:
            return "symbol"

        if self.curr_token.isdigit():
            if 0 <= int(self.curr_token) <= 32767:
                return "integerConstant"
            else:
                raise ValueError

        if self.curr_token[0] == '"':
            if "\n" not in self.curr_token[1:len(self.curr_token) - 1]:
                return "stringConstant"

        if self.curr_token[0].isdigit():
            raise ValueError
        else:
            return "identifier"
