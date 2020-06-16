import json
import numpy as np
from pyecharts import Graph
import csv


def readJSONFile(path):
    f = open(path, "r")
    return json.load(f)


def visualize():
    links = []
    nodes = []
    nodes_json = readJSONFile("data_release/topology/topology_edges_node.json")

    for node in nodes_json:
        nodes.append({"name": node, "symbolSize": 10})
        for son in nodes_json[node]:
            links.append({"source": node, "target": son})

    print(nodes)
    graph = Graph("整体可视化", width=1960, height=1080)
    graph.add("",
              nodes,
              links,
              is_focusnode=True,  # 是否在鼠标移到节点上的时候突出显示节点以及节点的边和邻接节点
              is_roam=True,
              layout="force",  # 布局类型，默认force=力引导图，circular=环形布局
              edge_length=400,  # 力布局下边的两个节点之间的距离
              gravity=0.1,  # 点受到的向中心的引力因子
              repulsion=200,
              is_label_show=False,
              line_curve=0,

              )
    graph.render(r"./full.html")
    print("visualized done")


if __name__ == '__main__':
    visualize()
