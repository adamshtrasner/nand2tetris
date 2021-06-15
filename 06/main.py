# This is the Assembler project for
# project 6 of the Nand2Tetris Course.


import os
import sys

import Code
import Parser
import SymbolTable
from constant import PREDEFINED


def iterate_l_commands(entry, lines):
    """
    First pass: adding the label symbols to the table
    :param entry: the asm file name
    :param lines: a list, in which we insert the commands in the given entry to the file
    :return: an updated table with the labels added to the predefined symbols.
    """
    constructor = PREDEFINED.copy()
    input_file = Parser.constructor(entry)
    i = 0
    command = Parser.advance(input_file)
    while Parser.has_more_commands(command):
        #########################
        # We ignore whitespaces and comments
        command = ''.join(command.split())
        if "/" in command:
            command = command[:command.index("/")]
        #########################
        if command != "":
            lines.append(command)
            if Parser.command_type(command) == "L":
                symbol = Parser.symbol(command)
                if not (SymbolTable.contains(constructor, symbol)):
                    SymbolTable.add_entry(constructor, symbol, i)
                    i -= 1
            i += 1
        command = Parser.advance(input_file)
    input_file.close()
    return constructor


def iterate_file(lines, hack_file, constructor):
    """
    Second Pass: adds the variable symbols to the table
    and write to file
    :param lines: a list consisting the lines of the chosen asm file
    :param hack_file: the output file in which we write to
    :param constructor: the table given with the predefined symbols and labels

    The function translates the asm file with name given by entry to hack.
    """

    addr = 16
    for command in lines:  # Second Pass
        type_command = Parser.command_type(command)
        if type_command == "A":
            symbol = Parser.symbol(command)
            if not (SymbolTable.contains(constructor, symbol)):
                if symbol.isdigit():
                    SymbolTable.add_entry(constructor, symbol, int(symbol))
                else:
                    SymbolTable.add_entry(constructor, symbol, addr)
                    addr += 1
            # the addresses are given as a decimal integer, and so we convert it to binary
            # and add zeroes (from the left side) to it in order to make it a 16-bit binary code
            bin_address = str(bin(SymbolTable.get_address(constructor, symbol)))[2:]
            bin_16_address = (16 - len(bin_address)) * "0" + bin_address
            hack_file.write(bin_16_address + "\n")
        elif type_command == "C":
            dest_mnemonic = Parser.dest(command)
            comp_mnemonic = Parser.comp(command)
            jump_mnemonic = Parser.jump(command)
            bin_dest = Code.dest(dest_mnemonic)
            bin_comp = Code.comp(comp_mnemonic)
            bin_jump = Code.jump(jump_mnemonic)
            if Parser.if_shift(command):
                # the last 3 bits of a commend are 101 if the commend has a shift in it
                hack_file.write("101" + bin_comp + bin_dest + bin_jump + "\n")
            else:
                hack_file.write("111" + bin_comp + bin_dest + bin_jump + "\n")


if __name__ == '__main__':
    directory = sys.argv[1]
    lines = list()
    if ".asm" not in directory:
        # if the file given is a folder which contains asm files,
        # then iterate through the asm files in the folder
        entries = os.listdir(directory)
        for entry in entries:
            hack_file_name = entry[:-3] + "hack"
            hack_file = open(directory + "/" + hack_file_name, "w")
            table = iterate_l_commands(entry, lines)
            while "" in lines:
                lines.remove("")
            iterate_file(lines, hack_file, table)
            lines = list()
    else:
        # the file given is a single asm file
        hack_file_name = directory[:-3] + "hack"
        hack_file = open(hack_file_name, "w")
        table = iterate_l_commands(directory, lines)
        iterate_file(lines, hack_file, table)
