from metricExtractor import extractor
from utility import np
from igraph import *
from graphBuilder import robustness, plt, graphBuilder
from csv_gen import csv_gen
deg = []
bet = []
betw = []
stren = []
vuln = []
vulnw = []
eff = []



def grapher(g):
    csv_gen(g.copy(), "Vinicios", 'giant',  1)
    metrics = extractor(g.copy(), 1)
    graphBuilder(g, metrics[1], metrics[0],'GiantComponent', "Vinicios/Graphs/Giant", 1)

    csv_gen(g.copy(), "Vinicios",'eff', 2)
    metrics = extractor(g.copy(), 2)
    graphBuilder(g, metrics[1], metrics[0],  'Efficiency', "Vinicios/Graphs/Effc", 2)

    csv_gen(g.copy(), "Vinicios",'flow', 3)
    metrics = extractor(g.copy(), 3)
    graphBuilder(g, metrics[1], metrics[0],  'TotalFlow',"Vinicios/Graphs/Flow",  3)


def vinic(g, type):
    metr = extractor(g,type)
    m  = metr[2]
    deg.append(m[0])
    bet.append(m[1])
    betw.append(m[2])
    stren.append(m[3])
    vuln.append(m[4])
    vulnw.append(m[5])
    eff.append(m[6])

    return [np.mean(deg), np.mean(bet), np.mean(betw), np.mean(stren), np.mean(vuln), np.mean(vulnw), np.mean(eff)]

def main(g):
    # grapher(g)
    for i in range(1, 4):
        s = vinic(g, i)
        robustness(s, 'Vinicios/Robustness/', i)
        plt.clf()

g = Graph.Read_GraphML('rmsp.GraphML')
main(g)