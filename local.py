import json
import numpy as np
from pyecharts import Graph
from pyecharts import GeoLines, Style
import csv


def readJSONFile(path):
    f = open(path, "r")
    return json.load(f)


def localNode(input_file):
    local = []
    nodes_json = readJSONFile("./data_release/topology/topology_edges_node.json")
    with open(input_file, 'r') as f:
        reader = csv.reader(f)
        result = list(reader)
    for line in result:
        print(line[3])
        local.append("node_" + line[3])

    for node in list(nodes_json):
            for son in nodes_json[node]:
                if node not in local:
                    del nodes_json[node]
                    break
                if son not in local:
                    nodes_json[node].remove(son)

    return nodes_json


def visualize(nodes_json, test_file):
    links = []
    nodes = []
    roots = []
    category = []
    count = 0

    # 获取局部根因roots
    with open(test_file, 'r') as f:
        reader = csv.reader(f)
        result = list(reader)
        for i in result:
            if i[4] == '1':
                roots.append(i[3])

    for node in nodes_json:
        symbolSize = 5  #普通节点大小
        for root in roots:
            if node.split('_')[1] == root:
                symbolSize = 20   # 根因节点大小
        nodes.append({"name": node, "symbolSize": symbolSize})  # 关系图结点
        # print(nodes)
        for son in nodes_json[node]:
            links.append({"source": node, "target": son})  # 结点间的关系数据
        # print(links)
    graph = Graph("局部可视化", width=1960, height=1080)
    print(nodes)
    print(links)
    graph.add("",
              nodes,
              links,
              label_color=['#ff0000'],
              label_text_color="#0000ff",
              geo_effect_symbol="plane",
              geo_effect_symbolsize=15,
              is_focusnode=False,  # 是否在鼠标移到节点上的时候突出显示节点以及节点的边和邻接节点
              is_roam=True,
              layout="force",  # 布局类型，默认force=力引导图，circular=环形布局
              edge_length=400,  # 力布局下边的两个节点之间的距离
              gravity=0.5,  # 点受到的向中心的引力因子。
              repulsion=200,
              is_label_show=True,
              line_curve=0,
              )
    graph.render(r"./local.html")
    print("visualized done")


if __name__ == '__main__':
    json_file = "data_release/topology/topology_edges_node.json"
    test_file = "./tf00/0.csv"
    new_node = localNode("./tf00/0.csv")
    visualize(new_node, test_file)
