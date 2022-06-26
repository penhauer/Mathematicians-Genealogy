import networkx as nx
from IPython.display import SVG
import numpy as np
import matplotlib.pyplot as plt
from sknetwork.data import karate_club, painters, movie_actor
from sknetwork.ranking import PageRank
from sknetwork.visualization import svg_graph, svg_digraph, svg_bigraph


# graph = karate_club(metadata=True)
# adjacency = graph.adjacency
# position = graph.position
#
# # PageRank
# pagerank = PageRank()
# scores = pagerank.fit_transform(adjacency)
#
# image = svg_graph(adjacency, position, scores=np.log(scores))
# SVG(image)

import matplotlib.pyplot as plt


def show_graph_with_labels(adjacency_matrix):
    mylabels = ['a', 'b', 'c', 'd']
    rows, cols = np.where(adjacency_matrix == 1)
    edges = zip(rows.tolist(), cols.tolist())
    gr = nx.Graph()
    gr.add_edges_from(edges)
    nx.draw(gr, node_size=500, labels=mylabels, with_labels=True)
    plt.show()




G = nx.DiGraph(nx.path_graph(4))


mat = np.matrix(
    [
        [1, 0, 0, 0],
        [1, 0, 0, 0],
        [1, 0, 1, 0],
        [1, 0, 0, 0],
    ]
)

# show_graph_with_labels(mat)


G = nx.from_numpy_matrix(mat)

pr = nx.pagerank(G, alpha=0.9)
print(pr)

nx.draw_networkx(G)
plt.show()
