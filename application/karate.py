# 加载原图
import networkx as nx
from matplotlib import pyplot as plt

import matplotlib as mpl
mpl.use('TkAgg')

from ExactMWKD import maximum_weighted_kclique_density


if __name__ == '__main__':

    G = nx.karate_club_graph()

    # 计算子图
    subgraph = maximum_weighted_kclique_density(G)

    # 设置节点位置
    pos = nx.spring_layout(G)
    # 创建绘图区域和子图
    fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(6, 4))

    nx.draw(G, pos=pos, with_labels=True, ax=axs[0])
    axs[0].set_title('G')

    # 绘制子图
    nx.draw(subgraph, pos=pos, with_labels=True, ax=axs[1])
    axs[1].set_title('subG')

    # 显示图形
    plt.show()

