# 加载原图
import networkx as nx
from matplotlib import pyplot as plt

import matplotlib as mpl

from ExactMWKD import maximum_weighted_kclique_density

mpl.use('TkAgg')

if __name__ == '__main__':

    G = nx.read_gml('lesmis.gml', label='id')
    # 计算子图
    subgraph = maximum_weighted_kclique_density(G)

    for u in subgraph:
        print(u, G.nodes[u])
    # 设置节点位置
    pos = nx.spring_layout(G)
    # 创建绘图区域和子图
    fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(6, 4))
    # 绘制原图
    nx.draw_networkx(G, pos=pos, with_labels=True,  ax=axs[0])
    axs[0].set_title('G')

    # 绘制子图
    nx.draw_networkx(subgraph, pos=pos, with_labels=True,  ax=axs[1])
    axs[1].set_title('subG')
    # 显示图形
    plt.show()
