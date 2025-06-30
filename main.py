from clinical_reasoning.data import clinical_notes
from clinical_reasoning.extraction import get_nlp_model, extract_concepts_and_relations
from clinical_reasoning.graph import create_diagnostic_graph
from clinical_reasoning.reasoning import (
    generate_reasoning_paths,
    compute_path_confidence,
    compute_path_entropy,
    compute_multi_path_uncertainty
)
from clinical_reasoning.visualization import visualize_diagnostic_graph

if __name__ == "__main__":
    nlp = get_nlp_model()
    concepts, relations = extract_concepts_and_relations(nlp, clinical_notes)
    G, node_dict = create_diagnostic_graph(concepts, relations)

    start_nodes = [node for node in G.nodes if G.nodes[node]['type'] == 'Symptom']
    end_nodes = [node for node in G.nodes if G.nodes[node]['type'] == 'Diagnosis']
    paths = generate_reasoning_paths(G, start_nodes, end_nodes)

    print("Reasoning Paths and Uncertainty Measures:")
    for i, path in enumerate(paths):
        node_labels = [G.nodes[node]['label'] for node in path]
        confidence = compute_path_confidence(G, path)
        entropy = compute_path_entropy(G, path)
        print(f"Path {i+1}: {' -> '.join(node_labels)}")
        print(f"  Confidence: {confidence:.4f}, Entropy: {entropy:.4f}")

    multi_path_uncertainty = compute_multi_path_uncertainty(G, paths)
    print(f"Multi-Path Uncertainty: {multi_path_uncertainty:.4f}")
    visualize_diagnostic_graph(G, paths, node_dict)
