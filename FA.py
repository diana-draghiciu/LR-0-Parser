class FA:
    def __init__(self, file):
        self.file = file
        self.finalStates = []
        self.initialState = ''
        self.transitions = {}
        self.alphabet = []
        self.states = []
        self.readFA()

    def readFA(self):
        f = open(self.file, 'rt')
        lines = f.readlines()
        f.close()

        self.initialState = lines[0].strip('\n')
        self.finalStates = lines[1].strip('\n').split(',')
        self.states = lines[2].strip('\n').split(',')
        self.alphabet = lines[3].strip('\n').split(',')
        for i in range(4, len(lines)):
            tuple = lines[i].strip('\n').split('=')
            key = tuple[0].split(',')
            if key[0] not in self.states or key[1] not in self.alphabet:
                raise Exception("Transition on line " + str(i) + " not correct")
            if (key[0], key[1]) not in self.transitions.keys():
                self.transitions[(key[0], key[1])] = []
            self.transitions[(key[0], key[1])].append(tuple[1])

    def checkSequence(self, w):
        start = self.initialState
        startChanged = False
        for i in range(len(w)):
            if (start, w[i]) in self.transitions.keys():
                for j in range(len(self.transitions[(start, w[i])])):
                    elem = self.transitions[(start, w[i])][j]
                    if i < len(w) - 1:  # take a random one that isn't a final state
                        if elem not in self.finalStates:
                            start = elem
                            startChanged = True
                            break
                        else:
                            if j == len(self.transitions[(start, w[i])]) - 1: #no other moves left
                                start = elem
                                startChanged = True
                                break
                    else:
                        if elem in self.finalStates:
                            start = elem
                            startChanged = True
                            break
                if not startChanged:
                    return False
            else:
                return False
        if start in self.finalStates:
            return True
        return False

    @staticmethod
    def printMenu():
        """
        #Displays its elements, using a menu:
        # the set of states,
        # the alphabet,
        # all the transitions,
        # the initial state,
        # the set of final states.
        """
        print("1) Display the set of states")
        print("2) Display the set of alphabet")
        print("3) Display the transitions")
        print("4) Display the initial state")
        print("5) Display the set of final states")
        print("6) Verify if sequence accepted by FA")

    def menu(self):
        self.printMenu()
        done = False
        while not done:
            option = input(">")
            if option == '1':
                print(self.states)
            elif option == '2':
                print(self.alphabet)
            elif option == '3':
                print(self.transitions)
            elif option == '4':
                print(self.initialState)
            elif option == '5':
                print(self.finalStates)
            elif option == '6':
                w = input("Give sequence: ")
                print(self.checkSequence(w))
            else:
                done = True
