# 2. Symbol Table (you need to implement the data structure and required operations) :
# d. hash table
from scanner import Scanner


class ST:
    def __init__(self):
        self.table = {}
        self.hashNr = 7

    def hashFunction(self, symbol):
        """
        Returns the hash for the hashtable for the given symbol
        :param symbol: represents the identifier's symbol
        :return: the hash
        """
        s = 0
        for elem in symbol:
            s += ord(elem)
        return s % self.hashNr

    def checkIfSymbolInST(self, symbol):
        """
        Checks if the given identifier's symbol already exists in the symbol table
        :param symbol: represents the identifier's symbol
        :return: True if the symbol is found, False otherwise
        """
        poz = self.hashFunction(symbol)
        if poz in self.table.keys():
            for elem in self.table[poz]:
                if elem == symbol:
                    return True
        return False

    def addToST(self, symbol):
        """
        Adds an identifier to the symbol table if it's symbol isn't already declared
        :param symbol: represents the identifier's symbol
        :param value: represents the identifier's value
        :return: -
        """
        poz = self.hashFunction(symbol)
        if poz not in self.table.keys():
            self.table[poz] = []

        if not self.checkIfSymbolInST(symbol):
            self.table[poz].append(symbol)

    def getSymbols(self, poz):
        """
        Returns the list of symbols from the given position
        :param poz: The key of the symbol table
        :return: the list of symbols
        """
        if poz in self.table.keys():
            return self.table[poz]

    def getSymbol(self, poz, index):
        """
        Returns the symbols from the given position
        :param poz: The key of the symbol table
        :param index: The position of the symbol in the list with the given key
        :return: the symbol
        """
        return self.table[poz][index]

    def getSymbolIndex(self, symbol):
        poz = self.hashFunction(symbol)
        if poz in self.table.keys():
            return self.table[poz].index(symbol)
