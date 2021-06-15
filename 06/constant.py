# The tables shown below are the tables:
# The dest, comp, and jump tables: each mnemonic's key represent the binary code of that mnemonic.
# The constructor table: this table consists the predefined symbols, and variables are added to it
# according to the asm file which we use.


DEST = {"null": "000", "M": "001", "D": "010", "MD": "011", "A": "100", "AM": "101", "AD": "110", "AMD": "111"}

COMP_a_0 = {"0": "101010", "1": "111111", "-1": "111010", "D": "001100", "A": "110000", "!D": "001101", "!A": "110001",
            "-D": "001111", "-A": "110011", "D+1": "011111", "A+1": "110111", "D-1": "001110", "A-1": "110010",
            "D+A": "000010", "D-A": "010011", "A-D": "000111", "D&A": "000000", "D|A": "010101", "D<<": "110000",
            "A<<": "100000", "D>>": "010000", "A>>": "000000"}

COMP_a_1 = {"M": "110000", "!M": "110001", "-M": "110011", "M+1": "110111", "M-1": "110010", "D+M": "000010",
            "D-M": "010011", "M-D": "000111", "D&M": "000000", "D|M": "010101", "M<<": "100000", "M>>": "000000"}

JUMP = {"null": "000", "JGT": "001", "JEQ": "010", "JGE": "011", "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111"}

PREDEFINED = {"SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4, "SCREEN": 16384,
               "KBD": 24576,
               "R0": 0, "R1": 1, "R2": 2, "R3": 3, "R4": 4, "R5": 5,
               "R6": 6, "R7": 7, "R8": 8, "R9": 9, "R10": 10, "R11": 11,
               "R12": 12, "R13": 13, "R14": 14, "R15": 15}
