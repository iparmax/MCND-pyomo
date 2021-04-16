import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

def network_dict(path):
    # Load Network
    df = pd.read_csv(path)
    network = {}
    operators = []
    for index, row in df.iterrows():
        network[row[0], row[1]] = row[2], row[3]
    return network

def get_network(links):
    G = nx.DiGraph()
    for i in links.values():
        G.add_node(i[0])
        G.add_node(i[1])
        G.add_edge(i[0],i[1])
    return G

def feas_paths(links,O,D):
    G = nx.DiGraph()
    for i in links.values():
        G.add_node(i[0])
        G.add_node(i[1])
        G.add_edge(i[0],i[1])

    r_feas = {}
    count = 1
    for i,j in zip(O,D): 
        for path in nx.all_simple_paths(G, source=i, target=j):
            r_feas[(count,i)] = path
            count+=1
    return r_feas

def plot_network(G):
    plt.subplot(121)
    nx.draw_shell(G, with_labels=True, font_weight='bold')
    plt.show()

def heads(G):
    heads = []
    heads_dict = {}
    for child in G.nodes: 
        parents = list(G.predecessors(child))
        for i in parents:
            heads.append((i,child))
    
    for node in G.nodes:
        count = 0 
        for j in heads:
            if j[0] == node:
                count+=1
                heads_dict[(node,count)] = j[1]

    return heads_dict

def tails(G):
    tails = []
    tails_dict = {}
    for child in G.nodes: 
        parents = list(G.successors(child))
        for i in parents:
            tails.append((i,child))
    
    for node in G.nodes:
        count = 0 
        for j in tails:
            if j[0] == node:
                count+=1
                tails_dict[(node,count)] = j[1]

    return tails_dict
