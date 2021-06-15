import re
import itertools
READ_MODE = "r"


class JackTokenizer:

    INLINE_COMMENT = re.compile(r'//.*\n')
    MULTILINE_COMMENT = re.compile(r'/\*.*?\*/', flags=re.S)

    TERMINAL_ELEMENTS_LIST = ['keyword', 'symbol', 'integerConstant', 'stringConstant',
                              'identifier']

    INT_CONST = r'(\d+)'
    STRING_CONST = r'\"([^\n]*)\"'

    SYMBOL = r'([{}()[\].,;+\-*/&|<>=~])'
    IDENTIFIER = r'([A-Za-z_]\w*)'
    KEYWORD = r'(class|constructor|function|method|field|static|var|' \
              'void|char|int|boolean|true|false|null|this|let|do|if|else|while|return)'

    TERMINAL_ELEMENTS = '{}|{}|{}|{}|{}'.format(KEYWORD, SYMBOL, INT_CONST,
                                                STRING_CONST, IDENTIFIER)
    TERMINAL_ELEMENTS_COMPILED = re.compile(TERMINAL_ELEMENTS)

    def __init__(self, file_name):
        self.open_jack_file = open(file_name, READ_MODE)
        self.jack_file = self.open_jack_file.read()
        self.tokens = self.tokenize()
        self.next = self.tokens.pop(0)
        self.curr_token = None

    def ignore_comments(self):
        without_multiline = re.sub(self.MULTILINE_COMMENT, ' ', self.jack_file)
        without_inline = re.sub(self.INLINE_COMMENT, '\n', without_multiline)
        return without_inline

    def tokenize(self):
        ignore_comments = self.ignore_comments()
        matches = self.TERMINAL_ELEMENTS_COMPILED.findall(ignore_comments)
        match_types = map(lambda element_matches: self.TERMINAL_ELEMENTS_LIST[
            next(index for index, element in enumerate(element_matches) if element)], matches)
        flat_matches = list(itertools.chain(*matches))
        tokens = [match for match in flat_matches if match]
        return list(zip(tokens, match_types))

    def peek(self):
        return self.next

    def has_more_tokens(self):
        return self.next

    def advance(self):
        self.curr_token = self.next

        if len(self.tokens) != 0:
            self.next = self.tokens.pop(0)
        else:
            self.next = False

    def token(self):
        return self.curr_token[0]

    def token_type(self):
        return self.curr_token[1]

    def close(self):
        self.open_jack_file.close()