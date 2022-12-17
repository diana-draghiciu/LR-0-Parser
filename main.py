from FA import FA
from Grammar import Grammar
from LR import LR
from scanner import Scanner
from symbolTable import ST


def createW(scanner, st, ct):
    w = []
    for elem in scanner.pif:
        key = list(elem.keys())[0]
        value = list(elem.values())[0]
        if key == 'identifier':
            symbol = st.getSymbol(value[0], value[1])
            w.append(symbol)
        elif key == 'constant':
            symbol = ct.getSymbol(value[0], value[1])
            w.append(symbol)
        else:
            w.append(key)
    print(w)
    return w


if __name__ == '__main__':
    st = ST()
    ct = ST()
    faS = FA("symbolFA.in")
    faC = FA("constantFA.in")
    scanner = Scanner('p1.txt', st, ct, faS, faC)

    prog = 2
    if prog == 2:
        g = Grammar('Grammars/grammar2.in')  # own language
        lr = LR(g, createW(scanner, st, ct))
    elif prog == 3:
        g = Grammar('Grammars/grammar3.in')
        f = open("seq.txt", 'rt')
        lines = f.readlines()
        w = []
        for line in lines:
            w.append(line.strip('\n'))
        f.close()
        lr = LR(g, w)    # with grammar 3
