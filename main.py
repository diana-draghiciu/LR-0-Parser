from Grammar import Grammar
from LR import LR

if __name__ == '__main__':
    g = Grammar('grammar3.in')
    # g.menu()
    lr = LR(g)
    lr.canonical_col()
    print(lr.canonicalCollection)
