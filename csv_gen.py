from metricExtractor import totalFlowRemovalFuncion, giantComponent, efficiencyRemovalFuncion
from utility import calculator,randomRemovalgenerator, makeFolder, np, pairBuilder
import pandas as pd

switcher = {
    1: giantComponent, # GIANT COMPONENT
    2: totalFlowRemovalFuncion, # TOTAL FLOW
    3: efficiencyRemovalFuncion # EFFICIENCY
}
switcherFoder = {
    1:'csvOutPut/GianComponent',
    2:'csvOutPut/Efficiency',
    3:'csvOutPut/TotalFlow'
}
                    #temporary
from igraph import *
from random import randint 
    #TESTES
from importlib import reload
#g = Graph.GRG(20, 0.3)
#g.es['weight'] = [randint(10,40) for x in range(g.ecount())]

def csv_gen(g, folder, network="Network", key=1):

    dinamicFunction = lambda graph, netName, type: switcher.get(type)(graph,netName)
    dic = {}
    N = g.vcount()

    Nodes = [x for x in range(g.vcount()+1)]

    
    dic['Nodes'] = Nodes
    g.vs['code'] = g.degree()
    deg = np.asarray(dinamicFunction(g.copy(), pairBuilder(g.copy(), g.degree()), key))
    # deg = deg*N
    dic['Degree Removal %']  = deg
    

    g.vs['code'] = g.betweenness()
    bet = np.asarray(dinamicFunction(g.copy(), pairBuilder(g.copy(),g.betweenness()), key))
    # bet = bet*N
    dic['Betweenness Removal %']  = bet

    _weight = np.array(g.es['weight'])
    _weight = np.array([1.0/x if x != 0.0 else 0 for x in _weight])
    g.vs['code'] = g.betweenness(weights = _weight)
    bet = np.asarray(dinamicFunction(g.copy(), pairBuilder(g.copy(),g.betweenness(weights = _weight)), key))
    dic['Weighted Betweenness Removal %']  = bet



    
    g.vs['code'] = calculator(g)
    eff = np.asarray(dinamicFunction(g.copy(), pairBuilder(g.copy(), calculator(g)), key))
    # eff = deg*N
    dic['Efficiency Removal']  = eff
    
    random = randomRemovalgenerator(g)
    g.vs['code'] = random
    rand = dinamicFunction(g.copy(), pairBuilder(g.copy(), random), key)
    # rand = deg*N
    dic['Random Removal']  = rand

    Data = pd.DataFrame(dic)
    folder = folder+'/'+switcherFoder.get(key)
    makeFolder(folder)
    Data.to_csv(folder+'/'+network+'.csv', float_format='%.2f', encoding='utf-8', index=False)
    # return dic
