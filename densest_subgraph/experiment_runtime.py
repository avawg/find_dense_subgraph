from timeit import timeit

from GreedyMWED import GreedyMWED
from GreedyMWTD import GreedyMWTD
from densest_subgraph.GreedyDS import GreedyDS
from densest_subgraph.GreedyOQC import GreedyOQC
from densest_subgraph.GreedyTDS import GreedyTDS
from densest_subgraph.GreedyTGDS import GreedyTGDS

from util import read_edgelist

if __name__ == '__main__':
    ls = ["as19991213.txt", "as20000102.txt", "oregon2_010428.txt", "oregon2_010512.txt", "oregon2_010526.txt",
          "Email-EuAll.txt", "com-dblp.ungraph.txt", "com-youtube.ungraph.txt"]

    path = "../data/greedy/"
    for file in ls:
        file_name = path + file
        G = read_edgelist(file_name)

        print(file.split('.')[0])
        #
        t = timeit('GreedyDS(G)', globals=globals(), number=3) / 3
        print("DS", "%.2f" % t)

        t = timeit('GreedyOQC(G)', globals=globals(), number=3) / 3
        print("OQC", "%.2f" % t)

        t = timeit('GreedyTDS(G)', globals=globals(), number=3) / 3
        print("TDS", "%.2f" % t)

        # t = timeit('GreedyTGDS(G)', globals=globals(), number=3) / 3
        # print("TGDS", "%.2f" % t)

        # t = timeit('GreedyMWED(G)', globals=globals(), number=3) / 3
        # print("MWED", "%.2f" % t)
        #
        # t = timeit('GreedyMWTD(G)', globals=globals(), number=3) / 3
        # print("MWTD", "%.2f" % t)
