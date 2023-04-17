
def get_triangles(G):
    """
    Algorithm 6 – forward
    时间复杂度$O(m ^ {3/2})$
    Reference
    --------
    Matthieu Latapy "Main-memory triangle computations for very large (sparse (power-law)) graphs." 2008
    """
    triangles = []
    ls = sorted(list(G.nodes), key=lambda x: -len(G.adj[x]))
    order = {node: i for i, node in enumerate(ls)}
    A = {node: set() for node in G.nodes()}
    for v in ls:
        for u in G.adj[v]:
            if order[u] > order[v]:
                for w in A[u] & A[v]:
                    triangles.append(tuple(sorted([u, v, w])))
                A[u].add(v)
    return triangles


def get_triangle_node_weight(G, triangles):
    """
    求每个triangle和节点的权重
    triangle 权重为其参与的4-clique个数
    node 权重为其参与triangle权重之和
    """
    edge_adj_nodes = get_edge_adj_nodes(G, triangles)
    
    triangle_weight = {}
    for triangle in triangles:
        u, v, w = triangle
        node_set1 = edge_adj_nodes[(u, v)]
        node_set2 = edge_adj_nodes[(u, w)]
        node_set3 = edge_adj_nodes[(v, w)]
        
        # 公共顶点集大小，即为triangle参与4-clique的个数
        nodes = node_set1 & node_set2 & node_set3
        triangle_weight[triangle] = len(nodes)

    node_weight = {node: 0 for node in G.nodes()}
    for triangle in triangles:
        for node in triangle:
            node_weight[node] += triangle_weight[triangle]
    return triangle_weight, node_weight


def get_node_adj_edges(G, triangles):
    """
    计算与顶点构成triangle的边的集合
    """
    node_adj_edges = {node: set() for node in G.nodes()}
    for triangle in triangles:
        u, v, w = triangle
        node_adj_edges[u].add((v, w))
        node_adj_edges[v].add((u, w))
        node_adj_edges[w].add((u, v))
    return node_adj_edges


def get_edge_adj_nodes(G, triangles):
    """
    计算与边构成triangle的顶点的集合
    """
    edge_adj_nodes = {tuple(sorted(edge)): set() for edge in G.edges()}
    for triangle in triangles:
        u, v, w = triangle
        edge_adj_nodes[(u, v)].add(w)
        edge_adj_nodes[(u, w)].add(v)
        edge_adj_nodes[(v, w)].add(u)
    return edge_adj_nodes
