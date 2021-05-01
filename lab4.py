from anytree import Node, RenderTree, AsciiStyle, PostOrderIter, PreOrderIter, LevelOrderIter
from anytree.exporter import DotExporter
import subprocess
import random

# для обозначения номера вершины
# depth = 0 #
# создание корня и трёх детей
num = 0
root = Node
right = Node
left = Node
middle = Node
list_of_lists_of_root = list()
list_of_players_by_levels = list()
list_of_strateges_players = list()


def sequence_of_players_in_game(depth, number_player):
    for i in range(depth):
        for j in range(number_players):
            list_of_players_by_levels.append(j)


def begin_game():
    global root
    global num
    root = Node(name=num, color='', number_edges=list_of_strateges_players[0], player=0, list1=list())

    for i in range(list_of_strateges_players[0]):
        num += 1
        list_of_lists_of_root.append(
            Node(name=num, color='', number_edges=list_of_strateges_players[1], player=1, list1=list(), parent=root))


def generate_tree(depth, number_players, low_value_win, high_value_win):
    global num
    flag = 0  # остановка алгоритма генерации дерева до глубины depth

    while flag == 0:
        for children in PostOrderIter(root):
            if children.is_leaf:
                if children.depth == depth:
                    flag = 1
                    break
                else:
                    continue
            else:
                break

        if flag == 1:
            break

        for children in PostOrderIter(root, maxlevel=depth):  # случайный выбор продолжать веришну вниз или нет
            if children.is_leaf:
                random_number = random.randint(0, 1)

                if random_number == 1:
                    list_of_strateges_players.index(children.number_edges)
                    strateges_of_player = list_of_strateges_players[
                        (list_of_strateges_players.index(children.number_edges)
                         + 1) % len(list_of_strateges_players)]
                    player = (children.player + 1) % number_players
                    for i in range(children.number_edges):
                        num += 1
                        Node(name=num, color='', list1=list(),
                             number_edges=strateges_of_player, player=player, parent=children)

    for children in PostOrderIter(root):  # заполнение листов случаным вектором из 3 чисел
        if children.is_leaf:
            list_rand = random.sample(range(low_value_win, high_value_win), number_players)
            children.list1.append(list_rand)


def nodenamefunc(node):
    if node.is_leaf is True:
        return '%s:%s' % (node.name, node.list1)
    else:
        return '%s:%s:%s' % (node.name, node.list1, node.player + 1)  # вывод в узлах (номер вершины, значение выиграшей


# и текущая глубина узла)


def nodeattrfunc(node):  # для раскрашивания вершин которые попали в оптимальный путь
    for i in range(len(root.list1)):
        if node == root:
            return '%s' % "color=red shape=box"
        else:
            for j in range(len(node.list1)):
                if node.list1[j] == root.list1[i]:
                    return '%s' % "color=red shape=box"
                #else:
                    #return '%s' % "shape=box"


def last_level(depth):
    list_of_wins_player = list()
    list_of_leaves = list()
    # max_num=list()
    for node in PreOrderIter(root):  # обход с вершины n и посещение её детей
        if node.depth == depth - 1 and node.is_leaf == False:
            for i in range(len(node.children)):
                child = node.children[i]
                list_of_leaves.append(child)
                # print(list_of_leaves)
                # print(child.list1[0][node.player])
                list_of_wins_player.append(child.list1[0][node.player])
                # print(list_of_wins_player)

            # print(list_of_wins_player)
            max_num = max(list_of_wins_player)
            # print(max_num)
            # print("max_num=", max_num) выбор максимального выигрыша у игрока 1
            #print(list_of_wins_player)
            for i in range(len(list_of_wins_player)):
                #print(list_of_wins_player[i],'-',max_num)
                if max_num == list_of_wins_player[i]:
                    node.list1.append(list_of_leaves[i].list1[0])
            list_of_wins_player.clear()
            list_of_leaves.clear()


def level_middle(depth):
    temp_depth = depth
    list_of_wins_player = list()
    list_of_leaves = list()
    list_of_max_values_in_each_vertex = list()
    list_of_min_values_in_each_vertex = list()
    if_in_vertex_len_of_list_greater_1 = 0
    list_of_lists_min_max_in_each_vertex = list()
    # while temp_depth > 0:
    for node in LevelOrderIter(root):  # обход со второго уровня и посещение детей
        if node.depth == temp_depth and node.is_leaf == False:
            # print(len(node.children))
            for i in range(len(node.children)):
                child = node.children[i]
                list_of_leaves.append(child)
                for j in range(len(child.list1)):
                    list_of_wins_player.append(child.list1[j][node.player])
                #print(list_of_wins_player)
                list_of_max_values_in_each_vertex.append(max(list_of_wins_player))
                list_of_min_values_in_each_vertex.append(min(list_of_wins_player))
                list_of_wins_player.clear()
                # print(list_of_max_values_in_each_vertex)
                # print(list_of_min_values_in_each_vertex)
            # max_max_num = max(max1, max2, max3)
            # случай когда в каждой вершине по одному списку
            for i in range(len(node.children)):
                if len(node.children[i].list1) == 1:
                    if_in_vertex_len_of_list_greater_1 = 0
                    continue
                else:
                    if_in_vertex_len_of_list_greater_1 = 1
                    break
            # print(if_in_vertex_len_of_list_greater_1)
            if if_in_vertex_len_of_list_greater_1 == 0:  # случай когда в каждой вершине один список из выиграшей
                # игроков
                max_num = max(list_of_max_values_in_each_vertex)
                count = 0
                #print(list_of_max_values_in_each_vertex)
                for i in range(len(list_of_max_values_in_each_vertex)):
                    #print(list_of_max_values_in_each_vertex[i], '-', max_num)
                    # count+=1
                    if max_num == list_of_max_values_in_each_vertex[i]:
                        #print(list_of_max_values_in_each_vertex.index(wins_of_player))

                        node.list1.append(list_of_leaves[i].list1[0])
                        count += 1
                    else:
                        count += 1
                # temp_depth -= 1
                # list_of_wins_player.clear()
                # list_of_wins_player.clear()
                list_of_max_values_in_each_vertex.clear()
                list_of_min_values_in_each_vertex.clear()
                list_of_lists_min_max_in_each_vertex.clear()
                # max_list_among_children.clear()
                list_of_leaves.clear()
                if_in_vertex_len_of_list_greater_1 = 0
            else:  # случай когда в вершине может быть несколько списков
                # алгоритм работает так: у каждой вершины из списков берется минимальный и максимальный элементы
                # далее создаётся отрезок [min,max] для каждой вершины и рассматриваются их пересечения
                # после нахождения пересечений проверяются следующие условия (см. ниже)
                print(list_of_max_values_in_each_vertex)
                print(list_of_min_values_in_each_vertex)
                for i in range(len(list_of_max_values_in_each_vertex)):
                    if list_of_max_values_in_each_vertex[i] == list_of_min_values_in_each_vertex[i]:
                        list_of_lists_min_max_in_each_vertex.append([list_of_min_values_in_each_vertex[i],
                                                                     list_of_max_values_in_each_vertex[i]])
                    else:
                        list_of_lists_min_max_in_each_vertex.append(list(range(list_of_min_values_in_each_vertex[i],
                                                                               list_of_max_values_in_each_vertex[
                                                                                   i] + 1)))

                max_list_among_children = max(list_of_lists_min_max_in_each_vertex)
                print(list_of_lists_min_max_in_each_vertex)
                # print(list_of_leaves)
                for i in range(len(list_of_lists_min_max_in_each_vertex)):
                    print(max_list_among_children,'-',list_of_lists_min_max_in_each_vertex[i])
                    if list(set(max_list_among_children) & set(list_of_lists_min_max_in_each_vertex[i])):
                        for j in range(len(list_of_leaves[i].list1)):
                            print('-',list_of_leaves[i].list1[j])
                            node.list1.append(list_of_leaves[i].list1[j])
                list_of_wins_player.clear()
                list_of_max_values_in_each_vertex.clear()
                list_of_min_values_in_each_vertex.clear()
                list_of_lists_min_max_in_each_vertex.clear()
                max_list_among_children.clear()
                list_of_leaves.clear()
                if_in_vertex_len_of_list_greater_1 = 0
                # if min1 == max1:
                #     min_max_list1 = [min1, max1]
                # else:
                #     min_max_list1 = list(range(min1, max1 + 1))
                # if min2 == max2:
                #     min_max_list2 = [min2, max2]
                # else:
                #     min_max_list2 = list(range(min2, max2 + 1))
                # if min3 == max3:
                #     min_max_list3 = [min3, max3]
                # else:
                #     min_max_list3 = list(range(min3, max3 + 1))

                # flag_stop = 0  # flag остановки условий if
                # result12 = list(set(min_max_list1) & set(min_max_list2))  # пересечение листов 1 и 2
                # result13 = list(set(min_max_list1) & set(min_max_list3))  # пересечение листов 1 и 3
                # result23 = list(set(min_max_list2) & set(min_max_list3))  # пересечение листов 2 и 3
                # result21 = list(set(min_max_list2) & set(min_max_list1))  # пересечение листов 2 и 1
                # result31 = list(set(min_max_list3) & set(min_max_list1))  # пересечение листов 3 и 1
                # result32 = list(set(min_max_list3) & set(min_max_list2))  # пересечение листов 3 и 2
                #
                # # если есть один строго доминирующий спсиок 1 или 2 или 3
                # if result12 == [] and result13 == [] and min_max_list1 > min_max_list2 and min_max_list1 > min_max_list3:
                #     flag_stop = 1
                #     for i in range(len(child1.list1)):
                #         children.list1.append(child1.list1[i])
                # else:
                #     if result12 == [] and result23 == [] and min_max_list2 > min_max_list1 and min_max_list2 > min_max_list3:
                #         flag_stop = 1
                #         for i in range(len(child2.list1)):
                #             children.list1.append(child2.list1[i])
                #     else:
                #         if result13 == [] and result23 == [] and min_max_list3 > min_max_list1 and min_max_list3 > min_max_list2:
                #             flag_stop = 1
                #             for i in range(len(child3.list1)):
                #                 children.list1.append(child3.list1[i])
                #
                # # если есть два подходящих 1,3
                # if flag_stop == 0:
                #     if result12 == [] and result13 != [] and result23 == []:
                #         flag_stop = 1
                #         for i in range(len(child1.list1)):
                #             children.list1.append(child1.list1[i])
                #         for i in range(len(child3.list1)):
                #             children.list1.append(child3.list1[i])
                #
                #     # если есть два подходящих 1,2
                # if flag_stop == 0:
                #     if result12 != [] and result13 == [] and result23 == []:
                #         flag_stop = 1
                #         for i in range(len(child1.list1)):
                #             children.list1.append(child1.list1[i])
                #         for i in range(len(child2.list1)):
                #             children.list1.append(child2.list1[i])
                #         # если есть два подходящих 2,3
                # if flag_stop == 0:
                #     if result12 == [] and result13 == [] and result23 != []:
                #         flag_stop = 1
                #         for i in range(len(child2.list1)):
                #             children.list1.append(child2.list1[i])
                #         for i in range(len(child3.list1)):
                #             children.list1.append(child3.list1[i])
                # # если есть два подходящих 1 со 2 и 3, либо 2 с 1 и 3 либо 3 с 1 и 2
                # if flag_stop == 0:
                #     if (result12 != [] and result13 != []) or (result21 != [] and result23 != []) or (
                #             result31 != [] and result32 != []):
                #         for i in range(len(child1.list1)):
                #             children.list1.append(child1.list1[i])
                #         for i in range(len(child2.list1)):
                #             children.list1.append(child2.list1[i])
                #         for i in range(len(child3.list1)):
                #             children.list1.append(child3.list1[i])

            # temp_depth -= 1


#
#
# # # DotExporter(root, nodenamefunc=nodenamefunc).to_dotfile("tree2.dot")
# # # subprocess.call(['C:\\Program Files\\Graphviz\\bin\\dot.exe', 'tree2.dot', '-T', 'jpg', '-o',
# # #                  'C:\\МГТУ\\ТеорияИгр\\lab4-py\\root2.jpg'])
# #
#
# #
# def root_level():
#     for children in LevelOrderIter(root):
#         temp_list1 = []
#         temp_list2 = []
#         temp_list3 = []
#         max1 = max2 = max3 = 0
#         min1 = min2 = min3 = 0
#         if children.depth == 0 and children.is_leaf == False:  # всё то же самое только для корня
#             # print(children.name)
#             child1 = children.children[0]
#             if isinstance(child1.list1[0], list) and len(child1.list1) >= 1:
#                 for i in range(len(child1.list1)):
#                     temp_list1.append(child1.list1[i][0])
#                     max1 = max(temp_list1)
#                     min1 = min(temp_list1)
#             # else:
#             # num1 = child1.list1[0][2]
#             child2 = children.children[1]
#             if isinstance(child2.list1[0], list) and len(child2.list1) >= 1:
#                 for i in range(len(child2.list1)):
#                     temp_list2.append(child2.list1[i][0])
#                     max2 = max(temp_list2)
#                     min2 = min(temp_list2)
#             # else:
#             # num2 = child2.list1[0][2]
#             child3 = children.children[2]
#             if isinstance(child3.list1[0], list) and len(child3.list1) >= 1:
#                 for i in range(len(child3.list1)):
#                     temp_list3.append(child3.list1[i][0])
#                     max3 = max(temp_list3)
#                     min3 = min(temp_list3)
#             # else:
#             # num3 = child3.list1[0][2]
#             max_num = max(max1, max2, max3)
#             # print("max_num=", max_num)
#             if len(temp_list3) == 1 and len(temp_list2) == 1 and len(temp_list1) == 1:
#                 if max_num == max1:
#                     if isinstance(child1.list1[0], list) and len(child1.list1) >= 1:
#                         for i in range(len(child1.list1)):
#                             if max_num in child1.list1[i]:
#                                 children.list1.append(child1.list1[i])
#                     else:
#                         children.list1.append(child1.list1)
#                     # print("list1_num1=",children.list1)
#                 if max_num == max2:
#                     if isinstance(child2.list1[0], list) and len(child2.list1) >= 1:
#                         for i in range(len(child2.list1)):
#                             if max_num in child2.list1[i]:
#                                 children.list1.append(child2.list1[i])
#                     else:
#                         children.list1.append(child2.list1)
#                     # print("list1_num2=",children.list1)
#                 if max_num == max3:
#                     if isinstance(child3.list1[0], list) and len(child3.list1) >= 1:
#                         for i in range(len(child3.list1)):
#                             if max_num in child3.list1[i]:
#                                 children.list1.append(child3.list1[i])
#                     else:
#                         children.list1.append(child3.list1)
#                     # print("list1_num3=",children.list1)
#             else:
#                 if min1 == max1:
#                     min_max_list1 = [min1, max1]
#                 else:
#                     min_max_list1 = list(range(min1, max1 + 1))
#                 if min2 == max2:
#                     min_max_list2 = [min2, max2]
#                 else:
#                     min_max_list2 = list(range(min2, max2 + 1))
#                 if min3 == max3:
#                     min_max_list3 = [min3, max3]
#                 else:
#                     min_max_list3 = list(range(min3, max3 + 1))
#
#                 flag_stop = 0
#                 result12 = list(set(min_max_list1) & set(min_max_list2))  # пересечение листов 1 и 2
#                 result13 = list(set(min_max_list1) & set(min_max_list3))
#                 result23 = list(set(min_max_list2) & set(min_max_list3))
#                 result21 = list(set(min_max_list2) & set(min_max_list1))
#                 result31 = list(set(min_max_list3) & set(min_max_list1))
#                 result32 = list(set(min_max_list3) & set(min_max_list2))
#
#                 # если есть один строго доминирующий
#                 if result12 == [] and result13 == [] and min_max_list1 > min_max_list2 and min_max_list1 > min_max_list3:
#                     flag_stop = 1
#                     for i in range(len(child1.list1)):
#                         children.list1.append(child1.list1[i])
#                 else:
#                     if result12 == [] and result23 == [] and min_max_list2 > min_max_list1 and min_max_list2 > min_max_list3:
#                         flag_stop = 1
#                         for i in range(len(child2.list1)):
#                             children.list1.append(child2.list1[i])
#                     else:
#                         if result13 == [] and result23 == [] and min_max_list3 > min_max_list1 and min_max_list3 > min_max_list2:
#                             flag_stop = 1
#                             for i in range(len(child3.list1)):
#                                 children.list1.append(child3.list1[i])
#
#                 # если есть два подходящих 1,3
#                 if flag_stop == 0:
#                     if result12 == [] and result13 != [] and result23 == []:
#                         flag_stop = 1
#                         for i in range(len(child1.list1)):
#                             children.list1.append(child1.list1[i])
#                         for i in range(len(child3.list1)):
#                             children.list1.append(child3.list1[i])
#
#                     # если есть два подходящих 1,2
#                 if flag_stop == 0:
#                     if result12 != [] and result13 == [] and result23 == []:
#                         flag_stop = 1
#                         for i in range(len(child1.list1)):
#                             children.list1.append(child1.list1[i])
#                         for i in range(len(child2.list1)):
#                             children.list1.append(child2.list1[i])
#                         # если есть два подходящих 2,3
#                 if flag_stop == 0:
#                     if result12 == [] and result13 == [] and result23 != []:
#                         flag_stop = 1
#                         for i in range(len(child2.list1)):
#                             children.list1.append(child2.list1[i])
#                         for i in range(len(child3.list1)):
#                             children.list1.append(child3.list1[i])
#                 # если есть два подходящих 1 со 2 и 3, либо 2 с 1 и 3 либо 3 с 1 и 2
#                 if flag_stop == 0:
#                     if (result12 != [] and result13 != []) or (result21 != [] and result23 != []) or (
#                             result31 != [] and result32 != []):
#                         for i in range(len(child1.list1)):
#                             children.list1.append(child1.list1[i])
#                         for i in range(len(child2.list1)):
#                             children.list1.append(child2.list1[i])
#                         for i in range(len(child3.list1)):
#                             children.list1.append(child3.list1[i])
#
#         else:
#             break


# DotExporter(root, nodenamefunc=nodenamefunc, nodeattrfunc=lambda node: "shape=box",
#             edgeattrfunc=lambda parent, child: "style=bold").to_dotfile("tree2.dot")
# subprocess.call(['C:\\Program Files\\Graphviz\\bin\\dot.exe', 'tree2.dot', '-T', 'jpg', '-o',
#                  'C:\\МГТУ\\ТеорияИгр\\lab4-py\\root2.jpg'])

print("Введите глубину дерева")
# depth = int(input())
depth = 5
print("Введите количество игроков")
# number_players = int(input())
number_players = 3
print("Введите стратегии игроков")
# for i in range(number_players):
#   list_of_strateges_players.append(int(input()))
list_of_strateges_players = [2, 3, 2]
print("Введите нижний выигрыш из диапазона выигрышей")
# low_value_win = int(input())
low_value_win = 0
print("Введите верхний выигрыш из диапазона выигрышей")
# high_value_win = int(input())
high_value_win = 15
begin_game()
generate_tree(depth, number_players, low_value_win, high_value_win)
last_level(depth)
# DotExporter(root, nodenamefunc=nodenamefunc, nodeattrfunc=lambda node: "shape=box",
#             edgeattrfunc=lambda parent, child: "style=bold").to_dotfile("tree2.dot")
# subprocess.call(['C:\\Program Files\\Graphviz\\bin\\dot.exe', 'tree2.dot', '-T', 'jpg', '-o',
#                  'C:\\МГТУ\\ТеорияИгр\\lab4-py\\root2.jpg'])
depth -= 1
while depth > 0:
    depth -= 1
    level_middle(depth)

print("Цена игры:")
print(root.list1)

print("Оптимальный путь")
for i in range(len(root.list1)):
    for children in LevelOrderIter(root):
        if children == root:
            print(children.name, "-", children.list1[i])
        else:
            for j in range(len(children.list1)):
                if children.list1[j] == root.list1[i]:
                    print(children.name, "-", children.list1[j])
                    DotExporter(root, nodenamefunc=nodenamefunc, nodeattrfunc=nodeattrfunc,
                                edgeattrfunc=lambda parent, child: "style=bold").to_dotfile(
                        "tree1.dot")  # вывод на картинку можно использовать команду

subprocess.call(['C:\\Program Files\\Graphviz\\bin\\dot.exe', 'tree1.dot', '-T', 'jpg', '-o',
                 'C:\\МГТУ\\ТеорияИгр\\lab4-py\\root1.jpg'])
