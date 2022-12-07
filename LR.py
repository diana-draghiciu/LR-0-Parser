class LR:
    def __init__(self, grammar):
        self.grammar = grammar
        self.canonicalCollection = []
        self.goToList = {}
        self.action = []
        self.canonical_col()
        self.computeAction()
        self.parseInput(['a', 'b', 'b', 'c'])

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

    def goto(self, state, symbol):

        # state should be a set of items
        # symbol shoud be a terminal/non-terminal
        """
        goto(s, X) = closure({[A → αX.β]|[A → α.Xβ] ∈ s})
        :param state: initial state
        :param symbol: non-terminal to find in initial state productions
        :return: a closure
        """
        # ex state=S, symbol=A, we find .AA and move the dot and end up with A.A and call closure
        items = []
        for elem in state:
            index = elem[1].find('.')
            if index < len(elem[1]) - 1:  # dot not at end
                if elem[1][index + 1] == symbol:
                    # move dot
                    aux = ""
                    i = 0
                    while i < (len(elem[1])):
                        if i == index:
                            aux += elem[1][i + 1]
                            aux += elem[1][i]
                            i += 2
                        else:
                            aux += elem[1][i]
                            i += 1
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

    def parseInput(self, input):
        wstack = [0]
        oband = []
        for elem in input:
            if len(input) > 0:
                prev = wstack[-1]
                wstack.append(elem)  # push element to working stack
                wstack.append(self.goToList[(prev, elem)])
                input = input[1:]  # pop element from input stack
            # TODO continue parsing when reducing starts ->compute oband
        print("WorkStack: " + str(wstack))
