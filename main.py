from Grammar import Grammar
from LR import LR

if __name__ == '__main__':
    g = Grammar('grammar2.in')
    # g.menu()
    lr = LR(g)
