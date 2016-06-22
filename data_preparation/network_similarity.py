import os
import sys
import json
import itertools as it

import networkx as nx

# settings
home_dir = '/home/vienna/FYP'
cfg_json_path = home_dir + '/cfg/g'

def get_filename(number):
    return '%s/S117-S%d-q1g.c.cfg.json' % (cfg_json_path, number)


def text_to_json_dict(text):
    d = json.loads(text)
    return d
    

def read_file(filename):
    with open(filename, 'r') as f:
        return f.read()


def adjacency_list_to_graph(adjacency_list):
    G = nx.DiGraph()

    for source, v in adjacency_list.items():
        for dest in v:
            G.add_edge(source, dest)
    return G
        

def subgraphs_product(G1, G2, length):
    assert length <= len(G1.nodes())
    assert length <= len(G2.nodes())

    a = it.combinations(G1.nodes(), length)
    b = it.combinations(G2.nodes(), length)
    gen = it.product(a, b)

    for pair in gen:
        sub1 = G1.subgraph(pair[0])
        sub2 = G2.subgraph(pair[1])
        if nx.is_weakly_connected(sub1) and nx.is_weakly_connected(sub2):
            yield (sub1, sub2)


def get_graph_from_id(ID):
    text = read_file(get_filename(ID))    
    d = text_to_json_dict(text)
    G = adjacency_list_to_graph(d['adjacency'])
    return G


def get_graph_from_filename(filename):
    text = read_file(filename)
    d = text_to_json_dict(text)
    G = adjacency_list_to_graph(d['adjacency'])
    return G


# def main():
#     G = get_graph_from_id(27)
#     
#     G2 = get_graph_from_id(21)
# 
#     length = int(min(len(G.nodes()), len(G2.nodes())) * .9)
#     
#     n_pair_subgraphs = 0
#     n_isomorphic = 0
#     for subgraphs in subgraphs_product(G, G2, length):
#         n_pair_subgraphs += 1
#         if nx.is_isomorphic(subgraphs[0], subgraphs[1]):
#             n_isomorphic += 1
#             print('a = %s' % subgraphs[0].edges())
#             print('b = %s' % subgraphs[1].edges())
# 
#     print('total = %d, isomorphic = %d' % (n_pair_subgraphs, n_isomorphic))


def check_similarity(filename_a, filename_b, expected_similarity):
    expected_similarity = float(expected_similarity)
    assert expected_similarity <= 1.0
    
    def sizeof_graph(g):
        return len(g.nodes())

    G_a = get_graph_from_filename(filename_a)
    G_b = get_graph_from_filename(filename_b)

    # always a < b
    if sizeof_graph(G_a) > sizeof_graph(G_b):
        G_a, G_b = G_b, G_a

    length = int((sizeof_graph(G_a) + sizeof_graph(G_b)) / 2.0 * expected_similarity)

    # print('length = %s, G_a_size = %s, G_b_size = %s' %(length, G_a_size, G_b_size))
    if length > sizeof_graph(G_a):
        # size difference too high, return false directly
        return False

    count = 0
    for subgraphs in subgraphs_product(G_a, G_b, length):
        count += 1
        # print(count)
        if nx.is_isomorphic(subgraphs[0], subgraphs[1]):
            return True

    return False



if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('Usage:')
        print('\tnetwork_similarity json_file_a json_file_b expected_similarity_value')

    else:
        res = check_similarity(sys.argv[1], sys.argv[2], sys.argv[3])
        print(res)
