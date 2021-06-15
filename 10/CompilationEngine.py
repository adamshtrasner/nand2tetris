from JackTokenizer import JackTokenizer
import os
import sys

WRITE_MODE = "w"
OP = ["+", "-", "*", "/", "&", "|", "<", ">", "="]
UNARY_OP = ["-", "~"]
KEYWORD_CONSTANT = ["true", "false", "null", "this"]
SPECIAL_OP = ['<', '>', '&']


def special_op(op):
    if op == '<':
        return "&lt;"
    if op == '>':
        return "&gt;"
    if op == '&':
        return "&amp;"
    else:
        return op


class CompilationEngine:
    def __init__(self, input_name, output_name):
        self.tokenizer = JackTokenizer(input_name)
        self.output_file = open(output_name, WRITE_MODE)
        self.indent = "  "
        self.output_file.write("<class>\n")
        self.parentheses_mode = list()
        self.compile_class()

    def if_sub_call(self):
        # identify a subroutine call - (XXX.)XXX( .... )
        if '(' not in self.tokenizer.curr_token:
            return False
        if self.tokenizer.curr_token[0] == '(':
            return False
        return True

    def if_array(self):
        # Checking if current token is an array - XXX[ ..
        if self.get_length() <= 2 or self.tokenizer.curr_token[0].isdigit():
            return False
        if '[' not in self.tokenizer.curr_token:
            return False
        return True

    def handling_arrays(self):
        # This section handles partsing of varName[expression]
        tmp = self.tokenizer.curr_token
        self.tokenizer.curr_token = tmp[:tmp.index('[')]
        self.write_in_xml("identifier", False)
        self.tokenizer.curr_token = '['
        self.eat('[', False)
        self.tokenizer.curr_token = tmp[tmp.index('[') + 1:]
        self.compile_expression()
        tmp = self.tokenizer.curr_token
        self.tokenizer.curr_token = ']'
        if tmp[-1:] != ']':
            self.eat(']', False)
            self.tokenizer.curr_token = tmp[tmp.index(']') + 1:]
        else:
            self.eat(']')

    def compile_subroutine_call(self):
        try:
            self.parentheses_mode.append("sub")
            tmp = self.tokenizer.curr_token
            if '.' in tmp:
                self.tokenizer.curr_token = tmp[:tmp.index('.')]
                self.write_in_xml("identifier", False)
                self.tokenizer.curr_token = '.'
                self.eat(".", False)
                tmp = tmp[tmp.index('.') + 1:]
            if '(' in tmp:
                self.tokenizer.curr_token = tmp[:tmp.index('(')]
                self.write_in_xml("identifier", False)
                self.tokenizer.curr_token = '('
                self.write_in_xml("symbol", False)
                self.tokenizer.curr_token = tmp[tmp.index('(')+1:]
                self.compile_expression_list()
                self.tokenizer.curr_token = ')'
                self.eat(')', False)
                self.tokenizer.curr_token = ';'
            else:
                raise ValueError

        except ValueError:
            self.close()
            raise ValueError

    def get_length(self):
        return len(self.tokenizer.curr_token)

    def write(self, string):
        self.output_file.write(self.indent + string + "\n")

    def close(self):
        self.output_file.close()

    def write_in_xml(self, token_type, activate_advancing=True):
        if self.tokenizer.token_type() != token_type:
            print("Token type error")
            raise ValueError
        elif token_type in ["identifier", "symbol", "keyword", "integerConstant"]:
            self.write("<" + token_type + "> " + self.tokenizer.curr_token + " </" + token_type + ">")
        elif token_type == "stringConstant":
            tmp = self.tokenizer.curr_token[1:-1]
            self.write("<" + token_type + "> " + tmp + " </" + token_type + ">")

        if activate_advancing:
            try:
                self.tokenizer.has_more_tokens()
            except StopIteration:
                self.output_file.write("</class>")
                self.close()
                raise StopIteration

    def eat(self, string, flag=True):
        # we call this function only if we know for sure
        # that the string has to appear in the jack file
        if self.tokenizer.curr_token != string:
            print("Eat (token) error")
            raise ValueError
        else:
            self.write_in_xml(self.tokenizer.token_type(), flag)

    def compile_class(self):
        try:
            self.eat("class")
            self.write_in_xml("identifier")
            self.eat("{")
            while self.tokenizer.curr_token in ["field", "static"]:
                self.compile_class_var_dec()
            while self.tokenizer.curr_token in ["constructor", "function", "method"]:
                self.compile_subroutine_dec()
            self.eat("}")

        except StopIteration:
            self.close()

        except ValueError:
            self.close()
            raise ValueError

        self.close()

    def compile_class_var_dec(self):
        self.write("<classVarDec>")
        self.indent += "  "

        try:
            self.write_in_xml("keyword")
            self.compile_type()

            while self.tokenizer.curr_token[-1:] == ",":
                self.write("<identifier> " +
                        self.tokenizer.curr_token[:-1] + " </identifier>")
                self.write("<symbol> , </symbol>")
                self.tokenizer.has_more_tokens()
            if self.tokenizer.curr_token[-1:] == ";":
                self.write("<identifier> " +
                        self.tokenizer.curr_token[:self.get_length() - 1] + " </identifier>")
                self.write("<symbol> " + ";" + " </symbol>")
                self.tokenizer.has_more_tokens()
            else:
                raise ValueError

            self.indent = self.indent[:-2]
            self.write("</classVarDec>")

        except StopIteration:
            self.close()

        except ValueError:
            self.close()
            raise ValueError

    def compile_type(self, flag=True):
        if self.tokenizer.curr_token in ["int", "char", "boolean"]:
            self.write_in_xml("keyword", flag)
        elif self.tokenizer.token_type() == "identifier":
            self.write_in_xml("identifier", flag)
        else:
            raise ValueError

    def compile_subroutine_dec(self):
        self.write("<subroutineDec>")
        self.indent += "  "

        try:
            if self.tokenizer.curr_token in ["constructor", "function", "method"]:
                self.write_in_xml("keyword")
            if self.tokenizer.curr_token == "void":
                self.write_in_xml("keyword")
            else:
                self.compile_type()

            self.is_func_dec()
            self.tokenizer.has_more_tokens()
            self.compile_subroutine_body()

            self.indent = self.indent[:-2]
            self.write("</subroutineDec>")

        except StopIteration:
            self.close()

        except ValueError:
            self.close()
            raise ValueError

    def compile_subroutine_body(self):
        self.write("<subroutineBody>")
        self.indent += "  "

        try:
            self.eat("{")
            while self.tokenizer.curr_token == "var":
                self.compile_var_dec()
            self.compile_statements()
            self.eat("}")
            self.indent = self.indent[:-2]
            self.write("</subroutineBody>")

        except StopIteration:
            self.close()

        except ValueError:
            self.close()
            raise ValueError
        return

    def is_func_dec(self):
        # Checking if current token is - XXX(parameterList)
        tmp = list(self.tokenizer.curr_token)
        tmp_curr_token = self.tokenizer.curr_token
        self.tokenizer.curr_token = ""
        i = 0
        while i != len(tmp):
            if tmp[i] == "(":
                break
            self.tokenizer.curr_token += tmp[i]
            i += 1
        self.write_in_xml("identifier", False)
        self.tokenizer.curr_token = tmp[i]
        self.eat("(", False)
        i += 1
        self.tokenizer.curr_token = ""
        while i != len(tmp):
            if tmp[i] == ")":
                self.tokenizer.curr_token = tmp[i]
                break
            self.tokenizer.curr_token += tmp[i]
            i += 1

        self.compile_parameter_list()

        self.tokenizer.curr_token = self.tokenizer.curr_token[-1:]
        self.eat(")", False)
        self.tokenizer.curr_token = tmp_curr_token

    def compile_parameter_list(self):
        self.write("<parameterList>")
        self.indent += "  "

        try:
            if self.tokenizer.curr_token != ")":
                self.compile_type()
                tmp = self.tokenizer.curr_token
                self.tokenizer.curr_token = tmp[:-1]
                self.write_in_xml("identifier", False)
                self.tokenizer.curr_token = tmp
                while self.tokenizer.curr_token[-1:] != ")":
                    self.tokenizer.curr_token = tmp[-1:]
                    self.eat(",")
                    self.compile_type()
                    tmp = self.tokenizer.curr_token
                    self.tokenizer.curr_token = tmp[:-1]
                    self.write_in_xml("identifier", False)
                    self.tokenizer.curr_token = tmp

            self.indent = self.indent[:-2]
            self.write("</parameterList>")

        except ValueError:
            self.close()
            raise ValueError

    def compile_var_dec(self):
        self.write("<varDec>")
        self.indent += "  "
        try:
            self.eat("var")
            self.compile_type()
            while self.tokenizer.curr_token[-1:] == ",":
                self.tokenizer.curr_token = self.tokenizer.curr_token[:-1]
                self.write_in_xml("identifier", False)
                self.tokenizer.curr_token = ","
                self.write_in_xml("symbol", False)
                self.tokenizer.has_more_tokens()
            if self.tokenizer.curr_token[-1:] != ";":
                raise ValueError
            else:
                self.tokenizer.curr_token = self.tokenizer.curr_token[:-1]
                self.write_in_xml("identifier", False)
                self.tokenizer.curr_token = ";"
                self.write_in_xml("symbol", False)

            self.indent = self.indent[:-2]
            self.write("</varDec>")

            self.tokenizer.has_more_tokens()

        except ValueError:
            self.close()
            raise ValueError

    # Statements

    def compile_statements(self):
        self.write("<statements>")
        self.indent += "  "
        try:
            while self.tokenizer.curr_token in ["let", "do", "if", "while", "return;", "return"]:
                if self.tokenizer.curr_token == "let":
                    self.compile_let()
                elif self.tokenizer.curr_token == "do":
                    self.compile_do()
                elif self.tokenizer.curr_token == "if":
                    self.compile_if()
                elif self.tokenizer.curr_token == "while":
                    self.compile_while()
                else:
                    self.compile_return()

            self.indent = self.indent[:-2]
            self.write("</statements>")

        except ValueError:
            self.close()
            raise ValueError

    def compile_do(self):
        self.write("<doStatement>")
        self.indent += "  "
        try:
            self.eat("do")
            self.compile_subroutine_call()
            self.eat(";")

            self.indent = self.indent[:-2]
            self.write("</doStatement>")

        except ValueError:
            self.close()
            raise ValueError

    def compile_let(self):
        self.write("<letStatement>")
        self.indent += "  "
        try:
            self.eat("let")
            if self.if_array():
                self.handling_arrays()
            else:
                self.write_in_xml("identifier")

            self.eat("=")
            self.compile_expression()
            self.tokenizer.curr_token = ';'
            self.eat(';')

            self.indent = self.indent[:-2]
            self.write("</letStatement>")

        except ValueError:
            self.close()
            raise ValueError
        return

    def compile_if(self):
        self.write("<ifStatement>")
        self.indent += "  "
        try:
            self.parentheses_mode.append("if_or_while")
            self.eat("if")
            tmp = self.tokenizer.curr_token
            self.tokenizer.curr_token = tmp[0]
            self.eat("(", False)
            self.tokenizer.curr_token = tmp[1:]
            self.compile_expression()
            self.eat(")")
            self.eat("{")
            self.compile_statements()
            self.eat("}")
            if self.tokenizer.curr_token == "else":
                self.eat("else")
                self.eat("{")
                self.compile_statements()
                self.eat("}")

            self.indent = self.indent[:-2]
            self.write("</ifStatement>")
        except ValueError:
            raise ValueError
        return

    def compile_while(self):
        self.write("<whileStatement>")
        self.indent += "  "
        try:
            self.parentheses_mode.append("if_or_while")
            self.eat("while")
            tmp = self.tokenizer.curr_token
            self.tokenizer.curr_token = tmp[0]
            self.eat("(", False)
            self.tokenizer.curr_token = tmp[1:]
            self.compile_expression()
            self.eat(")")
            self.eat("{")
            self.compile_statements()
            self.eat("}")

            self.indent = self.indent[:-2]
            self.write("</whileStatement>")
        except ValueError:
            raise ValueError

    def compile_return(self):
        self.write("<returnStatement>")
        self.indent += "  "
        try:
            tmp = self.tokenizer.curr_token
            if tmp[-1:] == ";":
                self.tokenizer.curr_token = tmp[:-1]
                self.eat("return", False)
                self.tokenizer.curr_token = ';'
                self.eat(";")
            else:
                self.eat("return")
                self.compile_expression()
                self.tokenizer.curr_token = ';'
                self.eat(";")

            self.indent = self.indent[:-2]
            self.write("</returnStatement>")

        except ValueError:
            self.close()
            raise ValueError

    # Handling expressions
    def compile_expression_list(self):
        self.write("<expressionList>")
        self.indent += "  "
        try:
            if self.tokenizer.curr_token != ");":
                while self.tokenizer.curr_token[0] != ')':
                    self.compile_expression()
                    if self.tokenizer.curr_token == ',':
                        self.write_in_xml("symbol")
            else:
                tmp = self.tokenizer.curr_token
                self.tokenizer.curr_token = tmp[0]

            self.indent = self.indent[:-2]
            self.write("</expressionList>")

        except ValueError:
            self.close()
            raise ValueError

    def handle_closure(self):
        tmp = self.tokenizer.curr_token
        if len(tmp) == 1:
            # token = ')'
            self.tokenizer.curr_token = ')'
        else:
            self.tokenizer.curr_token = tmp[tmp.index(')'):]

    def handle_string_term(self):
        string = ""
        self.tokenizer.curr_token = self.tokenizer.curr_token[1:]
        while '"' not in self.tokenizer.curr_token:
            string = string + self.tokenizer.curr_token + " "
            self.tokenizer.has_more_tokens()
        if ')' or ';' in self.tokenizer.curr_token:
            string = string + self.tokenizer.curr_token[:self.tokenizer.curr_token.index('"')]
            tmp = self.tokenizer.curr_token[
                                        self.tokenizer.curr_token.index('"') + 1:]
            self.write("<stringConstant> " + string + " </stringConstant>")
            self.tokenizer.curr_token = tmp
        else:
            string = string + self.tokenizer.curr_token[:-1]

    def compile_term(self):
        self.write("<term>")
        self.indent += "  "
        try:
            # Handling term = varName[expression]
            tmp = self.tokenizer.curr_token
            if self.tokenizer.curr_token[0] in UNARY_OP:
                self.tokenizer.curr_token = tmp[0]
                self.write_in_xml("symbol", False)
                self.tokenizer.curr_token = tmp[1:]
                self.compile_term()
            elif self.tokenizer.curr_token[0] == '"':
                self.handle_string_term()
            elif self.if_array():
                self.handling_arrays()
            elif self.if_sub_call():
                self.compile_subroutine_call()
            elif ']' in self.tokenizer.curr_token:
                self.tokenizer.curr_token = tmp[:tmp.index(']')]
                self.write_in_xml(self.tokenizer.token_type(), False)
                self.tokenizer.curr_token = tmp
            # Handling term = (expression)
            elif self.tokenizer.curr_token[0] == '(':
                self.parentheses_mode.append("exp")
                self.tokenizer.curr_token = '('
                self.eat('(', False)
                self.tokenizer.curr_token = tmp[tmp.index('(') + 1:]
                self.compile_expression()
                tmp = self.tokenizer.curr_token
                self.tokenizer.curr_token = ')'
                if tmp == ')':
                    self.eat(')')
                else:
                    self.eat(')', False)
            elif ')' in self.tokenizer.curr_token:
                mode = self.parentheses_mode.pop()
                if mode == "exp":
                    if tmp[0] == ')':
                        self.handle_closure()
                    else:
                        self.tokenizer.curr_token = tmp[:tmp.index(')')]
                        self.write_in_xml(self.tokenizer.token_type(), False)
                        if tmp.index(')') == len(tmp) - 1:
                            self.tokenizer.curr_token = ')'
                        else:
                            self.tokenizer.curr_token = tmp[tmp.index(')'):]
                            # now tmp[0] == ')' again
                            self.handle_closure()
                elif mode == "sub":
                    if tmp[0] == ')':
                        self.handle_closure()
                    else:
                        self.tokenizer.curr_token = tmp[:tmp.index(')')]
                        self.write_in_xml(self.tokenizer.token_type(), False)
                        if tmp.index(')') == len(tmp) - 1:
                            self.tokenizer.curr_token = ')'
                        else:
                            self.tokenizer.curr_token = tmp[tmp.index(')') + 1:]
                            self.handle_closure()
                else:
                    if tmp[0] == ')':
                        self.tokenizer.curr_token = ')'
                    else:
                        self.tokenizer.curr_token = tmp[:tmp.index(')')]
                        self.write_in_xml(self.tokenizer.token_type(), False)
                        self.tokenizer.curr_token = ')'

            elif self.tokenizer.curr_token[-1:] == ',':
                self.tokenizer.curr_token = tmp[:-1]
                self.write_in_xml(self.tokenizer.token_type(), False)
                self.tokenizer.curr_token = ','
            elif self.tokenizer.curr_token[-1:] == ',':
                self.tokenizer.curr_token = tmp[:-1]
                self.write_in_xml(self.tokenizer.token_type(), False)
                self.tokenizer.curr_token = tmp
            else:
                flag = True
                if self.tokenizer.curr_token[-1:] == ';':
                    flag = False
                    self.tokenizer.curr_token = tmp[:-1]
                self.write_in_xml(self.tokenizer.token_type(), flag)

            self.indent = self.indent[:-2]
            self.write("</term>")

        except ValueError:
            self.close()
            raise ValueError

    def compile_expression(self):
        # TODO: Later on. first, test without this function.
        self.write("<expression>")
        self.indent += "  "
        try:
            self.compile_term()
            while self.tokenizer.curr_token in OP:
                self.write("<symbol> " + special_op(self.tokenizer.curr_token) + " </symbol>")
                self.tokenizer.has_more_tokens()
                self.compile_term()

            self.indent = self.indent[:-2]
            self.write("</expression>")

        except ValueError:
            self.close()
            raise ValueError


if __name__ == '__main__':
    directory = sys.argv[1]
    if ".jack" not in directory:
        # if the file given is a folder which contains asm files,
        # then iterate through the asm files in the folder
        entries = os.listdir(directory)
        print(directory)
        for entry in entries:
            xml_file_name = directory + "/" + entry[:-4] + "xml"
            CompilationEngine(directory + "/" + entry, xml_file_name)
    else:
        # the file given is a single asm file
        xml_file_name = directory[:-4] + "xml"
        CompilationEngine(directory, xml_file_name)
