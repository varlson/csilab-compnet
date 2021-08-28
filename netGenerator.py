import pandas as pd
import numpy as np
from igraph import *
from math import pow

class GenNet:
    def __init__(self, data, name, delim=";"):

        dataFrame = pd.read_csv('csvFiles/'+data, delimiter=delim)
        # cities = pd.read_csv('csvFiles/cidades.csv', delimiter=";")
        coord = np.genfromtxt('csvFiles/cities_coord.csv', delimiter=",")

        desti = list(dataFrame['Cod-Dest'])
        source = list(dataFrame['Cod-orig'])

        pax = list(dataFrame['Pax'])
        ids = list(set(source+desti))
        # lst = list(cities['Codmundv'])
        # ids = list(set(ids+lst))
        n = len(ids)
        g = Graph()
        g.add_vertices(n)
        g.vs['id'] = ids

        for i in range(len(dataFrame)):
            src = g.vs.select(id_eq = source[i])[0].index
            dst = g.vs.select(id_eq = desti[i])[0].index
            g.add_edge(src,dst, weight=pax[i])

        p = (2*g.ecount())/(pow(n, 2))
        randomGraph2L = Graph.Erdos_Renyi(n, p)
        randomGraph2L.vs['id'] = g.vs['id']
        self.mine = g
        self.coord_setter(g, coord)
        self.plot(g, name)

        # self.coord_setter(randomGraph2L, coord)
        # self.plot(randomGraph2L, 'GeneratedNetworks/'+name+'RandomGraph2L.png')


    def coord_setter(self, g, coord):
        lst = coord.transpose()
        for i in range(g.vcount()):
            try:
                idx = list(lst[0]).index(g.vs[i]['id'])
            except:
                print(g.vs[i]['id'])
                pass
            # idx = list(lst[0]).index(g.vs[i]['id'])
            g.vs[i]['x'] = lst[1][idx]
            g.vs[i]['y'] = lst[2][idx] *(-1)

    def plot(self, g, name):
        visual_style = {}
        # visual_style['vertex_size'] =( (g.degree()/np.max(g.degree()))*10.0) +8
        try:
            visual_style['edge_width'] = (g.es['weight']/np.max(g.es['weight']))*10.0
        except:
            pass
        # visual_style['margin'] = 30
        # visual_style['vertex_color'] = 'Blue'
        # visual_style['edge_color'] = 'Black'
        # plot(g, name, ** visual_style)
        from utility import legend
        legend(g, name)
        
    def get(self):
        return self.mine



def _main(networkName):
    g = GenNet(networkName+'.csv', networkName)
    return g.get()

