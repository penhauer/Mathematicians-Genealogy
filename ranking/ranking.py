import networkx as nx
import matplotlib.pyplot as plt

plt.rcParams["figure.figsize"] = (40, 22)

def do_ranking(mat):
    G = nx.from_numpy_matrix(mat)
    pr = nx.pagerank(G, alpha=0.9)
    hub, authority = nx.hits(G)

    print(pr)
    print(hub, authority)

    nx.draw_networkx(G)
    plt.show()
