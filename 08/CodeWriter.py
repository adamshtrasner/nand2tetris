WRITE_MODE = "w"
COMMENT = "//"
SEGMENTS = {"local": "LCL", "argument": "ARG", "this": "THIS",
            "that": "THAT"}


class CodeWriter:
    def __init__(self, file_name):
        self.file_name = file_name
        self.asm_file = self.constructor()

        self.curr_function = "Sys.init"
        self.write_init()

        self.curr_vm_file_name = None

        self.num_of_vm_files = 1

        self.continue_labels = 0

        self.num_return_labels = 1
        self.return_address = "RETURN{num_returns}".format(num_returns=str(self.num_return_labels))

        self.num_frames = 0

        self.curr_return_address = None

    def constructor(self):
        return open(self.file_name, WRITE_MODE)

    # project 8
    def write_init(self):
        self.write(COMMENT + " SP = 256")
        self.at_var("256")
        self.set_d_to_m()
        self.at_var("SP")
        self.set_m_to_d()

        self.write(COMMENT + " call Sys.init")
        self.write_call("Sys.init", 0)

    def write_label(self, label):
        if self.curr_function is None:
            self.write("(" + label + ")")
        else:
            self.write("(" + self.curr_function + "$" + label + ")")

    def write_goto(self, label):
        self.at_var(label)
        self.write("D;JMP")

    def write_if_goto(self, label):
        self.at_var("SP")
        self.set_a_to_m()
        self.set_d_to_m()
        self.at_var(label)
        self.write("D;JNE")

    def write_call(self, func_name, num_args):
        self.curr_return_address = "RETURN_FROM_" + func_name
        to_save = [self.curr_return_address, "SP", "LCL", "ARG", "THIS", "THAT"]
        for segment in to_save:
            self.write(COMMENT + " push " + segment)
            self.at_var(segment)
            self.set_d_to_m()
            self.at_var("SP")
            self.set_a_to_m()
            self.set_m_to_d()
            self.increment_sp()

        self.write(COMMENT + " ARG = SP - n - 5")
        self.at_var("SP")
        self.set_d_to_m()
        self.at_var("ARG")
        self.set_m_to_d()
        self.at_var(str(num_args))
        self.set_d_to_a()
        self.at_var("ARG")
        self.write("M=M-D")
        self.at_var("5")
        self.set_d_to_a()
        self.at_var("ARG")
        self.write("M=M-D")

        self.write(COMMENT + " LCL = SP")
        self.at_var("SP")
        self.set_d_to_m()
        self.at_var("LCL")
        self.set_m_to_d()

        self.write(COMMENT + " goto func")
        self.at_var(func_name)
        self.write("D;JMP")

        self.write(COMMENT + " (return-address)")
        self.write_label(self.curr_return_address)

    def write_function(self, func_name, num_locals):
        self.curr_function = func_name
        self.write_label(func_name)
        for i in range(int(num_locals)):
            self.write_push_pop("push", "constant", "0")

    def write_return(self):
        self.write(COMMENT + " RETURN")
        if not self.curr_return_address:
            self.curr_return_address = "NO_CALLER_LOOP"
        self.num_frames += 1
        frame = "FRAME{}".format(str(self.num_frames))
        self.write(COMMENT + " " + frame + " = LCL")
        self.at_var("LCL")
        self.set_d_to_m()
        self.at_var(frame)
        self.set_m_to_d()

        self.write(COMMENT + self.curr_return_address + "= RAM[FRAME-5]")
        self.at_var(frame)
        self.set_d_to_m()
        self.at_var("5")
        self.write("D=D-A")
        self.at_var("addr")
        self.set_a_to_m()
        self.set_d_to_m()
        self.at_var(self.curr_return_address)
        self.set_m_to_d()

        self.write(COMMENT + " RAM[ARG] = pop()")
        self.write_push_pop("pop", "argument", "0")

        self.write(COMMENT + " SP = ARG + 1")
        self.at_var("ARG")
        self.write("D=M+1")
        self.at_var("SP")
        self.set_m_to_d()

        self.write(COMMENT + " THAT = RAM[FRAME - 1]")
        self.at_var(frame)
        self.set_d_to_m()
        self.at_var("1")
        self.write("D=D-A")
        self.at_var("addr")
        self.set_a_to_m()
        self.set_d_to_m()
        self.at_var("THAT")
        self.set_m_to_d()

        self.write(COMMENT + " THIS = RAM[FRAME - 2]")
        self.at_var(frame)
        self.set_d_to_m()
        self.at_var("2")
        self.write("D=D-A")
        self.at_var("addr")
        self.set_a_to_m()
        self.set_d_to_m()
        self.at_var("THIS")
        self.set_m_to_d()

        self.write(COMMENT + " ARG = RAM[FRAME - 3]")
        self.at_var(frame)
        self.set_d_to_m()
        self.at_var("3")
        self.write("D=D-A")
        self.at_var("addr")
        self.set_a_to_m()
        self.set_d_to_m()
        self.at_var("ARG")
        self.set_m_to_d()

        self.write(COMMENT + " LCL = RAM[FRAME - 4]")
        self.at_var(frame)
        self.set_d_to_m()
        self.at_var("4")
        self.write("D=D-A")
        self.at_var("addr")
        self.set_a_to_m()
        self.set_d_to_m()
        self.at_var("LCL")
        self.set_m_to_d()

        self.write(COMMENT + " goto return-address")
        if self.curr_return_address == "NO_CALLER_LOOP":
            self.write_label("NO_CALLER_LOOP")
        self.write_goto(self.curr_return_address)

    # project 7 functions
    def set_vm_file_name(self, new_vm_name):
        self.curr_vm_file_name = new_vm_name

    def decrement_sp(self):
        self.write(COMMENT + " SP--")
        self.write("@SP\nM=M-1")

    def increment_sp(self):
        self.write("@SP\nM=M+1 " + COMMENT + " SP++")

    def set_d_to_a(self):
        self.write("D=A")

    def set_a_to_m(self):
        self.write("A=M")

    def set_d_to_m(self):
        self.write("D=M")

    def set_m_to_d(self):
        self.write("M=D")

    def at_var(self, var):
        self.write("@{variable}".format(variable=var))

    # We'll use the fact that we can use R13, R14, and R15
    # as general purpose registers.
    # We use RAM[13] (R13) as an address value (R13 = addr)

    def set_r15(self):
        """
        we set RAM[15] to the variable in RAM[SP - 1]
        """
        self.decrement_sp()
        self.set_a_to_m()
        self.set_d_to_m()
        self.at_var("R15")
        self.set_m_to_d()

    def set_r14(self):
        """
        we set RAM[14] to the variable in to RAM[SP-1]
        """
        self.decrement_sp()
        self.set_a_to_m()
        self.set_d_to_m()
        self.at_var("R14")
        self.set_m_to_d()

    def eq(self):
        self.at_var("EQ")
        self.write("D;JEQ")
        self.write(COMMENT + " if R14 != R15")
        self.at_var("R14")
        self.write(COMMENT + " R14 is false")
        self.write("M=0")
        self.at_var("CONTINUE{}".format(self.continue_labels))
        self.write("D;JMP")
        self.write(COMMENT + " if R14 = R15")
        self.write_label("EQ")
        self.at_var("R14")
        self.write(COMMENT + " R14 is true")
        self.write("M=-1")

    def gt(self):
        self.at_var("GT")
        self.write("D;JGT")
        self.write(COMMENT + " if R14 - R15 > 0 => if R14 > R15")
        self.at_var("R14")
        self.write(COMMENT + " R14 is false")
        self.write("M=0")
        self.at_var("CONTINUE{}".format(self.continue_labels))
        self.write("D;JMP")
        self.write(COMMENT + " if R14 > R15")
        self.write_label("GT")
        self.at_var("R14")
        self.write(COMMENT + " R14 is true")
        self.write("M=-1")

    def lt(self):
        self.at_var("LT")
        self.write("D;JLT")
        self.write(COMMENT + " if R14 - R15 < 0 => if R14 < R15")
        self.at_var("R14")
        self.write(COMMENT + " R14 is false")
        self.write("M=0")
        self.at_var("CONTINUE{}".format(self.continue_labels))
        self.write("D;JMP")
        self.write(COMMENT + " if R14 < y")
        self.write_label("LT")
        self.at_var("R14")
        self.write(COMMENT + " R14 is true")
        self.write("M=-1")

    def write_arithmetic(self, command):
        self.set_r15()
        if command != "not" and command != "neg":
            self.set_r14()
            self.at_var("R15")
            self.set_d_to_m()
            self.at_var("R14")

        if command == "add":
            self.write("M=M+D " + COMMENT + command)
        elif command == "sub":
            self.write("M=M-D")
        elif command == "neg":
            self.at_var("R15")
            self.write("M=-M")
        elif command in ["eq", "gt", "lt"]:
            self.continue_labels += 1
            i = self.continue_labels
            self.write("D=M-D")
            if command == "eq":
                self.eq()
            if command == "gt":
                self.gt()
            if command == "lt":
                self.lt()
            self.write_label("CONTINUE{}".format(i))
        elif command == "and":
            self.write("M=M&D")
        elif command == "or":
            self.write("M=M|D")
        elif command == "not":
            self.at_var("R15")
            self.write("M=!M")

        if command in ["not", "neg"]:
            self.at_var("R15")

        else:
            self.at_var("R14")

        self.set_d_to_m()
        self.at_var("SP")
        self.set_a_to_m()
        self.set_m_to_d()
        self.increment_sp()

    def pop(self):
        self.decrement_sp()
        self.at_var("SP")
        self.set_a_to_m()
        self.set_d_to_m()
        self.at_var("R13")
        self.set_a_to_m()
        self.write(COMMENT + "RAM[R13] = RAM[SP]")
        self.set_m_to_d()

    def push(self):
        self.at_var("R13")
        self.set_a_to_m()
        self.set_d_to_m()
        self.at_var("SP")
        self.set_a_to_m()
        self.write(COMMENT + "RAM[SP] = RAM[R13]")
        self.set_m_to_d()
        self.increment_sp()

    def write_push_pop(self, command, segment, index):

        if segment == "temp":
            location = str(5 + int(index))
            base = "R{}".format(location)
            self.at_var(base)

        elif segment == "pointer":
            if index == "0":
                base = "THIS"
                self.at_var(base)
            else:
                base = "THAT"
                self.at_var(base)

        elif segment == "static":
            start_index = 0
            if "\\" in self.file_name:
                start_index = self.file_name.index("\\") + 1
            base = self.file_name[start_index:-3] + index
            self.at_var(base)

        elif segment == "constant":
            # the only command possible is push
            self.write(COMMENT + " push constant " + index)
            self.at_var(index)
            self.set_d_to_a()
            self.at_var("SP")
            self.set_a_to_m()
            self.set_m_to_d()
            self.increment_sp()

        else:
            base = SEGMENTS[segment]
            self.at_var(base)

        if segment != "constant":
            self.set_d_to_m()
            self.at_var("R13")
            self.set_m_to_d()
            self.at_var(index)
            self.set_d_to_a()
            self.at_var("R13")
            self.write("M=M+D")

            if command == "pop":
                self.write(COMMENT + "pop" + " " + segment + " " + index)
                self.pop()

            else:
                self.write(COMMENT + "push" + " " + segment + " " + index)
                self.push()

    def write(self, str):
        """
        this function just writes the given string to the file
        """
        self.asm_file.write(str + "\n")

    def close(self):
        self.asm_file.close()
