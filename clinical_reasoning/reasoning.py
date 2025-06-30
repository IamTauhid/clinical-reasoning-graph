import numpy as np
import networkx as nx
from itertools import combinations

def generate_reasoning_paths(G, start_nodes, end_nodes, max_length=3):
    paths = []
    for start in start_nodes:
        for end in end_nodes:
            for path in nx.all_simple_paths(G, start, end, cutoff=max_length):
                if len(path) > 1:
                    paths.append(path)
    return paths

def compute_path_confidence(G, path):
    confidence = 1.0
    for i in range(len(path) - 1):
        confidence *= G[path[i]][path[i+1]]['weight']
    return confidence

def compute_path_entropy(G, path):
    weights = [G[path[i]][path[i+1]]['weight'] for i in range(len(path) - 1)]
    weights = np.array(weights)
    entropy = -np.sum(weights * np.log(weights + 1e-10))
    return entropy

def compute_path_diversity(G, paths):
    if len(paths) < 2:
        return 0.0
    agreements = []
    for path_i, path_j in combinations(paths, 2):
        vertices_i = set(path_i)
        vertices_j = set(path_j)
        agreement = len(vertices_i.intersection(vertices_j)) / len(vertices_i.union(vertices_j))
        agreements.append(agreement)
    diversity = 1 - np.mean(agreements)
    return diversity

def compute_multi_path_uncertainty(G, paths):
    if not paths:
        return 0.0
    confidences = [compute_path_confidence(G, path) for path in paths]
    diversity = compute_path_diversity(G, paths)
    return diversity * (1 - np.mean(confidences))
