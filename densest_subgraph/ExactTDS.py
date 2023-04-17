import os

import networkx as nx

from util import read_edgelist, measure
from triangle_util import get_triangles


def triangle_densest_subgraph(G):
    """
    TDS基于最大流的精确算法 $O(m^{3/2} + (nt + \min(n, t)^3)\log_{}{n})$
    :param G:
    :return: G1: subgraph with maximum average triangle degree
    Reference
    --------
    Tsourakakis C. "The K-clique Densest Subgraph Problem." 2015
    """
    triangles = get_triangles(G)
    # 不含三角形，直接返回
    if len(triangles) == 0:
        return None
    # 计算节点权重
    node_weight = {node: 0 for node in G.nodes()}
    for triangle in triangles:
        for node in triangle:
            node_weight[node] += 1
    
    def construct_network(G, alpha, triangles):
        """
        构建有向图
        """
        g = nx.DiGraph()
        # 添加节点
        g.add_node('s')
        for triangle in triangles:
            g.add_node(triangle)
        for node in G.nodes():
            g.add_node(node)
        g.add_node('t')
        # 添加边
        for triangle in triangles:
            for node in triangle:
                g.add_edge(triangle, node, capacity=2)
                g.add_edge(node, triangle, capacity=1)
        for node in G.nodes():
            g.add_edge('s', node, capacity=node_weight[node])
            g.add_edge(node, 't', capacity=3 * alpha)
        return g
    
    def update_digraph(g, alpha):
        for node in g.pred['t']:  # 存在该边则直接更新
            g.add_edge(node, 't', capacity=3 * alpha)
            
    n, t = G.number_of_nodes(), len(triangles)
    lo, hi = t / n, (n - 1) * (n - 2) / 6
    condition = 1 / (n * (n - 1))
    V1 = set()
    alpha = (lo + hi) / 2
    g = construct_network(G, alpha, triangles)
    
    # 二分查找
    while hi - lo >= condition:
        alpha = (lo + hi) / 2
        update_digraph(g, alpha)
        cut_value, minimum_cuts = nx.minimum_cut(g, 's', 't')
        
        # S 为源点's'所在集合
        S = minimum_cuts[0] if 's' in minimum_cuts[0] else minimum_cuts[1]
        
        if S == {'s'}:
            hi = alpha
        else:
            lo = alpha
            V1 = set(G.nodes()) & S
    return G.subgraph(V1)


if __name__ == '__main__':
    path = "../data/exact/"
    for file in os.listdir(path):
        dataset = file.split('.')[0]
        mes = {"dataset": dataset}
        file_name = path + file
        G = read_edgelist(file_name)
        G1 = triangle_densest_subgraph(G)
        mes.update(measure(G1))
        print(mes)
