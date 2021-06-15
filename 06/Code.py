import constant


def dest(dest_str):
    """
    :param dest_str: the destination mnemonic
    :return: the binary code of the mnemonic
    """
    return constant.DEST[dest_str]


def comp(comp_str):
    """
    :param comp_str: the computation mnemonic
    :return: the binary code of the mnemonic
    """
    if "M" in comp_str:
        return "1" + constant.COMP_a_1[comp_str]
    return "0" + constant.COMP_a_0[comp_str]


def jump(jump_str):
    """
    :param jump_str: the jump mnemonic
    :return: the binary code of the mnemonic
    """
    return constant.JUMP[jump_str]
