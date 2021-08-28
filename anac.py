from randonCorres import*
# from graphBuilder import graphBuilder
# from metricExtractor import extractor


def main(g, folder):

    randon_main(g.copy(), folder+'/randon')    
    metrics  = extractor(g, 1)
<<<<<<< HEAD
    graphBuilder(g, metrics[1], metrics[0], 'giant', 'anac/terrestrial/GiantComponent', 1)

    metrics  = extractor(g, 2)
    graphBuilder(g, metrics[1], metrics[0], 'eff', 'anac/terrestrial/Effienciy', 2)

    metrics  = extractor(g, 3)
    graphBuilder(g, metrics[1], metrics[0], 'flow', 'anac/terrestrial/TotalFlow', 3)
=======
    graphBuilder(g, metrics[1], metrics[0], 'GiantComponent', folder, 1)

    metrics  = extractor(g, 2)
    graphBuilder(g, metrics[1], metrics[0], 'Effienciy', folder, 2)

    metrics  = extractor(g, 3)
    graphBuilder(g, metrics[1], metrics[0], 'TotalFlow', folder, 3)
>>>>>>> 6b32480561ad7fb3751a8e83770942b53a1cd12e


# g = Graph.Read_GraphML('rmsp.GraphML')

<<<<<<< HEAD
main(g)
=======
from netGenerator import _main
g = _main('pas2010')
main(g, 'ibge')
>>>>>>> 6b32480561ad7fb3751a8e83770942b53a1cd12e
