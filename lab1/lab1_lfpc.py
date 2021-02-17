# Made by: Cambur Dumitru
# Group: FAF-191
# Variant: (32 + 1) - 7 = 26
from collections import defaultdict
from PIL import Image
from networkx.drawing.nx_agraph import to_agraph
import networkx as nx
import matplotlib.pyplot as plt


class Graph:
    def __init__(self):
        self.graph = defaultdict(dict)

    def add_edge(self, fr, to, weight):
        if fr not in self.graph:
            self.graph[fr][to] = weight
        elif to not in self.graph[fr]:
            self.graph[fr][to] = weight
        else:
            self.graph[fr][to] += weight

    def check_grammar(self, start_node, re_input):
        res = f"{start_node}"
        node_current = self.graph[start_node]

        i = 0
        inp_len = len(re_input)
        while i != inp_len:

            flag = False
            for j in node_current.keys():

                if re_input[i] == node_current[j]:

                    res += f" -> {j}"
                    flag = True

                    if self.graph[j]:
                        node_current = self.graph[j]
                    break

            if not flag:
                return False, None

            i += 1

        if res[-1] != "*":
            return False, None
        else:
            return True, res


def convert_to_networkx(rules):
    G = nx.Graph()
    for i in rules:
        G.add_edge(*(i[0], i[1]), label=f"{i[2]}", font_color="red")
    return G


def draw_plt(G, rules):
    pos = nx.spring_layout(G)
    plt.figure()

    nx.draw(G, pos, with_labels=True,
            edge_color='black', width=1, linewidths=1,
            node_size=500, node_color='red', alpha=0.9,
            labels={node: node for node in G.nodes()})

    for i in rules:
        nx.draw_networkx_edge_labels(
            G, pos,
            edge_labels={(i[0], i[1]): i[2]},
            font_color='blue')

    plt.axis('off')
    plt.show()


def draw_graphviz(G, image_name):
    """ These are attributes for pygraphviz, if you are not satisfied resolution.
        Or your computer gets laggy on program run, you can try to raise/reduce dpi"""

    G.graph['edge'] = {'splines': 'curved', "color": "navyblue", "font_color": "red"}
    G.graph['graph'] = {'rankdir': 'TD', "dpi": 200, "bgcolor": "transparent"}
    G.graph['node'] = {'shape': 'circle', "style": "filled", "fillcolor": "aquamarine"}

    A = to_agraph(G)
    A.layout('dot')
    A.draw(f"{image_name}")

    im = Image.open(f"{image_name}")
    im.show()


rules = [
    ["S", "A", "d"],
    ["A", "B", "a"],
    ["B", "C", "b"],
    ["C", "B", "c"],
    ["B", "*", "d"],
    ["C", "A", "a"],
    ["A", "*", "b"],
]
G = convert_to_networkx(rules)
g = Graph()

for i in rules:
    g.add_edge(i[0], i[1], i[2])


write = input("\nWrite a string to check if it matches with FA: ")
is_accepted, path = g.check_grammar("S", write)

# if you want to draw pure networkx plot, then uncomment this function
# draw_plt(G, rules)

# Using graphviz for visualization is recommended, however you must have it installed.
draw_graphviz(G, "finite_automata.png")

if not is_accepted:
    print("This string is not accepted by FA")
else:
    print(f"This string is accepted by FA\n"
          f"Path: {path}\n")






