import fibonacci_heap_mod
from util import measure, read_edgelist
from triangle_util import *


def GreedyMWTD(G):
    """
    Greedy Algorithm for MWTD
    :return: subG: subgraph with max Weighted triangle density
    时间复杂度$O(m^{3/2} + nt + nlog_{}{n})$，近似比1/3
    Reference
    --------
    Jiabing W. "Finding Dense Subgraphs with Maximum Weighted Triangle Density." 2020
    """
    # the set of triangles
    triangles = get_triangles(G)
    triangle_weight, node_weight = get_triangle_node_weight(G, triangles)
    # 删除点时遍历节点所属的triangle
    node_adj_edges = get_node_adj_edges(G, triangles)

    triangle_weight_sum = sum(triangle_weight.values())

    fib_heap = fibonacci_heap_mod.Fibonacci_heap()
    # entry 记录每个顶点在fib_heap中的内存位置
    entry = {}
    for node in G.nodes():
        entry[node] = fib_heap.enqueue(node, node_weight[node])
    
    # 记录最大的加权三角密度及下标
    n = G.number_of_nodes()
    max_weighted_triangle_density = triangle_weight_sum / n
    max_density_index = 0
    remove_nodes = []
    is_remove = {node: False for node in G.nodes()}
    
    while n >= 4:
        # removes the vertex u with the smallest triangle weight sum
        obj = fib_heap.dequeue_min()
        u = obj.get_value()
        
        n -= 1
        is_remove[u] = True
        remove_nodes.append(u)

        for edge in node_adj_edges[u]:
            # 判断triangle是否已经被删除
            if is_remove[edge[0]] or is_remove[edge[1]]:
                continue
            triangle = tuple(sorted((u, edge[0], edge[1])))
            triangle_weight_sum -= triangle_weight[triangle]
            for node in edge:
                node_weight[node] -= triangle_weight[triangle]
                fib_heap.decrease_key(entry[node], node_weight[node])
        
        weighted_triangle_density = triangle_weight_sum / n
        
        if weighted_triangle_density > max_weighted_triangle_density:
            max_weighted_triangle_density = weighted_triangle_density
            max_density_index = len(remove_nodes)
    
    # 返回加权三角密度最大的子图
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
        G1 = GreedyMWTD(G)
        mes.update(measure(G1))
        print(mes)
