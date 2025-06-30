import matplotlib.pyplot as plt
import networkx as nx

def visualize_diagnostic_graph(G, paths, node_dict, filename='diagnostic_graph.png'):
    plt.figure(figsize=(10, 8))
    node_colors = []

    for node in G.nodes:
        node_type = G.nodes[node]['type']
        node_colors.append('lightblue' if node_type == 'Symptom' else 'lightgreen' if node_type == 'Finding' else 'salmon')

    pos = nx.spring_layout(G, seed=42)
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=1000, alpha=0.8)
    nx.draw_networkx_edges(G, pos, edge_color='gray', width=1.0)

    path_colors = ['red', 'blue', 'purple']
    for i, path in enumerate(paths[:3]):
        path_edges = [(path[j], path[j+1]) for j in range(len(path)-1)]
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color=path_colors[i], width=2.5, style='dashed')

    labels = {node: G.nodes[node]['label'] for node in G.nodes}
    nx.draw_networkx_labels(G, pos, labels, font_size=10)

    edge_labels = {(u, v): f"{d['weight']:.2f}" for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=8)

    plt.title("Diagnostic Reasoning Graph for Fatigue and Polyuria (i2b2 Data)")
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
