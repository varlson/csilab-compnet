from utility import *


def giantComponent(g, pair):
    N = g.vcount()
    giantComp = np.zeros(N+1)
    giantComp[0] = 1.0
    clusters = g.components()
    P = max(clusters.sizes())

    gcp = g.copy()
    count =1
    while gcp.vcount() > 1:     
        index = gcp.vs.find(code = pair[count-1][1]).index
        gcp.delete_vertices(index)
        clusters = gcp.components()
        giantComp[count] =  max(clusters.sizes())/P
        count+=1
    giantComp[N] = 1/P
    return giantComp


def totalFlowRemovalFuncion(g, pair):
    attribute="weight"
    totalFlow = np.zeros(g.vcount()+1)
    totalFlow[0] = 1.0
    F = sum(g.es[attribute])
    gcp = g.copy()

    count =1
    while gcp.vcount() > 1:
        index = gcp.vs.find(code = pair[count-1][1]).index
        gcp.delete_vertices(index)
        totalFlow[count] = sum(gcp.es[attribute])/F
        count+=1
    return totalFlow

def efficiencyRemovalFuncion(g, pair):
    effTotal = np.zeros(g.vcount()+1)
    E = effGlobal(g)
    effTotal[0] = 1.0
    
    gcp = g.copy()

    count =1
    while gcp.vcount() > 1:
        index = gcp.vs.find(code = pair[count-1][1]).index
        gcp.delete_vertices(index)
        effTotal[count] = effGlobal(gcp)/E
        count+=1
    return effTotal


def extractor(g, type=1):
     


    flag = True
    _weight=0
    switcher = {
        1: giantComponent,
        2: efficiencyRemovalFuncion,
        3: totalFlowRemovalFuncion
    }

    meanValue = []
    metricList = []
    N =g.vcount()
    metricNameList = []
    dinamicFunction = lambda graph, met, typ: switcher.get(typ)(graph, met)

     # DEGREE
    g.vs['code'] = g.degree()
    degree_removal_list = dinamicFunction(g.copy(),pairBuilder(g.copy(), g.degree()), type)
    metricList.append(degree_removal_list)
    metricNameList.append("Degree")
    meanValue.append(sum(degree_removal_list[1:])/len(degree_removal_list))

    #  BETWEENNESS WITHOUT WEIGHT
    g.vs['code'] = g.betweenness()
    betweenness_removal_list = dinamicFunction(g.copy(),pairBuilder(g.copy(), g.betweenness()), type)
    metricList.append(betweenness_removal_list)
    metricNameList.append("Betweenness")
    meanValue.append(sum(betweenness_removal_list[1:])/len(betweenness_removal_list))
    try:
        _weight = np.array(g.es['weight'])
    except:
        flag = False
    
    if flag:
        strength = g.strength(weights = _weight)
        g.vs['code'] = strength
        strength_removal_list = dinamicFunction(g.copy(), pairBuilder(g.copy(), strength), type)
        metricList.append(strength_removal_list)
        metricNameList.append("Strength")
        meanValue.append(sum(strength_removal_list[1:])/len(strength_removal_list))

    if flag:
    #BETWEENNESS WITH WEIGHT
        _weight = np.array([1.0/x if x >= 0.0 else 0 for x in _weight])
        g.vs['code'] = g.betweenness(weights = _weight)
        betweenness_removal_list = dinamicFunction(g.copy(), pairBuilder(g.copy(), g.betweenness(weights = _weight)),type)
        metricList.append(betweenness_removal_list)
        metricNameList.append("Betweenness with Weights")
        meanValue.append(sum( betweenness_removal_list[1:])/len(betweenness_removal_list))
    



    #  # VULNERABILITY
    vulnerability = calculator(g.copy())
    g.vs['code'] = vulnerability
    vulnerability_removal_list = dinamicFunction(g.copy(),pairBuilder(g.copy(), vulnerability), type)
    metricList.append(vulnerability_removal_list)
    metricNameList.append("Vulnerability")
    meanValue.append(sum(vulnerability_removal_list[1:])/len(vulnerability_removal_list))

    
    # # # VULNERABILITY WITH WEIGHTS
    if flag:
        vulnerability = calculator(g.copy(), True)
        g.vs['code'] = vulnerability
        vulnerability_removal_list = dinamicFunction(g.copy(), pairBuilder(g.copy(), vulnerability), type)
        metricList.append(vulnerability_removal_list)
        metricNameList.append("Vulnerability with Weights")
        meanValue.append(sum(vulnerability_removal_list[1:])/len(vulnerability_removal_list))

    
    # # RANDOM REMOVAL
    
    random_removal_list = randomRemovalgenerator(g.copy(), 100)
    g.vs['code'] = random_removal_list
    metricList.append(random_removal_list)
    metricNameList.append("Random")
    meanValue.append(sum(random_removal_list[1:])/len(random_removal_list))

    return [metricList, metricNameList, meanValue]