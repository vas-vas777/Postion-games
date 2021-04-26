from anytree import Node, RenderTree, AsciiStyle, PostOrderIter, PreOrderIter, LevelOrderIter
from anytree.exporter import DotExporter
import subprocess
import random

num = 0 # для обозначения номера вершины
#depth = 0 #
# создание корня и трёх детей
root = Node(name=num, list1=list())
num += 1
right = Node(name=num, list1=list(), parent=root)
num += 1
middle = Node(name=num, list1=list(), parent=root)
num += 1
left = Node(name=num, list1=list(), parent=root)

flag = 0 # остановка алгоритма генерации дерева до глубины 5 (в коде 4)
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

    for children in PostOrderIter(root, maxlevel=4):  # случайный выбор продолжать веришну вниз или нет
        if children.is_leaf:
            random_number = random.randint(0, 1)
            if random_number == 1:
                for i in range(3):
                    num += 1
                    Node(name=num, list1=list(), parent=children)


def nodenamefunc(node):
    return '%s:%s:%s' % (node.name, node.list1, node.depth)  # вывод в узлах (номер вершины, значение выиграшей
    # и текущая глубина узла)


for children in PostOrderIter(root): # заполнение листов случаным вектором из 3 чисел
    if children.is_leaf:
        list_rand = random.sample(range(0, 15), 3)
        children.list1.append(list_rand)

for children in PreOrderIter(root): # обход с вершины 3 и посещение её детей
    if children.depth == 3 and children.is_leaf == False:
        # print(children.name)
        child1 = children.children[0]
        num1 = child1.list1[0][0]
        child2 = children.children[1]
        num2 = child2.list1[0][0]
        child3 = children.children[2]
        num3 = child3.list1[0][0]
        max_num = max(num1, num2, num3)
        # print("max_num=", max_num) выбор максимального выигрыша у игрока 1
        if max_num == num1:
            children.list1.append(child1.list1[0])
            # print("list1_num1=",children.list1)
        if max_num == num2:
            children.list1.append(child2.list1[0])
            # print("list1_num2=",children.list1)
        if max_num == num3:
            children.list1.append(child3.list1[0])
            # print("list1_num3=",children.list1)

# print([2, 11] > [9])

for children in PreOrderIter(root): # обход со второго уровня и посещение детей
    temp_list1 = [] # временный список для сбора всех значений i-го игрока из всех списков 1 ребёнка
    temp_list2 = []
    temp_list3 = []
    max1 = max2 = max3 = 0 # значения макс и миним элементов списков 
    min1 = min2 = min3 = 0
    if children.depth == 2 and children.is_leaf == False:
        # print(children.name)
        child1 = children.children[0]
        if isinstance(child1.list1[0], list) and len(child1.list1) >= 1:
            for i in range(len(child1.list1)):
                temp_list1.append(child1.list1[i][2])
                max1 = max(temp_list1)
                min1 = min(temp_list1)
        # else:
        # num1 = child1.list1[0][2]
        child2 = children.children[1]
        if isinstance(child2.list1[0], list) and len(child2.list1) >= 1:
            for i in range(len(child2.list1)):
                temp_list2.append(child2.list1[i][2])
                max2 = max(temp_list2)
                min2 = min(temp_list2)
        # else:
        # num2 = child2.list1[0][2]
        child3 = children.children[2]
        if isinstance(child3.list1[0], list) and len(child3.list1) >= 1:
            for i in range(len(child3.list1)):
                temp_list3.append(child3.list1[i][2])
                max3 = max(temp_list3)
                min3 = min(temp_list3)

        max_max_num = max(max1, max2, max3)
        max_min_num = min(min1, min2, min3)
        # случай когда в каждой вершине по одному списку
        if len(temp_list3) == 1 and len(temp_list2) == 1 and len(temp_list1) == 1: # случай когда все списки
            if max_max_num == max1:
                if isinstance(child1.list1[0], list) and len(child1.list1) >= 1:
                    for i in range(len(child1.list1)):
                        if max_max_num in child1.list1[i]:
                            children.list1.append(child1.list1[i])
                # else:
                # children.list1.append(child1.list1)
                # print("list1_num1=",children.list1)
            if max_max_num == max2:
                if isinstance(child2.list1[0], list) and len(child2.list1) >= 1:
                    for i in range(len(child2.list1)):
                        if max_max_num in child2.list1[i]:
                            children.list1.append(child2.list1[i])
                else:
                    children.list1.append(child2.list1)
                # print("list1_num2=",children.list1)
            if max_max_num == max3:
                if isinstance(child3.list1[0], list) and len(child3.list1) >= 1:
                    for i in range(len(child3.list1)):
                        if max_max_num in child3.list1[i]:
                            children.list1.append(child3.list1[i])
                else:
                    children.list1.append(child3.list1)
                # print("list1_num3=",children.list1)
        else: #случай когда в вершине может быть несколько списков
            # алгоритм работает так: у каждой вершины из списков берется минимальный и максимальный элементы
            # далее создаётся отрезок [min,max] для каждой вершины и рассматриваются их пересечения
            # после нахождения пересечений проверяются следующие условия (см. ниже)
            if min1 == max1:
                min_max_list1 = [min1, max1]
            else:
                min_max_list1 = list(range(min1, max1 + 1))
            if min2 == max2:
                min_max_list2 = [min2, max2]
            else:
                min_max_list2 = list(range(min2, max2 + 1))
            if min3 == max3:
                min_max_list3 = [min3, max3]
            else:
                min_max_list3 = list(range(min3, max3 + 1))

            flag_stop = 0  # flag остановки условий if
            result12 = list(set(min_max_list1) & set(min_max_list2))  # пересечение листов 1 и 2
            result13 = list(set(min_max_list1) & set(min_max_list3))  # пересечение листов 1 и 3
            result23 = list(set(min_max_list2) & set(min_max_list3))  # пересечение листов 2 и 3
            result21 = list(set(min_max_list2) & set(min_max_list1))  # пересечение листов 2 и 1
            result31 = list(set(min_max_list3) & set(min_max_list1))  # пересечение листов 3 и 1
            result32 = list(set(min_max_list3) & set(min_max_list2))  # пересечение листов 3 и 2

            print(min_max_list1)
            print(min_max_list2)
            print(min_max_list3)
            print(result12)
            print(result13)
            print(result23)
            # если есть один строго доминирующий спсиок 1 или 2 или 3
            if result12 == [] and result13 == [] and min_max_list1 > min_max_list2 and min_max_list1 > min_max_list3:
                flag_stop = 1
                for i in range(len(child1.list1)):
                    children.list1.append(child1.list1[i])
            else:
                if result12 == [] and result23 == [] and min_max_list2 > min_max_list1 and min_max_list2 > min_max_list3:
                    flag_stop = 1
                    for i in range(len(child2.list1)):
                        children.list1.append(child2.list1[i])
                else:
                    if result13 == [] and result23 == [] and min_max_list3 > min_max_list1 and min_max_list3 > min_max_list2:
                        flag_stop = 1
                        for i in range(len(child3.list1)):
                            children.list1.append(child3.list1[i])

            # если есть два подходящих 1,3
            if flag_stop == 0:
                if result12 == [] and result13 != [] and result23 == []:
                    flag_stop = 1
                    for i in range(len(child1.list1)):
                        children.list1.append(child1.list1[i])
                    for i in range(len(child3.list1)):
                        children.list1.append(child3.list1[i])

                # если есть два подходящих 1,2
            if flag_stop == 0:
                if result12 != [] and result13 == [] and result23 == []:
                    flag_stop = 1
                    for i in range(len(child1.list1)):
                        children.list1.append(child1.list1[i])
                    for i in range(len(child2.list1)):
                        children.list1.append(child2.list1[i])
                    # если есть два подходящих 2,3
            if flag_stop == 0:
                if result12 == [] and result13 == [] and result23 != []:
                    flag_stop = 1
                    for i in range(len(child2.list1)):
                        children.list1.append(child2.list1[i])
                    for i in range(len(child3.list1)):
                        children.list1.append(child3.list1[i])
            # если есть два подходящих 1 со 2 и 3, либо 2 с 1 и 3 либо 3 с 1 и 2
            if flag_stop == 0:
                if (result12 != [] and result13 != []) or (result21 != [] and result23 != []) or (
                        result31 != [] and result32 != []):
                    for i in range(len(child1.list1)):
                        children.list1.append(child1.list1[i])
                    for i in range(len(child2.list1)):
                        children.list1.append(child2.list1[i])
                    for i in range(len(child3.list1)):
                        children.list1.append(child3.list1[i])

DotExporter(root, nodenamefunc=nodenamefunc).to_dotfile("tree2.dot")
subprocess.call(['C:\\Program Files\\Graphviz\\bin\\dot.exe', 'tree2.dot', '-T', 'jpg', '-o',
                 'C:\\МГТУ\\ТеорияИгр\\lab4-py\\root2.jpg'])

for children in PreOrderIter(root): # всё то же самое что и для предыдущего уровня
    temp_list1 = []
    temp_list2 = []
    temp_list3 = []
    max1 = max2 = max3 = 0
    min1 = min2 = min3 = 0
    if children.depth == 1 and children.is_leaf == False:
        # print(children.name)
        child1 = children.children[0]
        if isinstance(child1.list1[0], list) and len(child1.list1) >= 1:
            for i in range(len(child1.list1)):
                temp_list1.append(child1.list1[i][1])
                max1 = max(temp_list1)
                min1 = min(temp_list1)
        # else:
        # num1 = child1.list1[0][2]
        child2 = children.children[1]

        if isinstance(child2.list1[0], list) and len(child2.list1) >= 1:
            for i in range(len(child2.list1)):
                temp_list2.append(child2.list1[i][1])
                max2 = max(temp_list2)
                min2 = min(temp_list2)
        # else:
        # num2 = child2.list1[0][2]
        child3 = children.children[2]
        if isinstance(child3.list1[0], list) and len(child3.list1) >= 1:
            for i in range(len(child3.list1)):
                temp_list3.append(child3.list1[i][1])
                max3 = max(temp_list3)
                min3 = min(temp_list3)
        # else:
        # num3 = child3.list1[0][2]
        max_num = max(max1, max2, max3)
        # print("max_num=", max_num)
        if len(temp_list3) == 1 and len(temp_list2) == 1 and len(temp_list1) == 1:
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
            if min1 == max1:
                min_max_list1 = [min1, max1]
            else:
                min_max_list1 = list(range(min1, max1 + 1))
            if min2 == max2:
                min_max_list2 = [min2, max2]
            else:
                min_max_list2 = list(range(min2, max2 + 1))
            if min3 == max3:
                min_max_list3 = [min3, max3]
            else:
                min_max_list3 = list(range(min3, max3 + 1))

            flag_stop = 0
            result12 = list(set(min_max_list1) & set(min_max_list2))  # пересечение листов 1 и 2
            result13 = list(set(min_max_list1) & set(min_max_list3))
            result23 = list(set(min_max_list2) & set(min_max_list3))
            result21 = list(set(min_max_list2) & set(min_max_list1))
            result31 = list(set(min_max_list3) & set(min_max_list1))
            result32 = list(set(min_max_list3) & set(min_max_list2))

            print(min_max_list1)
            print(min_max_list2)
            print(min_max_list3)
            print(result12)
            print(result13)
            print(result23)
            # если есть один строго доминирующий
            if result12 == [] and result13 == [] and min_max_list1 > min_max_list2 and min_max_list1 > min_max_list3:
                flag_stop = 1
                for i in range(len(child1.list1)):
                    children.list1.append(child1.list1[i])
            else:
                if result12 == [] and result23 == [] and min_max_list2 > min_max_list1 and min_max_list2 > min_max_list3:
                    flag_stop = 1
                    for i in range(len(child2.list1)):
                        children.list1.append(child2.list1[i])
                else:
                    if result13 == [] and result23 == [] and min_max_list3 > min_max_list1 and min_max_list3 > min_max_list2:
                        flag_stop = 1
                        for i in range(len(child3.list1)):
                            children.list1.append(child3.list1[i])

            # если есть два подходящих 1,3
            if flag_stop == 0:
                if result12 == [] and result13 != [] and result23 == []:
                    flag_stop = 1
                    for i in range(len(child1.list1)):
                        children.list1.append(child1.list1[i])
                    for i in range(len(child3.list1)):
                        children.list1.append(child3.list1[i])

                # если есть два подходящих 1,2
            if flag_stop == 0:
                if result12 != [] and result13 == [] and result23 == []:
                    flag_stop = 1
                    for i in range(len(child1.list1)):
                        children.list1.append(child1.list1[i])
                    for i in range(len(child2.list1)):
                        children.list1.append(child2.list1[i])
                    # если есть два подходящих 2,3
            if flag_stop == 0:
                if result12 == [] and result13 == [] and result23 != []:
                    flag_stop = 1
                    for i in range(len(child2.list1)):
                        children.list1.append(child2.list1[i])
                    for i in range(len(child3.list1)):
                        children.list1.append(child3.list1[i])
            # если есть два подходящих 1 со 2 и 3, либо 2 с 1 и 3 либо 3 с 1 и 2
            if flag_stop == 0:
                if (result12 != [] and result13 != []) or (result21 != [] and result23 != []) or (
                        result31 != [] and result32 != []):
                    for i in range(len(child1.list1)):
                        children.list1.append(child1.list1[i])
                    for i in range(len(child2.list1)):
                        children.list1.append(child2.list1[i])
                    for i in range(len(child3.list1)):
                        children.list1.append(child3.list1[i])

for children in LevelOrderIter(root):
    temp_list1 = []
    temp_list2 = []
    temp_list3 = []
    max1 = max2 = max3 = 0
    min1 = min2 = min3 = 0
    if children.depth == 0 and children.is_leaf == False: # всё то же самое только для корня
        # print(children.name)
        child1 = children.children[0]
        if isinstance(child1.list1[0], list) and len(child1.list1) >= 1:
            for i in range(len(child1.list1)):
                temp_list1.append(child1.list1[i][0])
                max1 = max(temp_list1)
                min1 = min(temp_list1)
        # else:
        # num1 = child1.list1[0][2]
        child2 = children.children[1]
        if isinstance(child2.list1[0], list) and len(child2.list1) >= 1:
            for i in range(len(child2.list1)):
                temp_list2.append(child2.list1[i][0])
                max2 = max(temp_list2)
                min2 = min(temp_list2)
        # else:
        # num2 = child2.list1[0][2]
        child3 = children.children[2]
        if isinstance(child3.list1[0], list) and len(child3.list1) >= 1:
            for i in range(len(child3.list1)):
                temp_list3.append(child3.list1[i][0])
                max3 = max(temp_list3)
                min3 = min(temp_list3)
        # else:
        # num3 = child3.list1[0][2]
        max_num = max(max1, max2, max3)
        # print("max_num=", max_num)
        if len(temp_list3) == 1 and len(temp_list2) == 1 and len(temp_list1) == 1:
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
            if min1 == max1:
                min_max_list1 = [min1, max1]
            else:
                min_max_list1 = list(range(min1, max1 + 1))
            if min2 == max2:
                min_max_list2 = [min2, max2]
            else:
                min_max_list2 = list(range(min2, max2 + 1))
            if min3 == max3:
                min_max_list3 = [min3, max3]
            else:
                min_max_list3 = list(range(min3, max3 + 1))

            flag_stop = 0
            result12 = list(set(min_max_list1) & set(min_max_list2))  # пересечение листов 1 и 2
            result13 = list(set(min_max_list1) & set(min_max_list3))
            result23 = list(set(min_max_list2) & set(min_max_list3))
            result21 = list(set(min_max_list2) & set(min_max_list1))
            result31 = list(set(min_max_list3) & set(min_max_list1))
            result32 = list(set(min_max_list3) & set(min_max_list2))

            print(min_max_list1)
            print(min_max_list2)
            print(min_max_list3)
            print(result12)
            print(result13)
            print(result23)
            # если есть один строго доминирующий
            if result12 == [] and result13 == [] and min_max_list1 > min_max_list2 and min_max_list1 > min_max_list3:
                flag_stop = 1
                for i in range(len(child1.list1)):
                    children.list1.append(child1.list1[i])
            else:
                if result12 == [] and result23 == [] and min_max_list2 > min_max_list1 and min_max_list2 > min_max_list3:
                    flag_stop = 1
                    for i in range(len(child2.list1)):
                        children.list1.append(child2.list1[i])
                else:
                    if result13 == [] and result23 == [] and min_max_list3 > min_max_list1 and min_max_list3 > min_max_list2:
                        flag_stop = 1
                        for i in range(len(child3.list1)):
                            children.list1.append(child3.list1[i])

            # если есть два подходящих 1,3
            if flag_stop == 0:
                if result12 == [] and result13 != [] and result23 == []:
                    flag_stop = 1
                    for i in range(len(child1.list1)):
                        children.list1.append(child1.list1[i])
                    for i in range(len(child3.list1)):
                        children.list1.append(child3.list1[i])

                # если есть два подходящих 1,2
            if flag_stop == 0:
                if result12 != [] and result13 == [] and result23 == []:
                    flag_stop = 1
                    for i in range(len(child1.list1)):
                        children.list1.append(child1.list1[i])
                    for i in range(len(child2.list1)):
                        children.list1.append(child2.list1[i])
                    # если есть два подходящих 2,3
            if flag_stop == 0:
                if result12 == [] and result13 == [] and result23 != []:
                    flag_stop = 1
                    for i in range(len(child2.list1)):
                        children.list1.append(child2.list1[i])
                    for i in range(len(child3.list1)):
                        children.list1.append(child3.list1[i])
            # если есть два подходящих 1 со 2 и 3, либо 2 с 1 и 3 либо 3 с 1 и 2
            if flag_stop == 0:
                if (result12 != [] and result13 != []) or (result21 != [] and result23 != []) or (
                        result31 != [] and result32 != []):
                    for i in range(len(child1.list1)):
                        children.list1.append(child1.list1[i])
                    for i in range(len(child2.list1)):
                        children.list1.append(child2.list1[i])
                    for i in range(len(child3.list1)):
                        children.list1.append(child3.list1[i])

    else:
        break

DotExporter(root, nodenamefunc=nodenamefunc).to_dotfile("tree1.dot") # вывод на картинку можно использовать команду
# to_picture("tree.jpg")
subprocess.call(['C:\\Program Files\\Graphviz\\bin\\dot.exe', 'tree1.dot', '-T', 'jpg', '-o',
                 'C:\\МГТУ\\ТеорияИгр\\lab4-py\\root1.jpg'])
