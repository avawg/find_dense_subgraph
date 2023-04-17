from triangle_util import get_triangles
from util import read_edgelist, measure
import fibonacci_heap_mod

def GreedyMWED(G):
    """
    Greedy Algorithm for MWED
    :return:
    时间复杂度$O(m^{3/2} + t + n\log_{}{n})$ 边权重为参与三角形的个数
    时间复杂度$O(m + n\log_{}{n})$ 正常边权重
    Reference
    --------
    Jiabing W. "Finding Dense Subgraphs with Maximum Weighted Triangle Density." 2020
    """
    triangles = get_triangles(G)
    # 计算边和顶点的权重
    edge_weight = {} # 边权重
    # for edge in G.edges():
    #     edge_weight[edge] = G.edges[edge]["weight"]  # 边权重
    for edge in G.edges():
        u, v = edge
        edge_weight[tuple(sorted((u, v)))] = 0
    for triangle in triangles:
        u, v, w = triangle
        edge_weight[(u, v)] += 1
        edge_weight[(u, w)] += 1
        edge_weight[(v, w)] += 1

    node_weight = {node: 0 for node in G.nodes()} # 节点权重
    for edge in G.edges():
        u, v = sorted(edge)
        node_weight[u] += edge_weight[(u, v)]
        node_weight[v] += edge_weight[(u, v)]

    n = G.number_of_nodes()
    edge_weight_sum = sum(edge_weight.values())

    fib_heap = fibonacci_heap_mod.Fibonacci_heap()
    # entry 记录每个顶点在fib_heap中的内存位置
    entry = {}
    for node in G.nodes():
        entry[node] = fib_heap.enqueue(node, node_weight[node])
    
    # 记录最大的加权边密度及下标
    max_weighted_edge_density, max_density_index = edge_weight_sum / n, 0
    remove_nodes = []
    is_remove = {node: False for node in G.nodes()}
    
    while n >= 3:
        # removes the vertex u with the smallest edges weight sum
        obj = fib_heap.dequeue_min()
        u = obj.get_value()
        
        n -= 1
        is_remove[u] = True
        remove_nodes.append(u)
        for v in G.adj[u]:
            if is_remove[v]:
                continue
            edge = tuple(sorted((u, v)))
            edge_weight_sum -= edge_weight[edge]

            # 更新v节点
            node_weight[v] -= edge_weight[edge]
            fib_heap.decrease_key(entry[v], node_weight[v])
                
        weighted_edge_density = edge_weight_sum / n
        if weighted_edge_density > max_weighted_edge_density:
            max_weighted_edge_density = weighted_edge_density
            max_density_index = len(remove_nodes)
    
    # 返回加权边密度最大时的子图
    V1 = set(G.nodes) - set(remove_nodes[:max_density_index])
    return G.subgraph(V1)


if __name__ == '__main__':
    path = "data/greedy/"
    ls = ["polblogs.txt", "as19991231.txt", "as19991213.txt", "as20000102.txt", "p2p-Gnutella24.txt",
          "p2p-Gnutella30.txt",
          "p2p-Gnutella31.txt", "com-dblp.ungraph.txt", "oregon2_010526.txt", "oregon2_010512.txt",
          "oregon2_010428.txt",
          "douban.txt", "email-Eu-core.txt", "Email-EuAll.txt", "com-youtube.ungraph.txt", "web-Stanford.txt"]
    # for file in os.listdir(path)
    for file in ls:
        dataset = file.split('.')[0]
        mes = {"dataset": dataset}
        file_name = path + file
        G = read_edgelist(file_name)
        G1 = GreedyMWED(G)
        mes.update(measure(G1))
        print(mes)
