from random import random as rand
import numpy as np 
from os import path, mkdir
from igraph import Plot
from igraph.drawing.text import TextDrawer
#import cairo

def effGlobal(g, weighted=False): # global efficiency calculator
    eff= 0.0
    N = float(g.vcount())
    if weighted:
        _weight = np.array(g.es['weight'])
        _weight = np.array([1.0/x if x != 0.0 else 0 for x in _weight])
        for l in g.shortest_paths_dijkstra(weights = _weight):
            for ll in l:
                if(ll != 0):
                    eff+= (1.0/ll)
    else:
        for l in g.shortest_paths_dijkstra():
            for ll in l:
                if(ll != 0):
                    eff+= (1.0/ll)
    E = 0
    try:
        E = eff/(N*(N-1.0))
    except:
        pass
    
    return E

def calculator(g, weighted = False): # vulnerability calculator
    allEff = []
    eGlobal = effGlobal(g, weighted)
    for k in range(g.vcount()):
        g_copy = g.copy()
        list_of_ids = []

        for vertex_id in range(g_copy.vcount()):
            try:
                list_of_ids.append(g_copy.get_eid(k, vertex_id))
            except:
                pass
        g_copy.delete_edges(list_of_ids)
        aux = (eGlobal - effGlobal(g_copy,weighted))/eGlobal
        allEff.append(aux)

    _max = max(allEff)
    node_size = np.array(allEff)
    _min = min(allEff)

    node_size = 7+ ((node_size - _min) * (45 - 7))/(_max - _min)
    g.vs['size'] = node_size
    index = allEff.index(_max)
    return allEff


def randomRemovalgenerator(g, simulation=100):
    N = g.vcount()
    removaList = np.zeros(N+1)

    for i in range(simulation):
        gcopy = g.copy()
        removaList[0] += 1.0
        count=1
        while gcopy.vcount() > 1:
            index = rand() * gcopy.vcount()
            index = int(index)
            gcopy.delete_vertices(index)
            clusters = gcopy.components()
            if len(clusters) > 0:
                removaList[count] += max(clusters.sizes())/float(N)
                # print(clusters.sizes())
            else:
                removaList[count] += 0.0
            count = count+1 
    removaList = removaList/simulation
    return removaList 

def pairBuilder(g, metric):

    pair = []
    nodes = np.arange(0, g.vcount(), 1)
    
    for i in range(len(nodes)):
        pair.append((nodes[i], metric[i]))
    
    pair.sort(key = lambda x: x[1])
    pair.reverse()
    return pair


def makeFolder(folders):
    all = folders.split('/')
    walker = './'

    for i in range(len(all)):
        if i == 0:
            walker = walker+all[i]
        else:
            walker = walker+'/'+all[i]
        if not path.exists(walker):
            mkdir(walker)




def legend(g, name):
    # Construct the plot
    visual_style = {}
    visual_style['vertex_color'] = 'LightBlue'#DarkCyan
    visual_style['edge_color'] = 'Black'    
    makeFolder("GeneratedNetworks")
    plot = Plot("GeneratedNetworks/"+name+".png", bbox=(600, 650), background="White")

    # Create the graph and add it to the plot
    plot.add(g, bbox=(20, 70, 580, 630), ** visual_style)

    # Make the plot draw itself on the Cairo surface
    plot.redraw()

    # Grab the surface, construct a drawing context and a TextDrawer
 #   ctx = cairo.Context(plot.surface)
  #  ctx.set_font_size(36)
   # drawer = TextDrawer(ctx, "Eff Glob "+name, halign=TextDrawer.BOTTOM, )
    #drawer.draw_at(0, 50, width=600)

    # Save the plot
    # plot.save()
    #return plot
