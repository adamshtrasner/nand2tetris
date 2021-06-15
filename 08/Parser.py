import os
import sys

READ_MODE = "r"
COMMAND_TYPES = {"pop": "C_POP", "push": "C_PUSH", "label": "C_LABEL", "goto": "C_GOTO",
                 "if-goto": "C_IF", "function": "C_FUNCTION", "return": "C_RETURN",
                 "call": "C_CALL", "add": "C_ARITHMETIC", "sub": "C_ARITHMETIC",
                 "neg": "C_ARITHMETIC", "eq": "C_ARITHMETIC", "gt": "C_ARITHMETIC",
                 "lt": "C_ARITHMETIC", "and": "C_ARITHMETIC", "or": "C_ARITHMETIC",
                 "not": "C_ARITHMETIC"}


class Parser:
    def __init__(self, file_name):
        self.file_name = file_name
        if self.file_name is not None:
            self.vm_file = self.constructor()
            self.cur_line = None
            self.next_line = self.vm_file.readline()
        else:
            self.vm_file = None

    def set_new_vm_file_name(self, new_vm):
        if self.vm_file is not None:
            self.close()
        self.file_name = new_vm
        self.vm_file = self.constructor()
        self.cur_line = None
        self.next_line = self.vm_file.readline()

    def constructor(self):
        return open(self.file_name, READ_MODE)

    def is_comment(self):
        return self.cur_line.startswith("/")

    def is_blank(self):
        return self.cur_line == "\n"

    def has_more_commands(self):
        if self.next_line:
            return True
        return False

    def advance(self):
        self.cur_line = self.next_line
        self.next_line = self.vm_file.readline()

    def args_list(self):
        """
        the function splits the line according to whitespace
        :return: returns a list of the arguments of the list
        """
        return self.cur_line.split()

    def command_type(self):
        return COMMAND_TYPES[self.args_list()[0]]

    def arg1(self):
        if self.command_type() == "C_ARITHMETIC":
            return self.cur_line
        return self.args_list()[1]

    def arg2(self):
        return self.args_list()[2]

    def close(self):
        self.vm_file.close()
