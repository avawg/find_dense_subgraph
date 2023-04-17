import fibonacci_heap_mod
from util import measure, read_edgelist
from triangle_util import *


def GreedyTDS(G):
    """
    TDS贪心算法时间复杂度$O(m^{3/2} + n\log_{}{n} + t)$，近似比 1/3
    :param G:
    :return: G1: subgraph with max average triangle degree
    Reference
    --------
    Tsourakakis C. "The K-clique Densest Subgraph Problem." 2015
    """
    # the set of triangles
    triangles = get_triangles(G)
    triangle_degree = {node: 0 for node in G.nodes()}
    for triangle in triangles:
        for node in triangle:
            triangle_degree[node] += 1
    # 删除点时遍历triangle
    node_adj_edges = get_node_adj_edges(G, triangles)

    n, t = G.number_of_nodes(), len(triangles)

    fib_heap = fibonacci_heap_mod.Fibonacci_heap()
    # entry 记录每个顶点在fib_heap中的内存位置
    entry = {}
    for node in G.nodes():
        entry[node] = fib_heap.enqueue(node, triangle_degree[node])

    # 记录最大的平均三角度及下标
    max_average_triangle_degree = t / n
    max_index = 0
    remove_nodes = []
    is_remove = {node: False for node in G.nodes()}

    while n >= 4:
        # removes the vertex u with the smallest triangle degree
        obj = fib_heap.dequeue_min()
        u = obj.get_value()

        n -= 1
        is_remove[u] = True
        remove_nodes.append(u)

        for edge in node_adj_edges[u]:
            # 判断triangle是否已经被删除
            if is_remove[edge[0]] or is_remove[edge[1]]:
                continue
            t -= 1
            for node in edge:
                triangle_degree[node] -= 1
                fib_heap.decrease_key(entry[node], triangle_degree[node])

        average_triangle_degree = t / n

        if average_triangle_degree > max_average_triangle_degree:
            max_average_triangle_degree = average_triangle_degree
            max_index = len(remove_nodes)

    # 返回平均三角度最大的子图
    V1= set(G.nodes) - set(remove_nodes[:max_index])
    return G.subgraph(V1)


if __name__ == '__main__':
    path = "../data/greedy/"
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
        G1 = GreedyTDS(G)
        mes.update(measure(G1))
        print(mes)