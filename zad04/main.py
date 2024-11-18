"""
Zaimplementuj algorytm Christofidesa - zwróć uwagę na weryfikację warunku trójkąta na początku działania algorytmu.

Algorytm Christofidesa:
Niech G będzie grafem pełnym.
1. Dla G stwórzmy minimalne drzewo rozpinające T.
2. Niech O będzie zbiorem wierzchołków o nieparzystym stopniu w T. Znajdźmy minimalne skojarzenie doskonałe M na wierzchołkach O spośród krawędzi grafu pełnego G.
3. Niech H będzie multigrafem utworzonym z M i T.
4. Wyznaczamy cykl Eulera w grafie H (graf H jest Eulerowski ponieważ ma wszystkie wierzchołki parzystego stopnia).
5. Z cyklu Eulera zróbmy cykl Hamiltona poprzez pomijanie odwiedzonych wierzchołków (skracanie).

"""

import networkx as nx
import matplotlib.pyplot as plt

def check_triangle_inequality(graph):
    for u, v in graph.edges:
        for w in graph.nodes:
            if w != u and w != v:
                if graph[u][v]['weight'] > graph[u][w]['weight'] + graph[w][v]['weight']:
                    return False
    return True


def christofides(graph):
    if not check_triangle_inequality(graph):
        raise ValueError("Graf nie spełnia warunku nierówności trójkąta.")
    
    expected_edges = len(graph.nodes) * (len(graph.nodes) - 1) // 2
    if graph.number_of_edges() != expected_edges:
        raise ValueError("Graf nie jest pełny. Algorytm Christofidesa wymaga pełnego grafu.")
    print("Graf jest pełny.\n")
    
    mst = nx.minimum_spanning_tree(graph, weight='weight')
    print(f"Minimalne drzewo spinające T: {list(mst)}\n")
    
    odd_degree_nodes = [v for v in mst.nodes if mst.degree[v] % 2 != 0]
    print(f"Zbiór O - wierzchołki o nieparzystym stopniu z T: {odd_degree_nodes}\n")

    subgraph = graph.subgraph(odd_degree_nodes)
    matching = nx.algorithms.matching.min_weight_matching(
        subgraph, weight='weight'
    )
    print(f"Podgraf G z wierzchołkami O: {list(subgraph.edges)}\n")
    
    multigraph = nx.MultiGraph(mst)
    for u, v in matching:
        multigraph.add_edge(u, v, weight=graph[u][v]['weight'])
    print(f"Podgraf po połączeniu zbioru M i T: {[(u, v) for u, v, _ in multigraph.edges(data=True)]}\n")

    plt.figure(figsize=(12, 10))
    pos = nx.circular_layout(graph)
    
    nx.draw(mst, pos, with_labels=True, node_size=700, node_color='lightblue', font_size=10, font_weight='bold')
    nx.draw_networkx_edges(mst, pos, edgelist=mst.edges(), width=2, edge_color='green', label="Drzewo spinające T")
    
    nx.draw(subgraph, pos, with_labels=False, node_size=700, edge_color='orange', width=2, style='dashed', label="Podgraf G")
    
    nx.draw_networkx_nodes(mst, pos, nodelist=odd_degree_nodes, node_size=700, node_color='orange')
    
    x_values, y_values = zip(*pos.values())
    text_x = min(x_values) - 0
    text_y = max(y_values) - 0.01
    
    for u, v, data in subgraph.edges(data=True):
        mid_point = (pos[u] + pos[v]) / 2
        weight = data.get('weight', 1)
        plt.text(
            mid_point[0], mid_point[1], str(weight),
            color="white", fontsize=12, fontweight='bold', ha='center', va='center',
            bbox=dict(facecolor='black', edgecolor='black', boxstyle='round,pad=0.3')
        )

    for u, v, data in mst.edges(data=True):
        mid_point = (pos[u] + pos[v]) / 2
        weight = data.get('weight', 1)
        plt.text(
            mid_point[0], mid_point[1], str(weight),
            color="white", fontsize=12, fontweight='bold', ha='center', va='center',
            bbox=dict(facecolor='green', edgecolor='green', boxstyle='round,pad=0.3')
        )

    message = (
        f"Minimalne drzewo spinające T: {list(mst)}\n"
        f"Zbiór O - wierzchołki o nieparzystym stopniu z T: {odd_degree_nodes}\n"
        f"Podgraf G z wierzchołkami O: {list(subgraph.edges)}\n"
    )

    plt.text(
        text_x, text_y, message,
        fontsize=10,
        bbox=dict(boxstyle="round,pad=0.3", edgecolor="black", facecolor="lightyellow")
    )
    plt.axis("off")
    plt.show()

    eulerian_circuit = list(nx.eulerian_circuit(multigraph))
    eulerian_cycle = [u for u, v in eulerian_circuit] + [eulerian_circuit[0][0]]
    print(f"Cykl Eulera w grafie H: {eulerian_cycle}\n")
    
    hamiltonian_cycle = []
    visited = set()
    for u, v in eulerian_circuit:
        if u not in visited:
            hamiltonian_cycle.append(u)
            visited.add(u)
    hamiltonian_cycle.append(hamiltonian_cycle[0])
    
    return hamiltonian_cycle

def draw_graph_with_cycle(graph, cycle):
    pos = nx.circular_layout(graph)
    plt.figure(figsize=(10, 8))
    
    nx.draw(
        graph, pos, with_labels=True, node_size=700, node_color='lightblue',
        font_size=10, font_weight='bold', edge_color='gray'
    )
    
    for u, v, data in graph.edges(data=True):
        mid_point = (pos[u] + pos[v]) / 2
        weight = data.get('weight', 1)
        plt.text(
            mid_point[0], mid_point[1], str(weight),
            color="white", fontsize=12, fontweight='bold', ha='center', va='center',
            bbox=dict(facecolor='black', edgecolor='black', boxstyle='round,pad=0.3')
        )
    
    cycle_edges = [(cycle[i], cycle[i + 1]) for i in range(len(cycle) - 1)]
    nx.draw_networkx_edges(
        graph, pos, edgelist=cycle_edges, edge_color='red', width=2.5
    )
    
    cycle_message = f"Cykl Hamiltona:\n{" ⟶ ".join(map(str, cycle))}"
    x_values, y_values = zip(*pos.values())
    text_x = min(x_values) - 0.2
    text_y = max(y_values) + 0.2
    
    plt.xlim(min(x_values) - 0.5, max(x_values) + 0.5)
    plt.ylim(min(y_values) - 0.5, max(y_values) + 0.5)
    
    plt.text(
        text_x, text_y, cycle_message,
        fontsize=10,
        bbox=dict(boxstyle="round,pad=0.3", edgecolor="black", facecolor="lightyellow")
    )
    
    plt.title("Cykl Hamiltona w grafie", fontsize=15)
    plt.axis("off")
    plt.show()

def read_graph_from_file(filename):
    graph = nx.Graph()
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            if len(parts) != 3:
                raise ValueError(f"Nieprawidłowy format linii: {line}")
            u, v, w = map(int, parts)
            graph.add_edge(u, v, weight=w)
    return graph

if __name__ == "__main__":
    try:
        filename = "krawedzie.txt"
        G = read_graph_from_file(filename)
        
        cycle = christofides(G)
        print("Cykl Hamiltona:", cycle)
        
        draw_graph_with_cycle(G, cycle)

    except FileNotFoundError:
        print(f"Plik {filename} nie został znaleziony.")