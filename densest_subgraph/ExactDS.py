import networkx as nx

from util import read_edgelist
from util import measure
import os


def densest_subgraph(G):
    """
    densest_subgraph的精确算法 $O(m \min(\sqrt(m), n^{2/3}) log_{}{v})$
    :param G: 输入的无向图
    :return: G1: subgraph with maximum average degree
    Reference
    ---------
    Goldberg A. V. "Finding a Maximum Density Subgraph." 1984
    """

    def construct_digraph(G, lambda_):
        """
        构建有向流图
        :param G: 无向图
        :param lambda_:
        :return: directed_graph: 构建的有向带权图
        """
        g = nx.DiGraph()
        # 初始化有向图节点
        g.add_node('s')
        for node in G.nodes():
            g.add_node(node)
        g.add_node('t')
        m = G.number_of_edges()
        # 添加边
        for node in G.nodes():
            g.add_edge('s', node, capacity=m)
        for edge in G.edges():
            u, v = edge
            g.add_edge(u, v, capacity=1)
            g.add_edge(v, u, capacity=1)
        for node in G.nodes():
            g.add_edge(node, 't', capacity=m + 2 * lambda_ - len(G.adj[node]))
        return g

    def update_digraph(g, G, lambda_):
        m = G.number_of_edges()
        for node in g.pred['t']:
            g.add_edge(node, 't', capacity=m + 2 * lambda_ - len(G.adj[node]))
    
    V, V1 = set(G.nodes()), set()
    lo, hi = 0, G.number_of_edges()
    n = G.number_of_nodes()
    condition = 1 / (n * (n - 1))

    lambda_ = (lo + hi) / 2
    g = construct_digraph(G, lambda_)

    while hi - lo >= condition:
        lambda_ = (lo + hi) / 2
        update_digraph(g, G, lambda_)
        cut_value, cuts = nx.minimum_cut(g, 's', 't')
        S = cuts[0] if 's' in cuts[0] else cuts[1]
        if S == {'s'}:
            hi = lambda_
        else:
            lo = lambda_
            V1 = S & V
    return G.subgraph(V1)


if __name__ == '__main__':
    path = "../data/exact/"
    for file in os.listdir(path):
        dataset = file.split('.')[0]
        mes = {"dataset": dataset}
        file_name = path + file
        G = read_edgelist(file_name)
        G1 = densest_subgraph(G)
        mes.update(measure(G1))
        print(mes)

