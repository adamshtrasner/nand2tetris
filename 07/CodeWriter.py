WRITE_MODE = "w"
COMMENT = "//"

SEGMENTS = {"constant": "SP", "local": "LCL", "argument": "ARG", "this": "THIS",
            "that": "THAT"}


class CodeWriter:
    def __init__(self, file_name):
        self.file_name = file_name
        if self.file_name is not None:
            self.asm_file = self.constructor()
        self.continue_labels = 0

    def constructor(self):
        return open(self.file_name, WRITE_MODE)

    def set_new_asm_file_name(self, new_file_name):
        self.close()
        self.file_name = new_file_name
        self.asm_file = self.constructor()
        self.continue_labels = 0

    def decrement_sp(self):
        self.write("@SP\nM=M-1" + COMMENT + "SP--")

    def increment_sp(self):
        self.write("@SP\nM=M+1 " + COMMENT + "SP++")

    def set_a_to_m(self):
        self.write("A=M")

    def set_d_to_m(self):
        self.write("D=M")

    def set_m_to_d(self):
        self.write("M=D")

    def at_var(self, var):
        self.write("@{variable}".format(variable=var))

    # We'll use the fact that we can use R13, R14, and R15
    #
    # We use RAM[13] (R13) as an address value

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

    def write(self, str):
        """
        this function just writes the given string to the file
        """
        self.asm_file.write(str + "\n")

    def eq(self):
        self.at_var("eq")
        self.write("D;JEQ")
        self.write(COMMENT + "if R14 != R15")
        self.at_var("R14")
        self.write("M=0" + COMMENT + "R14 is false")
        self.write("(EQ)" + COMMENT + "if R14 = R15")
        self.at_var("R14")
        self.write("M=-1" + COMMENT + "R14 is true")

    def gt(self):
        self.at_var("gt")
        self.write("D;JGT")
        self.write(COMMENT + "if R14 - R15 > 0 => if R14 > R15")
        self.at_var("R14")
        self.write("M=0" + COMMENT + "R14 is false")
        self.write("(GT)" + COMMENT + "if R14 > R15")
        self.at_var("R14")
        self.write("M=-1" + COMMENT + "R14 is true")

    def lt(self):
        self.at_var("lt")
        self.write("D;JLT")
        self.write(COMMENT + "if R14 - R15 < 0 => if R14 < R15")
        self.at_var("R14")
        self.write("M=0" + COMMENT + "R14 is false")
        self.write("(LT)" + COMMENT + "if R14 < y")
        self.at_var("R14")
        self.write("M=-1" + COMMENT + "R14 is true")

    def write_arithmetic(self, command):
        self.set_r15()
        if command != "not" and command != "neg":
            self.set_r14()
            self.at_var("R15")
            self.set_d_to_m()
            self.at_var("R14")

        if command == "add":
            self.write("M=M+D " + COMMENT + command)
            self.increment_sp()
        elif command == "sub":
            self.write("M=M-D")
            self.increment_sp()
        elif command == "neg":
            self.at_var("y")
            self.write("M=-M")
            self.increment_sp()
        elif command in ["eq", "gt", "lt"]:
            self.continue_labels += 1
            i = self.continue_labels
            self.at_var("R15")
            self.set_d_to_m()
            self.at_var("R14")
            self.write("D=M-D")
            if command == "eq":
                self.eq()
            if command == "gt":
                self.gt()
            if command == "lt":
                self.lt()
            self.write("(CONTINUE{})".format(i))
            self.increment_sp()
        elif command == "and":
            self.write("M=M&D")
            self.increment_sp()
        elif command == "or":
            self.write("M=M|D")
            self.increment_sp()
        elif command == "not":
            self.at_var("y")
            self.write("M=!M")
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
        return

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

        else:
            base = SEGMENTS[segment]
            self.at_var(base)

        self.set_d_to_m()
        self.at_var("R13")
        self.set_m_to_d()
        self.at_var(index)
        self.set_d_to_m()
        self.at_var("R13")
        self.write("M=M+D")

        if command == "pop":
            self.write(COMMENT + "pop" + " " + segment + " " + index)
            self.pop()

        else:
            self.write(COMMENT + "push" + " " + segment + " " + index)
            self.push()

    def close(self):
        self.asm_file.close()
