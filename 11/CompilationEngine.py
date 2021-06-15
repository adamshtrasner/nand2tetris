from JackTokenizer import JackTokenizer
from SymbolTable import SymbolTable
from VMWriter import VMWriter

WRITE_MODE = "w"
KEYWORD_CONSTANT = ["true", "false", "null", "this"]


class CompilationEngine:

    STATIC = "static"
    THIS = "field"
    ARG = "argument"
    LCL = "var"

    STRING = 'stringConstant'
    INTEGER = 'integerConstant'

    OP = {"+": "add", "-": "sub", "=": "eq",
          "<": "lt", ">": "gt", "&": "and", "|": "or"}
    UNARY_OP = {"-": "neg", "~": "not"}
    MATH_OP = {"*": "Math.multiply", "/": "Math.divide"}

    def __init__(self, input_name, output_name):
        self.tokenizer = JackTokenizer(input_name)
        self.output_file = open(output_name, WRITE_MODE)
        # extended
        self.table = SymbolTable()
        self.vm_writer = VMWriter(self.output_file)
        self.labels = {"while": 0, "if": 0}
        self.class_name = None
        # --------
        self.compile_class()
        self.close()

    # -------- Methods of my own --------
    def fix_bug_identifier(self):
        # this method is for fixing a bug I found in the tokenizer:
        # each time an identifier starts with a keyword, my tokenizer splits it to two.
        # for example: var bool if_true - my tokenizer splits 'if_true' to:
        # 'if' - keyword, and '_true' - identifier, instead of 'if_true' - identifier.
        new_token = self.get_token()
        if self.tokenizer.token_type() == "keyword":
            new_token += self.get_token()
        return new_token

    def is_variable(self, name):
        if name[0].isupper():
            return False
        return True

    def if_sub_call(self):
        if self.tokenizer.tokens[0][0] in ['.', '(']:
            return True
        return False

    def if_array(self):
        # Checking if current token is an array - XXX[ ..
        if self.tokenizer.peek()[0] == "[":
            return True
        return False

    def compile_subroutine_call(self):
        n_args = 0
        subroutine_name = self.fix_bug_identifier()  # subroutineName|className|varName

        if self.tokenizer.peek()[0] == '.':

            if self.is_variable(subroutine_name):  # varName.subroutine(..)
                self.vm_writer.write_push(self.table.kind_of(subroutine_name),
                                          self.table.index_of(subroutine_name))
                n_args += 1
                subroutine_name = self.table.type_of(subroutine_name)

            subroutine_name = subroutine_name + self.get_token()  # .
            subroutine_name = subroutine_name + self.fix_bug_identifier()  # subroutineName

        if '.' not in subroutine_name:  # subroutine is a self method
            subroutine_name = "{}.{}".format(self.class_name, subroutine_name)
            self.vm_writer.write_push("pointer", 0)
            n_args += 1

        self.get_token()  # (
        n_args = self.compile_expression_list(n_args)  # expressionList
        self.get_token()  # )

        self.vm_writer.write_call(subroutine_name, n_args)

    def close(self):
        self.vm_writer.close()
        self.tokenizer.close()

    def get_token(self):
        if self.tokenizer.has_more_tokens():
            self.tokenizer.advance()
        return self.tokenizer.token()

    # -------- The API starts here --------

    def compile_class(self):
        self.get_token()  # class
        self.class_name = self.fix_bug_identifier()  # className
        # --------
        self.get_token()  # {
        while self.tokenizer.peek()[0] in ["field", "static"]:  # classVarDec*
            self.compile_class_var_dec()
        while self.tokenizer.peek()[0] in ["constructor", "function", "method"]:  # subroutineDec*
            self.table.start_subroutine()
            self.compile_subroutine_dec()
        self.get_token()  # }

    def compile_class_var_dec(self):
        _kind = self.get_token()  # static|field
        _type = self.get_token()  # type
        _name = self.fix_bug_identifier()  # varName

        self.table.define(_name, _type, _kind)

        while self.tokenizer.peek()[0] == ",":  # (, varName)*
            self.get_token()  # ,
            _name = self.fix_bug_identifier()
            self.table.define(_name, _type, _kind)

        self.get_token()  # ;

    def compile_subroutine_dec(self):
        subroutine_type = self.get_token()  # constructor|function|method
        self.get_token()  # void|type
        subroutine_name = "{}.{}".format(self.class_name, self.fix_bug_identifier())  # subroutineName

        self.get_token()  # (

        if subroutine_type == "method":
            self.table.define("this", self.class_name, self.ARG)

        self.compile_parameter_list()

        self.get_token()  # )
        self.compile_subroutine_body(subroutine_name, subroutine_type)

    def compile_subroutine_body(self, subroutine_name, subroutine_type):
        self.get_token()  # {

        while self.tokenizer.peek()[0] == "var":  # varDec*
            # local variables
            self.compile_var_dec()

        # function subroutine_name n_locals
        self.vm_writer.write_function(subroutine_name, self.table.var_count(self.LCL))

        if subroutine_type == "constructor":
            self.vm_writer.write_malloc_for_constructor(self.table.var_count(self.THIS))
        elif subroutine_type == "method":
            # push argument 0
            # pop pointer 0
            self.vm_writer.write_push(self.ARG, 0)
            self.vm_writer.write_pop("pointer", 0)

        self.compile_statements()  # statements

        self.get_token()  # }

    def compile_parameter_list(self):
        if self.tokenizer.peek()[0] != ")":
            _kind = self.ARG
            _type = self.get_token()  # type
            _name = self.fix_bug_identifier()  # varName
            self.table.define(_name, _type, _kind)
            while self.tokenizer.peek()[0] == ",":
                self.get_token()  # ,
                _type = self.get_token()  # type
                _name = self.fix_bug_identifier()  # varName
                self.table.define(_name, _type, _kind)

    def compile_var_dec(self):
        _kind = self.get_token()  # var
        _type = self.get_token()  # type
        _name = self.fix_bug_identifier()  # varName

        self.table.define(_name, _type, _kind)

        while self.tokenizer.peek()[0] == ",":
            self.get_token()  # ,
            _name = self.fix_bug_identifier()  # varName
            self.table.define(_name, _type, _kind)

        self.get_token()  # ;

    # Statements

    def compile_statements(self):

        while self.tokenizer.peek()[0] in ["let", "do", "if", "while", "return;", "return"]:
            if self.tokenizer.peek()[0] == "let":
                self.compile_let()
            elif self.tokenizer.peek()[0] == "do":
                self.compile_do()
            elif self.tokenizer.peek()[0] == "if":
                self.compile_if()
            elif self.tokenizer.peek()[0] == "while":
                self.compile_while()
            else:
                self.compile_return()

    def compile_do(self):
        self.get_token()  # do
        self.compile_subroutine_call()  # subroutineCall
        self.get_token()  # ;

        # because the functions after "do" are void
        # pop temp 0
        self.vm_writer.write_pop("temp", 0)

    def compile_let(self):
        self.get_token()  # let
        _name = self.fix_bug_identifier()  # varName
        if_array = False
        if self.if_array():

            if_array = True
            self.vm_writer.write_push(self.table.kind_of(_name), self.table.index_of(_name))

            self.get_token()  # [
            self.compile_expression()  # expression
            self.get_token()  # ]

            self.vm_writer.write_arithmetic("add")

        self.get_token()  # =
        self.compile_expression()  # expression
        if if_array:
            self.vm_writer.write_pop("temp", 0)  # pop temp 0
            self.vm_writer.write_pop("pointer", 1)  # pop pointer 1
            self.vm_writer.write_push("temp", 0)  # push temp 0
            self.vm_writer.write_pop("that", 0)  # pop that 0
        else:
            self.vm_writer.write_pop(self.table.kind_of(_name), self.table.index_of(_name))
        self.get_token()  # ;

    def compile_if(self):
        l1 = "IF_TRUE{}".format(self.labels["if"])
        l2 = "IF_FALSE{}".format(self.labels["if"])
        self.get_token()  # if
        self.get_token()  # (
        self.compile_expression()
        self.vm_writer.write_arithmetic("not")  # change to neg if necessary
        self.vm_writer.write_if(l1)
        self.get_token()  # )
        self.get_token()  # {
        self.compile_statements()
        self.get_token()  # }
        self.vm_writer.write_goto(l2)
        self.vm_writer.write_label(l1)
        if self.tokenizer.peek()[0] == "else":
            self.get_token()  # else
            self.get_token()  # {
            self.compile_statements()
            self.get_token()  # }
        self.vm_writer.write_label(l2)
        self.labels["if"] += 1

    def compile_while(self):
        l1 = "WHILE_TRUE{}".format(self.labels["while"])
        l2 = "WHILE_END{}".format(self.labels["while"])
        self.vm_writer.write_label(l1)
        self.get_token()  # while
        self.get_token()  # (
        self.compile_expression()
        self.get_token()  # )
        self.vm_writer.write_arithmetic("not")
        self.vm_writer.write_if(l2)
        self.get_token()  # {
        self.compile_statements()
        self.get_token()  # }
        self.vm_writer.write_goto(l1)
        self.vm_writer.write_label(l2)
        self.labels["while"] += 1

    def compile_return(self):
        self.get_token()  # return
        if self.tokenizer.peek()[0] != ';':
            self.compile_expression()

        else:
            # push constant 0
            self.vm_writer.write_int(0)

        self.vm_writer.write_return()

        self.get_token()  # ;

    # Handling expressions
    def compile_expression_list(self, n_args):
        if self.tokenizer.peek()[0] != ')':
            self.compile_expression()  # expression
            n_args += 1
            while self.tokenizer.peek()[0] != ')':
                self.get_token()  # ,
                self.compile_expression()
                n_args += 1

        return n_args

    def compile_term(self):
        if self.tokenizer.peek()[0] in self.UNARY_OP:  # unrayOp term
            command = self.get_token()
            self.compile_term()
            self.vm_writer.write_arithmetic(self.UNARY_OP[command])
        elif self.tokenizer.peek()[0] == '(':  # ( expression )
            self.get_token()  # (
            self.compile_expression()
            self.get_token()  # )
        elif self.tokenizer.tokens[0][0] == '[':
            _name = self.get_token()  # varName
            self.vm_writer.write_push(self.table.kind_of(_name), self.table.index_of(_name))

            self.get_token()  # [
            self.compile_expression()
            self.get_token()  # ]

            self.vm_writer.write_arithmetic("add")

            self.vm_writer.write_pop("pointer", 1)
            self.vm_writer.write_push("that", 0)

        elif self.if_sub_call():
            self.compile_subroutine_call()
        else:
            token = self.get_token()  # integerConst|stringConst|keywordConst|varName
            if self.tokenizer.token_type() == self.INTEGER:
                self.vm_writer.write_int(token)
            elif self.tokenizer.token_type() == self.STRING:
                self.vm_writer.write_string(token)
            elif self.tokenizer.token_type() == 'keyword':
                if token == 'this':
                    self.vm_writer.write_push("pointer", 0)
                elif token == 'true':
                    self.vm_writer.write_int(1)
                    self.vm_writer.write_arithmetic("neg")
                elif token in ['false', 'null']:
                    self.vm_writer.write_int(0)
            else:
                self.vm_writer.write_push(self.table.kind_of(token), self.table.index_of(token))

    def compile_expression(self):
        self.compile_term()  # term
        while self.tokenizer.peek()[0] in self.OP or self.tokenizer.peek()[0] in self.MATH_OP:
            op = self.get_token()  # op
            self.compile_term()  # term
            if op in self.OP:
                self.vm_writer.write_arithmetic(self.OP[op])
            else:
                self.vm_writer.write_call(self.MATH_OP[op], 2)
