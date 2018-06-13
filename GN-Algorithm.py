'''
Created on 2018-06-01
@Original author: Chuang YANG
@Edit by: Chuang YANG
'''
import math
class Node:

    def __init__(self,id):
        self.id = id
        self.parents = []
        self.childs = []
        self.edges = dict()
        self.credit = 0
        self.layer = 0
        self.numOfShortestPath = 0

    def addParent(self, parent):
        self.parents.append(parent)  # by default, edge credits is zero

    def addChild(self, child):
        self.childs.append(child)


    def setLayer(self):
        if self.parents:
            node = self.parents[0]
            self.layer = 1
            while(node.parents):
                node = node.parents[0]
                self.layer += 1
            return self.layer
        else:
            return 0
    def getLayer(self):
        return self.layer

    def getParentNum(self):
        if self.parents :
            return len(self.parents)
        else : # root node
            return 1

    def getChildNum(self):
        return len(self.childs)

    def setCredit(self,credit):
        self.credit = credit

    def getCredit(self):
        return self.credit

    def get_num_of_shorest_path(self):
        return self.numOfShortestPath
    def set_num_of_shorest_path(self):
        if self.parents:
           for item in self.parents:
               self.numOfShortestPath += item.get_num_of_shorest_path()
        else:
           self.numOfShortestPath = 1

        return self.numOfShortestPath
"""
read a txt/csv/others files to build a graph
"""
def buildGraph(filename):
    graph = {}
    try:
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip("\n").split(" ")
                line = list(map(int, line))  # map 映射进行类型转换
                graph[line[0]] = line[1:]

    except IOError:
        if filename:
            print("I/O Error,invaild filename!")
        else:
            print("I/O Error,xxx")
    else:
        print("reading file successfully！")
    return graph

"""
use bfs to build a tree from graph
"""
def breadFirstSearch(root,graph):
    # initial root Node
    root_node = Node(root)
    queue = [root_node]  # put root Node in queue
    visited_node_list = [root_node]
    visited_id_dict = {root: root_node}  # use hash set to accelerate query

    while queue:
        # pop parent node
        node = queue.pop(0)
        # set node's layer
        node.setLayer()
        # calculate the number of shortest path from root to each node

        # get parent node's childList
        child_list = graph[node.id]
        for childID in child_list:
            # judge if a child id is visited by other earlier pop node
            if visited_id_dict.get(childID):
                # get this visited Node
                temp = visited_id_dict.get(childID)
                # get this Node's layer
                temp.setLayer()
                # if this Node's layer is deeper than current pop node,
                if node.getLayer() < temp.getLayer():
                    node.addChild(temp)
                    temp.addParent(node)
            else:
                # put child Node in queue
                child = Node(childID)
                queue.append(child)
                # put child Node in visited set and visited list
                visited_id_dict[childID] = child
                visited_node_list.append(child)
                # set parent and child relationship
                node.addChild(child)
                child.addParent(node)

    return visited_node_list

"""
for each node in graph ,calculate the num of shorest path from root to it.
"""
def set_num_of_shorest_path_lable(tree):
    # in this tree, the traverse order if form lower layer to high layer
    for node in tree:
        node.set_num_of_shorest_path()
    return tree

"""
for each node, calculate the edge's credit, which these edges connect this node and its parents 
"""
def update_edge_credit(node):
    # calculate the sum of currentNode parents' shortest path num
    total_num = 0
    for Y in node.parents:
        total_num += Y.get_num_of_shorest_path()
    # calculate leaf node's upper edge's credit
    for Y in node.parents:
        edge_credit = (Y.get_num_of_shorest_path() / total_num) * node.credit
        # set edge credit
        node.edges[Y.id] = edge_credit
        Y.edges[node.id] = edge_credit


def GN(graph,root):
    # build tree from graph
    tree = breadFirstSearch(root,graph)
    # set num of shortest path lable
    labled_tree = set_num_of_shorest_path_lable(tree)
    # select the last node as start node
    length = len(labled_tree)
    current_node = labled_tree[length-1]

    i = length - 1
    while i >= 0:
        # current node is a left node
        if current_node.getChildNum() == 0:
            current_node.setCredit(1)
            update_edge_credit(current_node)

        # if current node is not a leaf node
        else:
            # calculate this node's credit
            credit = 1
            for C in current_node.childs:
                credit += current_node.edges[C.id]
            current_node.setCredit(credit)
            update_edge_credit(current_node)
        next_node = labled_tree[i]
        current_node = next_node
        i -= 1
    for x in labled_tree:
        print("NodeID", x.id, "NodeCredit", x.credit, "edgeCredit",x.edges)



def neighbor_profile(graph,root):
    tree = breadFirstSearch(root, graph)
    temp_result= {}
    result = {}
    for x in tree:
        x.setLayer()
        if(temp_result.get(x.layer)):
            temp_result[x.layer]+=1
        else:
            temp_result[x.layer] = 1
    result[0] = temp_result[0]
    for x in range(1,len(tree)):
        if(temp_result.get(x)):
            result[x] = result[x-1] + temp_result[x]
        else:
            result[x] = result[x-1]
    for k, v in result.items():
        print("|N("+str(root)+","+str(k)+")|="+str(v))
def graph_diameter(graph):
    max = 0
    for x in graph:
        tree = breadFirstSearch(x, graph)
        tree[len(tree)-1].setLayer()
        layer = tree[len(tree)-1].layer
        if layer>max:
            max = layer

    return max
def graph_transitive_closure_pair_num(graph):
    return (len(graph)-1)*len(graph)
def round_num_with_recursive_doubling(graph):
    diameter = graph_diameter(graph)
    result = math.log(diameter,2)
    return math.ceil(result)

def main():
    graph = buildGraph("social_network_test")
    # 实验一        计算边最短路径数目
    print("root is:",1)
    GN(graph, 1)
    print("root is:", 2)
    GN_core(graph, 2)
    # 实验二 第一问， 计算邻居的描述
    neighbor_profile(graph, 1)
    neighbor_profile(graph, 2)
    # 实验二 第二问， 计算图的直径
    diameter = graph_diameter(graph)
    print("the diameter of graph is:", diameter)
    # 实验二 第三问， 计算图的传递闭包节点对数目，双重递归计算传递闭包的循环次数
    pair_num = graph_transitive_closure_pair_num(graph)
    print("the transitive closure pair number of graph is:", pair_num)
    recursive_num = round_num_with_recursive_doubling(graph)
    print("the round num is:",recursive_num)
if __name__ == "__main__":
    main()







