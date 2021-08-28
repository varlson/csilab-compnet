from graphBuilder import graphBuilder, robustness, plt, allRobusteness
import numpy as  np
from metricExtractor import extractor
from igraph import *
from netGenerator import _main
from csv_gen import csv_gen

def main(network):

    for net in network:
        g = _main(net)
        # csv_gen(g.copy(), 'csvOutPut', net)
        metrics = extractor(g.copy(), 1)
        graphBuilder(g, metrics[1], metrics[0], net, 'GeneratedGraph/GiantComponent', 1)

        # csv_gen(g.copy(),'csvOutPut', net, 2)
        metrics = extractor(g.copy(), 2)
        graphBuilder(g, metrics[1], metrics[0], net, 'GeneratedGraph/Efficiency', 2)

        # csv_gen(g.copy(),'csvOutPut', net, 3)
        metrics = extractor(g.copy(), 3)
        graphBuilder(g, metrics[1], metrics[0], net, 'GeneratedGraph/TotalFlow', 3)

def temporary(networks, type):
    deg = []
    bet = []
    betw = []
    stren = []
    vuln = []
    vulnw = []
    eff = []
    for net in networks:
        g = _main(net)
        metr = extractor(g,type)
        m  = metr[2]
        deg.append(m[0])
        bet.append(m[1])
        betw.append(m[2])
        stren.append(m[3])
        vuln.append(m[4])
        vulnw.append(m[5])
        eff.append(m[6])

    # print(mean(deg), mean(bet), mean(betw), mean(stren), mean(vuln), mean(vulnw), mean(eff))
    # return [[np.mean(deg), np.mean(bet), np.mean(betw), np.mean(stren), np.mean(vuln), np.mean(vulnw), np.mean(eff)],
    #         [np.std(deg), np.std(bet), np.std(betw), np.std(stren), np.std(vuln), np.std(vulnw), np.std(eff)]] 
        return [deg, bet, betw, stren, vuln, vulnw, eff] 
networks = ['pas2010', 'pas2005', 'pas2000', 'pas1995', 
            'pas1990', 'pas1985', 'pas1980', 'pas1975', 'pas1972']

# for i in range(1, 4):
#     s = temporary(networks, i)
#     robustness(s[0], s[1], 'robustness/fill_between', i)
#     plt.clf()

# giant = temporary(networks, 1)
# eff = temporary(networks, 2)
# flow = temporary(networks, 3)

# allRobusteness(giant, eff, flow, 'robustness/all_fiil_b')
main(networks)
