class Reader:
    def __init__(self, file):
        self.file = file
        self.start = "S"
        self.non_terminals = []
        self.terminals = []
        self.productions={}
        self.readGrammar()

    def readGrammar(self):
        f = open(self.file, 'rt')
        lines = f.readlines()
        f.close()

        self.start = lines[0].strip('\n')
        self.non_terminals = lines[1].strip('\n').split(',')
        self.terminals = lines[2].strip('\n').split(',')
        for i in range(3, len(lines)):
            tuple = lines[i].strip('\n').split('->')
            if tuple[0] not in self.productions.keys():
                self.productions[tuple[0]]=[]
            self.productions[tuple[0]].append(tuple[1])

    def checkCFG(self):
        for elem in self.productions.keys():
            if elem not in self.non_terminals:
                return False
        return True

    @staticmethod
    def printMenu():
        print("1) Display the start symbol")
        print("2) Display the set of non-terminals")
        print("3) Display the sel of terminals")
        print("4) Display the set of productions")
        print("5) Display the set of productions for a given non-terminal")
        print("6) CFG")

    def menu(self):
        self.printMenu()
        done = False
        while not done:
            option = input(">")
            if option == '1':
                print(self.start)
            elif option == '2':
                print(self.non_terminals)
            elif option == '3':
                print(self.terminals)
            elif option == '4':
                print(self.productions)
            elif option == '5':
                nt = input("Give non-terminal: ")
                if nt in self.productions.keys():
                    print(self.productions[nt])
                else:
                    print("The given non-terminat is not in the set of productions")
            elif option == '6':
                result = self.checkCFG()
                if result:
                    print("Grammar is CFG")
                else:
                    print("Grammar is not CFG")
            else:
                done = True

if __name__ == '__main__':
    r = Reader('grammar2.in')
    r.menu()