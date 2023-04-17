import os
from collections import defaultdict

from triangle_util import get_triangles
from util import read_edgelist, measure
import networkx as nx


def construct_triangle_graph(G):
    """
    构建三角形图
    """
    def share_edge(tri_u, tri_v):
        uu, uv, uw = tri_u
        vu, vv, vw = tri_v
        edges_u = {(uu, uv), (uu, uw), (uv, uw)}
        edges_v = {(vu, vv), (vu, vw), (vv, vw)}
        if len(edges_u & edges_v) > 1:
            print("****")
        if len(edges_u & edges_v) > 0:
            return True, tuple((edges_u & edges_v).pop())
        else:
            return False, None

    triangles = get_triangles(G)
    tri_G = nx.Graph()
    # 添加节点
    for i, triangle in enumerate(triangles):
        tri_G.add_node(i, tri=triangle)
    # 添加边
    n = tri_G.number_of_nodes()
    for u in range(n):
        tri_u = tri_G.nodes[u]["tri"]
        for v in range(u + 1, n):
            tri_v = tri_G.nodes[v]["tri"]
            flag, label = share_edge(tri_u, tri_v)
            if flag:
                tri_G.add_edge(u, v, label=label)
    return tri_G


def triangle_graph_density(G):
    d, n = 0, G.number_of_nodes()
    for u in G.nodes():
        counter = defaultdict(int)
        for v in G.adj[u]:
            label = G.edges[u, v]['label']
            counter[label] += 1
        if len(counter) > 0:
            d += min(counter.values())
    return d / n


def triangle_graph_densest_subgraph(G):
    # G: triangle-graph

    # Get the vertices of G
    V = set(G.nodes())

    # Compute the lower and upper bounds for alpha
    n = len(V)
    l = triangle_graph_density(G)
    u = n * (n - 1) / (3 * n)

    # Initialize the solution to be the entire vertex set
    S_star = V.copy()

    # Loop until the interval [l, u] has length 1
    while u - l >= 1 / (n * (n - 1)):
        alpha = (l + u) / 2

        # Solve the supermodular optimization problem using Orlin's algorithm
        val, S = orlin_supermodular_opt(G, lambda x : triangle_graph_density(x), alpha)

        # Check if the objective function value is negative
        if val < 0:
            u = alpha
        else:
            l = alpha
            S_star = S.copy()
    return S_star


def orlin_supermodular_opt(G, f, alpha):
    # G: networkx graph
    # f: supermodular set function
    # alpha: tradeoff paramete
    return None, None


def ExactTGDS(G):
    tri_G = construct_triangle_graph(G)
    S_star = triangle_graph_densest_subgraph(tri_G)
    S = set()
    for u in S_star:
        triangle = tri_G.nodes[u]["tri"]
        for node in triangle:
            S.add(node)
    return G.subgraph(S)


if __name__ == "__main__":
    path = "../data/exact/"
    for file in os.listdir(path):
        dataset = file.split('.')[0]
        mes = {"datasets": dataset}
        file_name = path + file
        G = read_edgelist(file_name)
        G1 = ExactTGDS(G)
        mes.update(measure(G1))
        print(mes)