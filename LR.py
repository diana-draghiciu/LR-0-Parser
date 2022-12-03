class LR:
    def __init__(self, grammar):
        self.grammar = grammar
        self.grammar.productions['S`'] = []
        self.grammar.productions['S`'].append('S')  # add augmented production
        self.canonicalCollection = {} # productions, but with the dot added
        self.createCanCol()

    def createCanCol(self):
        for production in self.grammar.productions:
            self.canonicalCollection[production] = []
            for elem in self.grammar.productions[production]:
                self.canonicalCollection[production].append('.' + elem)

    def computeClosure(self, list):
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
        # inputState: [a.A, b.]
        items = list.copy()
        while True:
            for elem in items.values():
                index = elem.find('.')
                if index != -1:
                    if index < len(elem):  # dot not at end
                        symbol = elem[index + 1]
                        if symbol in self.grammar.non_terminals:  # found dot non-terminal
                            for prod in self.grammar.productions.keys():
                                if prod == symbol and prod not in items:
                                    items.append(prod)
                            if list == items:
                                break
                    else:  # dot at end
                        continue
        #TODO
        # return ??

    def goTo(self, state, symbol):
        """
        goto(s, X) = closure({[A → αX.β]|[A → α.Xβ] ∈ s})
        :param state: initial state
        :param symbol: non-terminal to find in initial state productions
        :return: a closure
        """
        # ex state=S, symbol=A we find .AA and move the dot and end up with A.A and call closure
        items = []
        for elem in self.canonicalCollection[state]:
            index = elem.find('.')
            if index < len(elem):  # dot not at end
                if elem[index + 1] == symbol:
                    # move dot
                    aux = ""
                    i = 0
                    while i < (len(elem)):
                        if i == index:
                            aux += elem[i + 1]
                            aux += elem[i]
                            i += 2
                        else:
                            aux += elem[i]
                            i += 1
                    items.append(aux)
            else:
                continue
        if items:
            return self.computeClosure(items)
        else:
            return []

    def canonicalCol(self):
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
        while True:
            aux_canonical_collection = self.canonicalCollection.copy()
            for s in aux_canonical_collection:
                for X in self.grammar.non_terminals + self.grammar.terminals:
                    result = self.goTo(s, X)
                    if result != [] and result not in aux_canonical_collection.values():
                        self.canonicalCollection[s].append(result)
            if aux_canonical_collection == self.canonicalCollection:  # C stopped changing
                break