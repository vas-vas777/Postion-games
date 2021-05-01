from anytree import Node, RenderTree, AsciiStyle, PostOrderIter, PreOrderIter, LevelOrderIter
from anytree.exporter import DotExporter
import subprocess
import random
import numpy as np

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
colors = ["red", "yellow", "green", "gold", "orange", "fuchsia"]


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
        color = colors[i % len(colors)]
        if node == root:
            return '%s' % ""
        else:
            for j in range(len(node.list1)):
                if node.list1[j] == root.list1[i] and len(node.list1) == 1:
                    return '%s' % "color=" + color


def edgeattrfunc(parent, child):
    for i in range(len(root.list1)):
        color = colors[i % len(colors)]
        for j in range(len(child.list1)):
            if child.list1[j] == root.list1[i]:
                print(child.name, child.list1[j])
                return '%s' % "color=" + color


def last_level(depth):
    list_of_wins_player = list()
    list_of_leaves = list()
    for node in PreOrderIter(root):  # обход с вершины n и посещение её детей
        if node.depth == depth and node.is_leaf == False:
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
            # print(list_of_wins_player)
            for i in range(len(list_of_wins_player)):
                # print(list_of_wins_player[i],'-',max_num)
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
    for node in LevelOrderIter(root):  # обход со второго уровня и посещение детей
        if node.depth == temp_depth and node.is_leaf == False:
            # print(len(node.children))
            for i in range(len(node.children)):
                child = node.children[i]
                list_of_leaves.append(child)
                for j in range(len(child.list1)):
                    list_of_wins_player.append(child.list1[j][node.player])
                # print(list_of_wins_player)
                list_of_max_values_in_each_vertex.append(max(list_of_wins_player))
                list_of_min_values_in_each_vertex.append(min(list_of_wins_player))
                list_of_wins_player.clear()
                # print(list_of_max_values_in_each_vertex)
                # print(list_of_min_values_in_each_vertex)

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
                # print(list_of_max_values_in_each_vertex)
                for i in range(len(list_of_max_values_in_each_vertex)):
                    if max_num == list_of_max_values_in_each_vertex[i]:
                        # print(list_of_max_values_in_each_vertex.index(wins_of_player))

                        node.list1.append(list_of_leaves[i].list1[0])
                        count += 1
                    else:
                        count += 1
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
                # print(list_of_max_values_in_each_vertex)
                # print(list_of_min_values_in_each_vertex)
                for i in range(len(list_of_max_values_in_each_vertex)):
                    if list_of_max_values_in_each_vertex[i] == list_of_min_values_in_each_vertex[i]:
                        list_of_lists_min_max_in_each_vertex.append([list_of_min_values_in_each_vertex[i],
                                                                     list_of_max_values_in_each_vertex[i]])
                    else:
                        list_of_lists_min_max_in_each_vertex.append(list(range(list_of_min_values_in_each_vertex[i],
                                                                               list_of_max_values_in_each_vertex[
                                                                                   i] + 1)))
                # max_list_among_children = list()
                # for i in range(len(list_of_lists_min_max_in_each_vertex)):
                #     max_list_among_children.append(set(list_of_lists_min_max_in_each_vertex[i]))
                # print(max_list_among_children)
                max_list_among_children = np.max(list_of_lists_min_max_in_each_vertex)
                # print('max=', max_list_among_children)
                for i in range(len(list_of_lists_min_max_in_each_vertex)):
                    if max_list_among_children in list_of_lists_min_max_in_each_vertex[i]:
                        max_list_among_children = list_of_lists_min_max_in_each_vertex[i]
                        break
                # print(list_of_leaves)
                for i in range(len(list_of_lists_min_max_in_each_vertex)):
                    # print(max_list_among_children, '-', list_of_lists_min_max_in_each_vertex[i])
                    if list(set(max_list_among_children) & set(list_of_lists_min_max_in_each_vertex[i])):
                        for j in range(len(list_of_leaves[i].list1)):
                            # print('-', list_of_leaves[i].list1[j])
                            node.list1.append(list_of_leaves[i].list1[j])
                list_of_wins_player.clear()
                list_of_max_values_in_each_vertex.clear()
                list_of_min_values_in_each_vertex.clear()
                list_of_lists_min_max_in_each_vertex.clear()
                max_list_among_children.clear()
                list_of_leaves.clear()
                if_in_vertex_len_of_list_greater_1 = 0


print("Введите глубину дерева")
depth = int(input())
#depth = 5
print("Введите количество игроков")
number_players = int(input())
#number_players = 3
print("Введите стратегии игроков")
for i in range(number_players):
    list_of_strateges_players.append(int(input()))
#list_of_strateges_players = [3, 3, 3]
print("Введите нижний выигрыш из диапазона выигрышей")
low_value_win = int(input())
#low_value_win = 0
print("Введите верхний выигрыш из диапазона выигрышей")
high_value_win = int(input())
#high_value_win = 15
begin_game()
generate_tree(depth - 1, number_players, low_value_win, high_value_win)
last_level(depth - 1)
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
                                edgeattrfunc=edgeattrfunc).to_dotfile(
                        "tree1.dot")

subprocess.call(['C:\\Program Files\\Graphviz\\bin\\dot.exe', 'tree1.dot', '-T', 'jpg', '-o',
                 'C:\\МГТУ\\ТеорияИгр\\lab4-py\\root1.jpg'])
