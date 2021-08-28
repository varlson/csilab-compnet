from utility import  makeFolder, pairBuilder, effGlobal
from igraph import *
from igraph.drawing.text import TextDrawer
import cairo

def step_by_step(graph, folder):

    makeFolder(folder)
    g = graph.copy()
    count =1
    pair = pairBuilder(g, g.degree())
    while g.vcount() > 1:

        E = str(effGlobal(g))[:5]    
        index = g.vs.find(code = pair[count-1][1]).index
        g.vs[index]['size'] = 50
        pl = plot(g, folder+'/'+str(count)+'.png', layout='circle')    
        
        pl.redraw()
        ctx = cairo.Context(pl.surface)
        ctx.set_font_size(35)

        drawer = TextDrawer(ctx, "Eff Glob = "+E, halign=TextDrawer.BOTTOM, )
        drawer.draw_at(1, 50, width=1000)
        pl.save()
        g.delete_vertices(index)
        
        count+=1

def main(size):

    g = Graph.GRG(size, 0.5)
    g.vs['code'] = g.degree()
    g.vs['label'] = [x for x in range(g.vcount())]
    step_by_step(g, 'effDemo')

main(10)
