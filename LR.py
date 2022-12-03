class LR:
    def __init__(self, grammar):
        self.grammar = grammar
        self.closure = {}
        self.canonicalCollection = []

    # TODO
    def closure(self):
        """
        repeat
            for any [A -> α.Bβ] in C do
                for any B -> γ in P do
                    if [B -> .γ] 2/ C then
                        C = C U [B -> .γ]
                    end if
                end for
            end for
        until C stops changing
        :return:
        """
        pass

    def goTo(self, state, symbol):
        """
        goto(s, X) = closure({[A → αX.β]|[A → α.Xβ] ∈ s})
        :param state:
        :param symbol:
        :return:
        """
        pass

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
                    if result != [] and result not in aux_canonical_collection:
                        self.canonicalCollection.append(result)
            if aux_canonical_collection == self.canonicalCollection:  # C stopped changing
                break
