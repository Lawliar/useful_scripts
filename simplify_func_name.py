import os
import sys
import networkx as nx
import pydot
from IPython import embed

# import write_dot
try:
    import pygraphviz
    from networkx.drawing.nx_agraph import write_dot
    print("using package pygraphviz")
except ImportError:
    try:
        import pydot
        from networkx.drawing.nx_pydot import write_dot
        print("using package pydot")
    except ImportError:
        print()
        print("Both pygraphviz and pydot were not found ")
        print("see  https://networkx.github.io/documentation/latest/reference/drawing.html")
        print()
        raise

filename = sys.argv[1]

# parse a .dot file into pydot object
pydot_g = pydot.graph_from_dot_file(filename)[0]

## transform a pydot object to a networkx graph
g = nx.drawing.nx_pydot.from_pydot(pydot_g)

nodes = list(g.nodes())

## some uninteresting functions
black_list = ["__cxx_global_var_in","Statistic","MDNode","atomic","_ZN4llvm","DenseMap","::~","Twine","llvm::isa"] 
white_list = ["AddressSanitizer","Analysis","ASan"]
for each_node in nodes:
    if "label" not in g.nodes[each_node]:
        continue
    label = g.nodes[each_node]['label']
    remove = True
    for each_str in white_list:
        if each_str in label:
            remove = False
            break
    if not remove:
        for each_str in black_list:
            if each_str in label:
                remove = True
                break
    if remove:
        g.remove_node(each_node)
        continue
    g.nodes[each_node]['label'] = label.replace("\"","").replace("{","").replace("}","")
embed()
write_dot(g,"simplified.dot")
