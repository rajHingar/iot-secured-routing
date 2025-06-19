import networkx as nx
import matplotlib.pyplot as plt

def draw_topology(graph, path=None):
    G = nx.Graph()

    # Build graph from dictionary
    for node in graph:
        for neighbor, weight in graph[node].items():
            G.add_edge(node, neighbor, weight=weight)

    pos = nx.spring_layout(G, seed=42)  # Consistent layout

    # Draw base network
    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=800, font_weight='bold')
    nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): d['weight'] for u, v, d in G.edges(data=True)})

    # Highlight shortest path
    if path:
        edge_list = list(zip(path, path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=edge_list, edge_color='red', width=3)

    plt.title("IoT Network Topology with Shortest Path")
    plt.show()
