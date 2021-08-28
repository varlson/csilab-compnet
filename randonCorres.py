from math import pow
from igraph import *



def gen(g):
    n = g.vcount()
    p = (2 * g.ecount())/pow(n, 2)
    gRandom = Graph.Erdos_Renyi(n, p)
    return gRandom


from metricExtractor import extractor
from graphBuilder import graphBuilder
# from utility import makeFolder
def randon_main(g, folder):
    g = gen(g)
    
    metrics = extractor(g.copy(), 1)
    graphBuilder(g, metrics[1], metrics[0], 'GiantRandon', folder, 1)

    metrics = extractor(g.copy(), 2)
    graphBuilder(g, metrics[1], metrics[0], 'EficRandon', folder, 2)



