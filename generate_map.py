import random
import MinimumSpanningTree





def __main__():
    rand = random.seed(47)
    mst = MinimumSpanningTree.MST(5, 100, 100, 1, rand)
    mst.add_cycles(2)
    return map