from anytree import Node, RenderTree, AsciiStyle, PostOrderIter, PreOrderIter, LevelOrderIter
from anytree.exporter import DotExporter
import subprocess
import random

num = 0
depth = 0
root = Node(name=num, list1=list())
num += 1
right = Node(name=num, list1=list(), parent=root)
num += 1
middle = Node(name=num, list1=list(), parent=root)
num += 1
left = Node(name=num, list1=list(), parent=root)

flag = 0
while flag == 0:
    for children in PostOrderIter(root):
        if children.is_leaf:
            if children.depth == 4:
                flag = 1
                break
            else:
                continue
        else:
            break

    if flag == 1:
        break

    for children in PostOrderIter(root, maxlevel=4):
        if children.is_leaf:
            random_number = random.randint(0, 1)
            if random_number == 1:
                for i in range(3):
                    num += 1
                    Node(name=num, list1=list(), parent=children)


def nodenamefunc(node):
    return '%s:%s:%s' % (node.name, node.list1, node.depth)


for children in PostOrderIter(root):
    if children.is_leaf:
        list_rand = random.sample(range(0, 15), 3)
        children.list1.append(list_rand)

# for line in DotExporter(root, graph="graph", nodenamefunc=nodenamefunc):
#                      print(line)

k = [[2, 3, 4]]
print(k[0])

for children in PreOrderIter(root):
    if children.depth == 3 and children.is_leaf == False:
        # print(children.name)
        child1 = children.children[0]
        num1 = child1.list1[0][0]
        child2 = children.children[1]
        num2 = child2.list1[0][0]
        child3 = children.children[2]
        num3 = child3.list1[0][0]
        max_num = max(num1, num2, num3)
        # print("max_num=", max_num)
        if max_num == num1:
            children.list1.append(child1.list1[0])
            # print("list1_num1=",children.list1)
        if max_num == num2:
            children.list1.append(child2.list1[0])
            # print("list1_num2=",children.list1)
        if max_num == num3:
            children.list1.append(child3.list1[0])
            # print("list1_num3=",children.list1)

# DotExporter(root, nodenamefunc=nodenamefunc).to_dotfile("tree3.dot")
# subprocess.call(['C:\\Program Files\\Graphviz\\bin\\dot.exe', 'tree3.dot', '-T', 'jpg', '-o',
#               'C:\\МГТУ\\ТеорияИгр\\lab4-py\\root3.jpg'])
# a=[[5,1,1],[5,1,3]]
# print(a[0][0])


for children in PreOrderIter(root):
    temp_list1 = []
    temp_list2 = []
    temp_list3 = []
    max1 = max2 = max3 = 0
    if children.depth == 2 and children.is_leaf == False:
        # print(children.name)
        child1 = children.children[0]
        if isinstance(child1.list1[0], list) and len(child1.list1) >= 1:
            for i in range(len(child1.list1)):
                temp_list1.append(child1.list1[i][2])
                max1 = max(temp_list1)
        # else:
        # num1 = child1.list1[0][2]
        child2 = children.children[1]
        if isinstance(child2.list1[0], list) and len(child2.list1) >= 1:
            for i in range(len(child2.list1)):
                temp_list2.append(child2.list1[i][2])
                max2 = max(temp_list2)
        # else:
        # num2 = child2.list1[0][2]
        child3 = children.children[2]
        if isinstance(child3.list1[0], list) and len(child3.list1) >= 1:
            for i in range(len(child3.list1)):
                temp_list3.append(child3.list1[i][2])
                max3 = max(temp_list3)
        # else:
        # num3 = child3.list1[0][2]
        max_num = max(max1, max2, max3)
        # print("max_num=", max_num)
        if max_num == max1:
            if isinstance(child1.list1[0], list) and len(child1.list1) >= 1:
                for i in range(len(child1.list1)):
                    if max_num in child1.list1[i]:
                        children.list1.append(child1.list1[i])
            else:
                children.list1.append(child1.list1)
            # print("list1_num1=",children.list1)
        if max_num == max2:
            if isinstance(child2.list1[0], list) and len(child2.list1) >= 1:
                for i in range(len(child2.list1)):
                    if max_num in child2.list1[i]:
                        children.list1.append(child2.list1[i])
            else:
                children.list1.append(child2.list1)
            # print("list1_num2=",children.list1)
        if max_num == max3:
            if isinstance(child3.list1[0], list) and len(child3.list1) >= 1:
                for i in range(len(child3.list1)):
                    if max_num in child3.list1[i]:
                        children.list1.append(child3.list1[i])
            else:
                children.list1.append(child3.list1)
            # print("list1_num3=",children.list1)


for children in PreOrderIter(root):
    temp_list1 = []
    temp_list2 = []
    temp_list3 = []
    max1 = max2 = max3 = 0
    if children.depth == 1 and children.is_leaf == False:
        # print(children.name)
        child1 = children.children[0]
        if isinstance(child1.list1[0], list) and len(child1.list1) >= 1:
            for i in range(len(child1.list1)):
                temp_list1.append(child1.list1[i][1])
                max1 = max(temp_list1)
        # else:
        # num1 = child1.list1[0][2]
        child2 = children.children[1]
        if isinstance(child2.list1[0], list) and len(child2.list1) >= 1:
            for i in range(len(child2.list1)):
                temp_list2.append(child2.list1[i][1])
                max2 = max(temp_list2)
        # else:
        # num2 = child2.list1[0][2]
        child3 = children.children[2]
        if isinstance(child3.list1[0], list) and len(child3.list1) >= 1:
            for i in range(len(child3.list1)):
                temp_list3.append(child3.list1[i][1])
                max3 = max(temp_list3)
        # else:
        # num3 = child3.list1[0][2]
        max_num = max(max1, max2, max3)
        # print("max_num=", max_num)
        if max_num == max1:
            if isinstance(child1.list1[0], list) and len(child1.list1) >= 1:
                for i in range(len(child1.list1)):
                    if max_num in child1.list1[i]:
                        children.list1.append(child1.list1[i])
            else:
                children.list1.append(child1.list1)
            # print("list1_num1=",children.list1)
        if max_num == max2:
            if isinstance(child2.list1[0], list) and len(child2.list1) >= 1:
                for i in range(len(child2.list1)):
                    if max_num in child2.list1[i]:
                        children.list1.append(child2.list1[i])
            else:
                children.list1.append(child2.list1)
            # print("list1_num2=",children.list1)
        if max_num == max3:
            if isinstance(child3.list1[0], list) and len(child3.list1) >= 1:
                for i in range(len(child3.list1)):
                    if max_num in child3.list1[i]:
                        children.list1.append(child3.list1[i])
            else:
                children.list1.append(child3.list1)
            # print("list1_num3=",children.list1)

for children in LevelOrderIter(root):
    temp_list1 = []
    temp_list2 = []
    temp_list3 = []
    max1 = max2 = max3 = 0
    if children.depth == 0 and children.is_leaf == False:
        # print(children.name)
        child1 = children.children[0]
        if isinstance(child1.list1[0], list) and len(child1.list1) >= 1:
            for i in range(len(child1.list1)):
                temp_list1.append(child1.list1[i][0])
                max1 = max(temp_list1)
        # else:
        # num1 = child1.list1[0][2]
        child2 = children.children[1]
        if isinstance(child2.list1[0], list) and len(child2.list1) >= 1:
            for i in range(len(child2.list1)):
                temp_list2.append(child2.list1[i][0])
                max2 = max(temp_list2)
        # else:
        # num2 = child2.list1[0][2]
        child3 = children.children[2]
        if isinstance(child3.list1[0], list) and len(child3.list1) >= 1:
            for i in range(len(child3.list1)):
                temp_list3.append(child3.list1[i][0])
                max3 = max(temp_list3)
        # else:
        # num3 = child3.list1[0][2]
        max_num = max(max1, max2, max3)
        # print("max_num=", max_num)
        if max_num == max1:
            if isinstance(child1.list1[0], list) and len(child1.list1) >= 1:
                for i in range(len(child1.list1)):
                    if max_num in child1.list1[i]:
                        children.list1.append(child1.list1[i])
            else:
                children.list1.append(child1.list1)
            # print("list1_num1=",children.list1)
        if max_num == max2:
            if isinstance(child2.list1[0], list) and len(child2.list1) >= 1:
                for i in range(len(child2.list1)):
                    if max_num in child2.list1[i]:
                        children.list1.append(child2.list1[i])
            else:
                children.list1.append(child2.list1)
            # print("list1_num2=",children.list1)
        if max_num == max3:
            if isinstance(child3.list1[0], list) and len(child3.list1) >= 1:
                for i in range(len(child3.list1)):
                    if max_num in child3.list1[i]:
                        children.list1.append(child3.list1[i])
            else:
                children.list1.append(child3.list1)
            # print("list1_num3=",children.list1)
    else:
        break

DotExporter(root, nodenamefunc=nodenamefunc).to_dotfile("tree1.dot")

subprocess.call(['C:\\Program Files\\Graphviz\\bin\\dot.exe', 'tree1.dot', '-T', 'jpg', '-o',
                 'C:\\МГТУ\\ТеорияИгр\\lab4-py\\root1.jpg'])
