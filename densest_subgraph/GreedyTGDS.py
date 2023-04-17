import fibonacci_heap_mod

from triangle_util import get_triangles
from util import read_edgelist, measure

def GreedyTGDS(G):
    """
    Greedy Algorithm for triangle-graph densest subgraph problem
    :param G: 输入的无向图
    :return: G1:
    时间复杂度 O(m^{3/2} + t \log_{}{t} + nt)
    Reference
    --------
    Giannis Nikolentzos. "K-Clique-Graphs for Dense Subgraph Discovery" 2017
    """
    triangles = get_triangles(G)
    edge_in_triangle = {tuple(sorted(edge)): set() for edge in G.edges()}
    for i, triangle in enumerate(triangles):
        u, v, w = triangle
        edge_in_triangle[(u, v)].add(i)
        edge_in_triangle[(u, w)].add(i)
        edge_in_triangle[(v, w)].add(i)

    triangle_weight, node_weight = {}, {}
    for i, triangle in enumerate(triangles):
        triangle_weight[i] = {}
        u, v, w = triangle
        triangle_weight[i][(u, v)] = len(edge_in_triangle[(u, v)]) - 1
        triangle_weight[i][(u, w)] = len(edge_in_triangle[(u, w)]) - 1
        triangle_weight[i][(v, w)] = len(edge_in_triangle[(v, w)]) - 1
        node_weight[i] = min(triangle_weight[i].values())

    min_deg_sum, n = sum(node_weight.values()), len(triangles)
    max_triangle_density = min_deg_sum / n
    max_index = 0
    is_remove = {i: False for i in range(n)}
    remove_nodes = []

    fib_heap = fibonacci_heap_mod.Fibonacci_heap()
    # entry 记录每个顶点在fib_heap中的内存位置
    entry = {}
    for i in range(n):
        entry[i] = fib_heap.enqueue(i, node_weight[i])


    while n >= 2:
        obj = fib_heap.dequeue_min()
        i = obj.get_value()

        min_deg_sum -= node_weight[i]
        n -= 1
        is_remove[i] = True
        remove_nodes.append(i)

        u, v, w = triangles[i]

        for j in edge_in_triangle[(u, v)]:
            if is_remove[j]:
                continue
            triangle_weight[j][(u, v)] -= 1
            t = node_weight[j]
            node_weight[j] = min(triangle_weight[j].values())
            if node_weight[j] != t:
                fib_heap.decrease_key(entry[j], node_weight[j])
                min_deg_sum -= t - node_weight[j]
        for j in edge_in_triangle[(u, w)]:
            if is_remove[j]:
                continue
            triangle_weight[j][(u, w)] -= 1
            t = node_weight[j]
            node_weight[j] = min(triangle_weight[j].values())
            if node_weight[j] != t:
                fib_heap.decrease_key(entry[j], node_weight[j])
                min_deg_sum -= t - node_weight[j]
        for j in edge_in_triangle[(v, w)]:
            if is_remove[j]:
                continue
            triangle_weight[j][(v, w)] -= 1
            t = node_weight[j]
            node_weight[j] = min(triangle_weight[j].values())
            if node_weight[j] != t:
                fib_heap.decrease_key(entry[j], node_weight[j])
                min_deg_sum -= t - node_weight[j]

        density = min_deg_sum / n
        if density > max_triangle_density:
            max_triangle_density = density
            max_index = len(remove_nodes)

    # 返回三角形密度最大的三角形子图
    V1 = set(i for i in range(len(triangles))) - set(remove_nodes[:max_index])
    S = set()
    for i in V1:
        for u in triangles[i]:
            S.add(u)
    return G.subgraph(S)


if __name__ == '__main__':
    path = "../data/greedy/"
    ls = ["polblogs.txt", "as19991231.txt", "as19991213.txt", "as20000102.txt", "p2p-Gnutella24.txt",
          "p2p-Gnutella30.txt",
          "p2p-Gnutella31.txt", "com-dblp.ungraph.txt", "oregon2_010526.txt", "oregon2_010512.txt",
          "oregon2_010428.txt",
          "douban.txt", "email-Eu-core.txt", "Email-EuAll.txt", "com-youtube.ungraph.txt", "web-Stanford.txt"]
    ls = ["web-Stanford.txt"]
    # for file in os.listdir(path)
    for file in ls:
        dataset = file.split('.')[0]
        mes = {"dataset": dataset}
        file_name = path + file
        G = read_edgelist(file_name)
        G1 = GreedyTGDS(G)
        mes.update(measure(G1))
        print(mes)