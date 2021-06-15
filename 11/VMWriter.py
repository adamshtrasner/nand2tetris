from SymbolTable import SymbolTable


class VMWriter:

    def __init__(self, output_file):
        self.output_file = output_file

    # -------- Methods of my own --------

    def write(self, output):
        self.output_file.write("  {}\n".format(output))

    def write_int(self, integer):
        self.write_push("constant", integer)

    def write_string(self, string):
        # push constant 'len(string)'
        # call String.new 1
        # ( do 'len(string)' times : )
        # push constant 'unicode of character'
        # call String.append 1
        self.write_int(len(string))
        self.write_call("String.new", 1)
        for c in string:
            self.write_int(ord(c))
            self.write_call("String.appendChar", 2)

    def write_malloc_for_constructor(self, n_args):
        # push constant n_args
        # call Memory.alloc 1
        # pop pointer 0
        self.write_int(n_args)
        self.write_call("Memory.alloc", 1)
        self.write_pop("pointer", 0)

    # -------- The API starts here --------

    def write_push(self, segment, index):
        if segment == "field":
            segment = "this"
        elif segment == "var":
            segment = "local"
        self.write("push {} {}".format(segment, index))

    def write_pop(self, segment, index):
        if segment == "field":
            segment = "this"
        elif segment == "var":
            segment = "local"
        self.write("pop {} {}".format(segment, index))

    def write_arithmetic(self, command):
        self.write(command)

    def write_label(self, label):
        self.output_file.write("label {}\n".format(label))

    def write_goto(self, label):
        self.write("goto {}".format(label))

    def write_if(self, label):
        self.write("if-goto {}".format(label))

    def write_call(self, name, n_args):
        self.write("call {} {}".format(name, n_args))

    def write_function(self, name, n_locals):
        self.output_file.write("function {} {}\n".format(name, n_locals))

    def write_return(self):
        self.write("return")

    def close(self):
        self.output_file.close()

