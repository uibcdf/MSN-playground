import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import networkx as nx
import pathlib
import matplotlib.colors as colors


def pkl2graphml(archivo):
    
    Gx = nx.read_gpickle(archivo)
    N = Gx.number_of_nodes()
    M = Gx.number_of_edges()

    print("nodos = ",N)
    print("edges = ",M)

    print("Weighted:", nx.is_weighted(Gx))
    print("Directed:", nx.is_directed(Gx))

    name = archivo.split("/")[1].split(".")[0]

    nx.write_graphml(Gx,name+".graphml")
    
    print("Network saved as "+name+".graphml")
    
    

def draw_network(G,im,name,etiquetas=False):

    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(8, 6))
    
    if not bool(im.get_names()):
        communities = [c - 1 for c in nx.get_node_attributes(G, "community").values()]
        num_communities = max(communities) + 1
    else:
        communities = list(im.get_modules().values())
        num_communities = len(communities)+1

    cmap_light = colors.ListedColormap(
        ["#a6cee3", "#b2df8a", "#fb9a99", "#fdbf6f", "#cab2d6"],
        "indexed",
        num_communities,
    )
    cmap_dark = colors.ListedColormap(
        ["#1f78b4", "#33a02c", "#e31a1c", "#ff7f00", "#6a3d9a"],
        "indexed",
        num_communities,
    )

    # edges
    nx.draw_networkx_edges(G, pos, alpha=0.5)

    # nodes
    node_collection = nx.draw_networkx_nodes(
        G, pos=pos, node_color=communities, node_size = 50, cmap=cmap_light
    )

    dark_colors = [cmap_dark(v) for v in communities]
    node_collection.set_edgecolor(dark_colors)
    
    if etiquetas:
        if not bool(im.get_names()):
            for n in G.nodes:
                plt.annotate(
                    n,
                    xy=pos[n],
                    textcoords="offset points",
                    horizontalalignment="center",
                    verticalalignment="center",
                    xytext=[0, 2],
                    color=cmap_dark(communities[n]),
                )
        else:
            i=0
            for n in G.nodes:            
                plt.annotate(
                    n,
                    xy=pos[n],
                    textcoords="offset points",
                    horizontalalignment="center",
                    verticalalignment="center",
                    xytext=[0, 2],
                    color=cmap_dark(communities[i]),                
                    # index = communities.index(n),
                    # color=cmap_dark(communities[index]),
                )
                i=i+1


    
    plt.title(name+" Network with Community Detection (Infomap)")
    
    plt.axis("off")
    pathlib.Path("output").mkdir(exist_ok=True)
    output = "output/"+name+"_Infomap.png"
    
    print("Writing network figure to "+output)
    plt.savefig(output)





def CuentaMembresias2df(Membs):
    N = 0
    MembsL = Membs.tolist()
    Mods = []
    Nodos = []
    j = 1
    for memb in set(MembsL):
        num = MembsL.count(memb)
        Mods.append(j)
        Nodos.append(num)
        # print(num,"nodos en el modulo",j)
        N = N + num
        j = j+1
    print(N,"nodos totales")
    print(len(Mods),"Modulos")
    
    dict = {'Nodos': Nodos, 'Modulo': Mods}
    df = pd.DataFrame(dict)
    df = df.sort_values('Nodos', ascending=False)
    
    df = df.reset_index(drop=True)
    
    return df
    
    
def CuentaMembresias(Membs):
    N = 0
    MembsL = Membs.tolist()
    for i in set(MembsL):
        num = MembsL.count(i)
        print(num,"nodos en el modulo",i+1)
        N = N + num
    print(N,"nodos totales")    
    
def toProbMatrix(M2,Membs):
    
    nM = []

    MembsL = Membs.tolist()
    for i in set(MembsL):
        num = MembsL.count(i)
        nM.append(num)
        
    N = len(nM)
        
    P = np.zeros((N,N))
        
    for i in range(len(nM)):
        for j in range(len(nM)):
            P[i,j] = (M2[i,j])/(nM[i]*nM[j])
    return P    
