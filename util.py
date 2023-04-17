import os

import networkx as nx
from triangle_util import get_triangles


def read_edgelist(file_name, separator='\t'):
    """
    从txt文件中读取创建图
    :param file_name: 文件名
    :param separator: 分隔符
    :return: G: 创建的无向图
    """
    G = nx.Graph()
    with open(file_name, "r") as f:
        for line in f:
            line = line.strip()
            if line == "" or line[0] == "#":  # 过滤掉空行和注释行
                continue
            cols = line.split(separator)
            s, t = int(cols[0]), int(cols[1])
            weight = int(cols[2]) if len(cols) > 2 else 1
            # 添加节点和边
            G.add_node(s)
            G.add_node(t)
            if s == t:  # 过滤掉自循环边
                continue
            G.add_edge(s, t, weight=weight)
    return G


def measure(G):
    """
    计算密度统计指标
    """
    n = G.number_of_nodes()
    m = G.number_of_edges()
    t = len(get_triangles(G))
    # 边密度
    edge_density = m / (n * (n - 1) / 2) if n > 1 else 0
    # 三角密度
    triangle_density = t / (n * (n - 1) * (n - 2) / 6) if n > 2 else 0
    
    return {
        "delta2": int(edge_density * 100) / 100,
        "delta4": int(triangle_density * 100) / 100,
        "subn": n
    }



def size():
    for file in os.listdir("./data/greedy/"):
        file_name = "./data/greedy/" + file
        if file.endswith("gml"):
            g = nx.read_gml(file_name)
        else:
            g = read_edgelist(file_name)

        n, m = g.number_of_nodes(), g.number_of_edges()
        t = len(get_triangles(g))
        dataset = file.split('.')[0]
        print(dataset, n, m, t)


if __name__ == '__main__':
    size()
