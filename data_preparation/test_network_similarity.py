import network_similarity as ns
import sys

import networkx as nx
import matplotlib.pyplot as plt

from os import listdir
from os.path import isfile, join

if __name__ == '__main__':
    
    # filename = sys.argv[1]
    directory = sys.argv[1]
    expected_similarity = sys.argv[2]
    
    onlyfiles = [f for f in listdir(directory) if isfile(join(directory, f))]

    # g = nx.Graph()
    g = nx.star_graph(20)
    for f in onlyfiles:
        g.add_node(f)

    count = 0
    for f1 in onlyfiles:
        similars = []
        print(count)
        count += 1
        for f2 in onlyfiles:
            f1_fullpath = join(directory, f1)
            f2_fullpath = join(directory, f2)
            if f1 == f2:
                continue

            if f1 > f2:
                f1, f2 = f2, f1

            if (f1, f2) in g.edges():
                continue

            if ns.check_similarity(f1_fullpath, f2_fullpath, expected_similarity):
                g.add_edge(f1, f2)

    pos = nx.spring_layout(g)
    nx.draw(g, pos=pos, node_color='#BBBBBB')
    plt.savefig('a.png')
    plt.show()
    
