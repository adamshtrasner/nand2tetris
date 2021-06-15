def constructor(input_file_name):
    # This program opens the file with the name
    # given in input_file_name
    input_file = open(input_file_name, "r")
    return input_file


def has_more_commands(command):
    """
    :param command: a string
    :return: True if there are any commends left, False otherwise
    """
    if not command:
        return False
    return True


def advance(input_file):
    """
    :param input_file: the input file
    :return: the next commend in the file
    """
    next_com = input_file.readline()
    return next_com


def command_type(command):
    """
    :param command: a string
    :return: "A" if it's an A-command, "C" if it's a C-command,
    "L" if it's a Label.
    """
    if "@" in command:
        return "A"
    if ("=" in command) or (";" in command):
        return "C"
    if (command[0] == "(") and (command[len(command) - 1] == ")"):
        return "L"


def symbol(command):
    """
    :param command: a string
    :return: returning XXX if the command is a label - (XXX), and X if its
    an A-command - @X
    """
    if command_type(command) == "A":
        return command[1:]
    else:
        return command[1:(len(command)-1)]


def dest(c_command):
    """
    :param c_command: a C-command - string
    :return: the destination part of the command
    """
    if "=" not in c_command:
        return "null"
    return c_command[:c_command.index("=")]


def comp(c_command):
    """
    :param c_command: a C-command - string
    :return: the computation part of the commend
    """
    if dest(c_command) == "null":
        return c_command[:c_command.index(";")]
    return c_command[c_command.index("=") + 1:]


def jump(c_command):
    """
    :param c_command: a C-command - string
    :return: the jump part of the command.
    """
    if ";" not in c_command:
        return "null"
    return c_command[c_command.index(";") + 1:]


def if_shift(c_command):
    """
    :param c_command: a C-command - string
    :return: True if the command has a shift in it, False otherwise
    """
    return "<" in c_command or ">" in c_command
