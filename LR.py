class LR:
    def __init__(self, grammar, w):
        self.grammar = grammar
        self.canonicalCollection = []
        self.goToList = {}
        self.action = []
        # self.pif = []

        self.info = []
        self.parent = [0]
        self.sibling = [0]

        self.canonical_col()
        self.computeAction()
        self.parseInput(w)

    def closure(self, list):  # list contains items
        """
        I-state
        repeat
            for any [A -> α.Bβ] in C do
                for any B -> γ in P do
                    if [B -> .γ] 2/ C then
                        C = C U [B -> .γ]
                    end if
                end for
            end for
        until C stops changing
        :return: C = closure(I);
        """
        items = list.copy()
        ok = True
        while ok:
            prev = items.copy()
            for elem in items:  # items()	Returns a list containing a tuple for each key value pair
                index = elem[1].find('.')
                if index != -1:
                    if index < len(elem[1]) - 1:  # dot not at end
                        symbol = elem[1][index + 1]  # WHAT IF ITS COMPOSED FROM MULTIPLE SYMBOLS?
                        if symbol in self.grammar.non_terminals:  # found dot non-terminal
                            for prod in self.grammar.productions.keys():  # look for a production with the symbol
                                if prod == symbol:
                                    for val in self.grammar.productions[prod]:
                                        right = ""
                                        right += "."
                                        right += val  # compose the right side with the dot
                                        if (symbol, right) not in items:
                                            items.append((symbol, right))  # add to the new item to the list of items
                    else:  # dot at end
                        continue
            if prev == items:
                ok = False
        return items  # item is a list of items

    # state should be a set of items
    # symbol should be a terminal/non-terminal
    # ex state=S, symbol=A, we find .AA and move the dot and end up with A.A and call closure
    def goto(self, state, symbol):
        """
        goto(s, X) = closure({[A → αX.β]|[A → α.Xβ] ∈ s})
        :param state: initial state
        :param symbol: non-terminal to find in initial state productions
        :return: a closure
        """
        items = []
        for elem in state:
            index = elem[1].find('.')
            if index < len(elem[1]) - 1:  # dot not at end
                # if elem[1][index + 1] == symbol: # CHANGE TO LOOK AT WHAT FOLLOWS AFTER
                # if elem[1].startswith(symbol): not good cuz it start with .
                if elem[1].startswith("." + symbol):
                    # move dot
                    aux = ""
                    aux += symbol
                    aux += "."
                    if len(aux)!=len(elem[1]):
                        aux += elem[1][len(aux)]
                    # i = 0
                    # while i < (len(elem[1])):
                    #     if i == index:
                    #         aux += elem[1][i + 1]
                    #         aux += elem[1][i]
                    #         i += 2
                    #     else:
                    #         aux += elem[1][i]
                    #         i += 1

                    items.append((elem[0], aux))  # aux should be of type Item
            else:
                continue
        if items:
            return self.closure(items)
        else:
            return []

    def canonical_col(self):
        """
        repeat
            for any s in C do
                for any X in N U ß do
                    if goto(s,X) != ∅ and goto(s,X) not in C then
                        C = C U goto(s,X)
                    end if
                end for
            end for
        until C stops changing
        """
        state0 = self.closure([('S`', '.' + self.grammar.start)])
        self.canonicalCollection.append(state0)
        while True:
            aux_canonical_collection = self.canonicalCollection.copy()
            index = 0
            for s in aux_canonical_collection:
                for X in self.grammar.non_terminals + self.grammar.terminals:
                    result = self.goto(s, X)
                    if result != []:
                        if result not in aux_canonical_collection:
                            self.canonicalCollection.append(result)

                        current_state = self.canonicalCollection.index(result)
                        if (index, X) not in self.goToList:
                            self.goToList[(index, X)] = current_state
                index += 1
            if aux_canonical_collection == self.canonicalCollection:  # C stopped changing
                break
        print("GoToList: " + str(self.goToList))

    def findReduceIndex(self, production):
        rhs = production[1][:-1]  # get rhs without dot
        index = 1
        for elem in self.grammar.productions.values():  # elem is a list of rhs
            for e in elem:
                if e == rhs:
                    return index
                index += 1
        return index

    def checkIfProduction(self, prod):
        for key, value in self.grammar.productions.items():
            for p in value:
                if p == prod:
                    return True, key
        return False, ''

    def getProductionByNr(self, nr):
        index = 1
        for key, value in self.grammar.productions.items():
            for p in value:
                if index == nr:
                    return key, p
                index += 1

    def computeAction(self):
        for elem in self.canonicalCollection:
            shift = True
            accept = False
            reduce = True
            for production in elem:
                dot_index = production[1].find('.')
                if dot_index == len(production[1]) - 1:
                    shift = False
                else:
                    reduce = False
                if production[1] == self.grammar.start + '.':
                    accept = True
            if shift:
                self.action.append("shift")
            elif accept:
                self.action.append("accept")
            elif reduce:
                self.action.append("reduce" + str(self.findReduceIndex(elem[0])))  # always only one element
        print("Action: " + str(self.action))

    def getProduction(self, prod, prodnr):
        # for key, value in self.grammar.productions.items():
        #     for p in value:
        #         if p == prod:
        #             return  key
        #
        return self.grammar.productions[prodnr]

    def parseInput(self, input):
        wstack = [0]
        oband = []

        while len(wstack) > 0:
            state = wstack[-1]  # state to check for state
            if self.action[state][0] == "s":
                wstack.append(input[0])  # push element to working stack
                wstack.append(self.goToList[(state, input[0])])
                input = input[1:]  # pop element from input stack
            elif self.action[state][0] == 'r':
                production = ""
                state = wstack[-1]
                while True:
                    result, replaced_value = self.checkIfProduction(production)
                    if result:
                        break
                    wstack.pop()  # remove state
                    prod = wstack.pop()
                    production = prod + production
                action = int(self.action[state][-1])
                oband.insert(0, action)
                wstack.append(replaced_value)
                wstack.append(self.goToList[(wstack[-2], replaced_value)])
            elif self.action[state][0] == 'a':
                break

        parent, prod = self.getProductionByNr(oband[0])
        self.info.append(parent)
        self.addToTable(oband, 0, 1)
        print("WorkStack: " + str(wstack))
        self.printTable()

    def printTable(self):
        for i in range(len(self.info)):
            print(i + 1, self.info[i], self.parent[i], self.sibling[i])

    def addToTable(self, oband, obandIndex, parent_index):
        parent, prod = self.getProductionByNr(oband[obandIndex])
        index = parent_index + 1
        for elem in prod:
            self.info.append(elem)
            self.parent.append(parent_index)
            if self.info[-2] != parent:
                self.sibling.append(len(self.info) - 1)
            else:
                self.sibling.append(0)
            if elem in self.grammar.non_terminals:
                self.addToTable(oband, obandIndex + 1, index)
            index += 1
