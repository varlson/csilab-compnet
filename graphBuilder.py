import matplotlib.pyplot as plt
from utility import makeFolder, np

def graphBuilder(g, removalTypes, metrics, network, folder, option=1):
    N = float(g.vcount())
    nodes = [x/N for x in range(0, g.vcount()+1)]
    plt.xlabel("nodes")
    
    removalTypes = [removalTypes] if not isinstance(removalTypes, list) else removalTypes
    metrics = [metrics] if not isinstance(metrics, list) else metrics

    for metric, removalType in zip(metrics, removalTypes):
    	R = sum(metric[1:])/len(metric)
    	R = str(R)[:5]
    	plt.plot(nodes, metric, label = removalType+' '+R)
    
    plt.title("Rede de "+network)
    # plt.title("Rede de Passageiros de "+network[3:])
    plt.xlabel(r'$f$', fontsize=14)
    if option == 1:
        plt.ylabel(r'$P_\infty(f) / P_\infty(0)$', fontsize=14)
    elif option ==3:
        plt.ylabel(r'$ \parallel W \parallel(f) / \parallel W \parallel(0)$', fontsize=16)
    else:
        plt.ylabel(r'$ E (f) / E (0)$', fontsize=16)
    plt.legend()
    plt.margins(x = 0.02, y = 0.02)
    # plt.set_aspect('equal')
    makeFolder(folder)
     
    plt.savefig(folder+'/'+network+".png")
    plt.clf()

def robustness(ymeans, ystd, outputFolder, type):

    ymeans = np.asarray(ymeans)
    ystd = np.asarray(ystd)
    chose = {
        1:'GiantComponent',
        2:'Efficiency',
        3:'TotalFlow',
    }
    makeFolder(outputFolder)

    file =  lambda type: chose.get(type)
    x = ['Degr', 'Betw', 'BetW', 'Stre', 'Vuln', 'VulW', 'Rand']
    plt.plot(x, ymeans, 'yo-', color="g")
    plt.fill_between(x, ymeans-ystd, ymeans+ystd, alpha=.1)
    plt.xticks(rotation=45)
    name = str(file(type))
    plt.title(name)
    plt.xlabel('Metrics')
    plt.ylabel('Robustness')
    plt.savefig(outputFolder+'/'+name+'.png')


def auxRebPloter(x, yMean, yStd, _label, type):
    _color  = ''
    if type==1:
        _color = 'Green'
    elif type ==2:
        _color='Blue'
    else:
        _color ='Black'

    plt.plot(x, yMean, 'yo-', label=_label, color=_color)
    plt.fill_between(x, yMean-yStd, yMean+yStd, alpha=.1)
    # plt.errorbar(x, yMean, yerr=yStd, fmt="o")
    plt.xticks(rotation=45)


def allRobusteness(yGiant, yEff, yFlow, outputFolder):
    
    makeFolder(outputFolder)
    yGiantMeans = np.asarray([np.mean(x) for x in yGiant])
    yEffMeans = np.asarray([np.mean(x) for x in yEff])
    yFlowMeans = np.asarray([np.mean(x) for x in yFlow])

    yGiantStd = np.std(yGiantMeans)
    yEffStd = np.std(yEffMeans)
    yFlowStd = np.std(yFlowMeans)


    x = ['Degr', 'Betw', 'BetW', 'Stre', 'Vuln', 'VulW', 'Rand']
    auxRebPloter(x, yGiantMeans, yGiantStd,'GiantComponent', 1)
    auxRebPloter(x, yEffMeans, yEffStd,'Efficiency', 2)
    auxRebPloter(x, yFlowMeans, yFlowStd,'TotalFlow', 3)
 
    # plt.title(name)
    plt.xlabel('Metrics')
    plt.ylabel('Robustness')
    plt.legend()
    plt.savefig(outputFolder+'/'+'all'+'.png')