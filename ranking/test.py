import networkx as nx
import matplotlib.pyplot as plt


def do_ranking(mat):
    # mat = np.matrix(
    #     [
    #         [1, 0, 0, 0],
    #         [1, 0, 0, 0],
    #         [1, 0, 1, 0],
    #         [1, 0, 0, 0],
    #     ]
    # )

    G = nx.from_numpy_matrix(mat)

    pr = nx.pagerank(G, alpha=0.9)
    print(pr)

    nx.draw_networkx(G)
    plt.show()
