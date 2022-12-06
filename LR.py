from Item import Item


class LR:
    def __init__(self, grammar):
        self.grammar = grammar
        self.grammar.productions['S`'] = []
        self.grammar.productions['S`'].append('S')  # add augmented production
        self.canonicalCollection = {}  # productions, but with the dot added
        self.create_can_col()

    def create_can_col(self):
        for production in self.grammar.productions:
            self.canonicalCollection[production] = []
            for elem in self.grammar.productions[production]:
                self.canonicalCollection[production].append('.' + elem)

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
                index = elem.dot_position()
                if index != -1:
                    if index < len(elem.right):  # dot not at end
                        symbol = elem.roght[index + 1]  # WHAT IF ITS COMPOSED FROM MULTIPLE SYMBOLS?
                        if symbol in self.grammar.non_terminals:  # found dot non-terminal
                            for prod in self.grammar.productions.keys():  # look for a production with the symbol
                                if prod == symbol:
                                    right = ""
                                    right += "."
                                    right += self.grammar.productions[prod]  # compose the right side with the dot
                                    new_item = Item(symbol, right)
                                    items[prod].append(new_item)  # add to the new item to the list of items
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
                    right = aux
                    left = symbol
                    auxx = Item(left, right)
                    items.append(auxx)  # aux should be of type Item
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
        while True:
            aux_canonical_collection = self.canonicalCollection.copy()
            for s in aux_canonical_collection:
                for X in self.grammar.non_terminals + self.grammar.terminals:
                    result = self.goto(s, X)
                    if result != [] and result not in aux_canonical_collection.values():
                        self.canonicalCollection[s].append(result)
            if aux_canonical_collection == self.canonicalCollection:  # C stopped changing
                break
