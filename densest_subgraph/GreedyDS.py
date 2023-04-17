from util import read_edgelist, measure


def GreedyDS(G):
    """
    Greedy Algorithm for densest subgraph problem
    :param G: 输入的无向图
    :return: G1: subgraph with max average degree
    时间复杂度 O(n + m)，近似比 1/2
    Reference
    --------
    Charikar M. "Greedy Approximation Algorithms for Finding Dense Components in a Graph." 2000
    """
    degree = {node: len(G.adj[node]) for node in G.nodes()}
    n, m = G.number_of_nodes(), G.number_of_edges()

    ls = [set() for _ in range(n)]
    for u in G.nodes():
        d = degree[u]
        ls[d].add(u)

    # 记录最大的平均边度及下标
    max_average_degree = m / n
    max_index = 0
    remove_nodes = []
    is_remove = {node: False for node in G.nodes()}

    mind = 0
    while n >= 2:
        # 寻找度数最小的节点
        while len(ls[mind]) == 0:
            mind += 1
        u = ls[mind].pop()

        n -= 1
        is_remove[u] = True
        remove_nodes.append(u)
        # 删除u为顶点的边
        for v in G.adj[u]:
            if is_remove[v]:
                continue
            # 更新节点v的degree值
            m -= 1
            d = degree[v]
            ls[d].remove(v)
            ls[d - 1].add(v)
            degree[v] = d - 1
            mind = min(mind, d - 1)

        average_degree = m / n
        if average_degree > max_average_degree:
            max_average_degree = average_degree
            max_index = len(remove_nodes)

    # 返回平均边度最大的子图
    V1 = set(G.nodes) - set(remove_nodes[:max_index])
    return G.subgraph(V1)


if __name__ == '__main__':
    path = "../data/greedy/"
    ls = ["polblogs.txt", "as19991231.txt", "as19991213.txt", "as20000102.txt", "p2p-Gnutella24.txt", "p2p-Gnutella30.txt",
          "p2p-Gnutella31.txt", "com-dblp.ungraph.txt", "oregon2_010526.txt", "oregon2_010512.txt", "oregon2_010428.txt",
          "douban.txt", "email-Eu-core.txt", "Email-EuAll.txt", "com-youtube.ungraph.txt", "web-Stanford.txt"]
    # for file in os.listdir(path)
    for file in ls:
        dataset = file.split('.')[0]
        mes = {"dataset": dataset}
        file_name = path + file
        G = read_edgelist(file_name)
        G1 = GreedyDS(G)
        mes.update(measure(G1))
        print(mes)