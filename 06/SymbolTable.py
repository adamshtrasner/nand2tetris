import constant


def add_entry(constructor, symbol, address):
    """
    :param constructor: a table with the predefined symbols
    :param symbol: a string
    :param address: a given address
    :return: adds the symbol with the given address to the given table
    """
    constructor.update({symbol: address})


def contains(constructor, symbol):
    """
    :param constructor: a table with the predefined symbols
    :param symbol: a string
    :return: True if a symbol exists in the table, False otherwise
    """
    return symbol in constructor


def get_address(constructor, symbol):
    """
    :param constructor: a table with the predefined symbols
    :param symbol: a string
    :return: the address of the given symbol according to the table
    """
    return constructor[symbol]
