import os
import networkx as nx
from triangle_util import get_triangles, get_triangle_node_weight
from util import measure, read_edgelist


def maximum_weighted_kclique_density(G, k=3):
    """
    Maximum Weighted K-clique Density的精确算法
    时间复杂度为$O((n+t)^2 \log_{}{W_\triangle})$，$t$是$k$-团的个数
    :param G: 输入的无向图
    :param k: $k$-clique的大小，k=3, clique为triangle, 即为MWTD
                           k=2, clique为edge, 对应MWED
    :return: subG: subgraph with maximum weighted k-clique density
    Reference
    --------
    Jiabing W. "Finding Dense Subgraphs with Maximum Weighted Triangle Density." 2020
    """
    if k not in [2, 3]:
        raise Exception("参数k目前只支持为2或3")

    def construct_digraph(G, cliques, lambda_):
        """
        :param cliques: {}，key为clique元组， value为对应的权重
        :param lambda_:
        :return: g: 构建的有向带权图
        """
        g = nx.DiGraph()
        # 添加节点
        g.add_node('s')
        for clique in cliques:
            g.add_node(clique)
        for node in G.nodes():
            g.add_node(node)
        g.add_node('t')
        # 添加边
        for clique, weight in cliques.items():
            g.add_edge('s', clique, capacity=weight)
            for node in clique:
                g.add_edge(clique, node, capacity=float('inf'))
        for node in G.nodes():
            g.add_edge(node, 't', capacity=lambda_)
        return g
    
    def update_digraph(g, lambda_):
        for node in g.pred['t']:  # 存在该边则直接更新
            g.add_edge(node, 't', capacity=lambda_)
    
    # list all cliques
    cliques = {}
    if k == 3:
        triangles = get_triangles(G)
        cliques, _ = get_triangle_node_weight(G, triangles)
    elif k == 2:
        for edge in G.edges():
            u, v = edge
            cliques[tuple(sorted((u, v)))] = 0
        triangles = get_triangles(G)
        for triangle in triangles:
            u, v, w = triangle
            cliques[(u, v)] += 1
            cliques[(u, w)] += 1
            cliques[(v, w)] += 1
        # for edge in G.edges():
        #     u, v = edge
        #     nodes = set(G.adj[u]) & set(G.adj[v])
        #     cliques[edge] = len(nodes)

    # cliques为空集，直接返回
    if len(cliques) == 0:
        return None

    lo, hi = 0, sum(cliques.values())
    n = G.number_of_nodes()
    condition = 1 / (n * (n - 1))

    lambda_ = (lo + hi) / 2
    g = construct_digraph(G, cliques, lambda_)
    V = {}
    # 二分查找
    while hi - lo >= condition:
        lambda_ = (lo + hi) / 2

        update_digraph(g, lambda_)
        cut_value, cuts = nx.minimum_cut(g, 's', 't')
        # S 为源点's'所在集合
        S = cuts[0] if 's' in cuts[0] else cuts[1]
        
        if S == {'s'}:  # 所有子图的密度都比lambda_小
            hi = lambda_
        else:
            lo = lambda_  # 存在子图的密度 >= lambda_
            V = set(G.nodes()) & S
    return G.subgraph(V)


if __name__ == '__main__':
    path = "./data/exact/"
    for file in os.listdir(path):
        datasets = file.split('.')[0]
        mes = {"dataset": datasets}
        file_name = path + file
        G = read_edgelist(file_name)
        G1 = maximum_weighted_kclique_density(G, k=2)
        mes.update(measure(G1))
        print(mes)
