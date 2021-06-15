import os
import sys
from Parser import Parser
from CodeWriter import CodeWriter

# Things to handle:
# 1. handle overflow - there's a problem in gl and lt,
#    when numbers are big, and checking whether x-y<0 (or x-y>0)
#    doesn't give the right jump.

# 2. pass the tests for this project, and then move on to project 8!!


class VMTranslator:
    def __init__(self, input_vm_file_name, output_asm_file_name):
        self.input_vm_file_name = input_vm_file_name
        if self.input_vm_file_name is not None:
            self.parser = Parser(self.input_vm_file_name)
        else:
            self.parser = None
        self.output_asm_file_name = output_asm_file_name
        self.code_writer = CodeWriter(self.output_asm_file_name)

    def set_new_vm_file(self, new_vm):
        """
        :param new_vm: the next vm file
        sets the new files to translate
        """
        self.code_writer.set_vm_file_name(new_vm)

        if self.parser is not None:
            self.parser.close()

        self.input_vm_file_name = new_vm

        if self.parser is not None:
            self.parser.set_new_vm_file_name(self.input_vm_file_name)
        else:
            self.parser = Parser(self.input_vm_file_name)

    def translate(self):
        while self.parser.has_more_commands():
            self.parser.advance()
            if not self.parser.is_comment() and not self.parser.is_blank():
                command = self.parser.args_list()[0]
                command_type = self.parser.command_type()
                if command_type != "C_RETURN":
                    arg1 = self.parser.arg1()
                if command_type in ["C_PUSH", "C_POP", "C_FUNCTION", "C_CALL"]:
                    arg2 = self.parser.arg2()

                if command_type == "C_ARITHMETIC":
                    self.code_writer.write_arithmetic(command)
                elif command_type in ["C_PUSH", "C_POP"]:
                    self.code_writer.write_push_pop(command, arg1, arg2)
                elif command_type == "C_LABEL":
                    self.code_writer.write_label(arg1)
                elif command_type == "C_GOTO":
                    self.code_writer.write_goto(arg1)
                elif command_type == "C_IF":
                    self.code_writer.write_if_goto(arg1)
                elif command_type == "C_CALL":
                    self.code_writer.write_call(arg1, arg2)
                elif command_type == "C_FUNCTION":
                    self.code_writer.write_function(arg1, arg2)
                elif command_type == "C_RETURN":
                    self.code_writer.write_return()

    def close(self):
        self.parser.close()
        self.code_writer.close()


# Main #


if __name__ == '__main__':
    directory = sys.argv[1]
    if ".vm" not in directory:
        # if the given directory is a file containing one or more vm files
        files = os.listdir(directory)
        reverse = directory[::-1]
        main_file_name = (reverse[:reverse.index("\\")])[::-1]
        asm_file_name = directory + "\\" + main_file_name + ".asm"
        translator = VMTranslator(None, asm_file_name)
        for file in files:
            if ".vm" in file:
                translator.set_new_vm_file(directory + "\\\\" + file)
                translator.translate()
        translator.close()
    else:
        # if the given directory is a single vm file
        asm_file_name = directory[:-2] + "asm"
        translator = VMTranslator(directory, asm_file_name)
        translator.translate()
        translator.close()
