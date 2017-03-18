import matplotlib.pyplot as plt

# sort the data and make a graph
def show_graph(graph, title, xlabel, ylabel):
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.plot(*zip(*sorted(graph.items())))
    
    
def show_two_graphs(graph1, graph2, title, xlabel, ylabel):
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.plot(*zip(*sorted(graph1.items())), label='one_level')
    plt.plot(*zip(*sorted(graph2.items())), label='two_level')
    plt.legend(loc=2)
    

