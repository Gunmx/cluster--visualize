import csv
import json
import sys
import numpy as np


class Solution:
    def __init__(self):
        self.nodes = []
        self.graph = readJSONFile("./data_release/topology/topology_edges_node.json")
        for i in self.graph:
            self.nodes.append(i)

    def bfs_path(self, start, end):
        queue = []  # 路径队列
        fail = 0
        queue.append([start])  # 入列
        while queue:
            fail = fail + 1
            if fail >= 100000:
                # print("Search Failed\n")
                return
            # 取出队头元素
            path = queue.pop(0)
            # 取出path最后一个节点
            node = path[-1]
            # 路径找到
            if node == end:
                return path
            # 遍历node的邻接节点, 并把新的路径入列
            # print(self.graph.get(node, []))
            for adjacent in self.graph.get(node, []):
                new_path = list(path)
                new_path.append(adjacent)
                queue.append(new_path)

    def bfs(self):
        from collections import deque
        queue = deque()
        visited = set()
        for key in self.graph.keys():
            if key not in visited:
                queue.append(key)
                visited.add(key)
            while len(queue) > 0:
                tmp = queue.popleft()
                print(tmp, end='\t')
                if tmp not in self.graph:
                    break
                for value in self.graph[tmp]:
                    if value not in visited:
                        queue.append(value)
                        visited.add(value)


def readJSONFile(path):
    f = open(path, "r")
    return json.load(f)


def readCSVFile(path):
    file = open(path, 'r')
    return csv.reader(file)


def cluster():
    root = []; nodes = []; content = list(readCSVFile("./tf01/0.csv"))
    for line in content:
        nodes.append(line[2])
        if line[3] == '1':
            root.append(line[2])
    root = list(set(root))
    nodes = list(set(nodes))
    print('\n---根因与告警节点---')
    print(root, nodes)
    s = Solution(); delete = []; result = list()
    for i in root:
        for j in nodes:
            source = 'node_' + i
            target = 'node_' + j
            print('\n{}--->{}'.format(source, target))
            result = s.bfs_path(source, target)
            print(result)
            if result is not None:
                if len(result) > 3:
                    delete.append(j)
    return delete


if __name__ == "__main__":
    s = Solution()
    print("BFS")
    s.bfs()
    # s.bfs_path("node_60", "node_16")
    print(cluster())
