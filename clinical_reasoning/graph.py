import networkx as nx

def create_diagnostic_graph(concepts, relations):
    G = nx.DiGraph()
    node_dict = {}

    for i, (text, cui, ctype, score) in enumerate(concepts):
        node_id = f"N{i}"
        node_dict[text] = node_id
        G.add_node(node_id, label=text, type=ctype, cui=cui)
    
    for src, tgt, weight in relations:
        if src in node_dict and tgt in node_dict:
            G.add_edge(node_dict[src], node_dict[tgt], weight=min(weight, 0.95))

    return G, node_dict
