"""
Zaimplementuj algorytm rozwiązujący problem chińskiego listonosza.
Do poszczególnych etapów algorytmu dozwolone jest użycie wbudowanych funkcji.

Rozważymy trzy przypadki:
Przypadek 1: Graf G jest eulerowski. Wówczas każdy cykl Eulera jest optymalnym rozwiązaniem, 
które można znaleźć korzystając np. z algorytmu Fleury'ego.

Przypadek 2: Graf g jest półeulerowski. Znajdujemy ścieżkę Eulera łączącą dwa wierzchołki nieparzystego 
stopnia u i v. Następnie szukamy najkrótszej drogi z u do v. Łącząc obie drogi otrzymujemy rozwiązanie.

Przypadek 3: 
1. Zidentyfikuj wierzchołki nieparzystego stopnia w grafie G. Niech W będzie zbiorem takich wierzchołków.
2. Skonstruuj obciążony graf pełny G' o zbiorze wierzchołków W, w którym waga krawędzi {u, v} 
   jest równa długości najkrótszej ścieżki łączącej u z v w wyjściowym grafie G.
3. Znajdź minimalne skojarzenie dokładne (ang. minimum weight perfect matching) M w grafie G'.
4. Dla każdej krawędzi e ∈ M dodaj krawędzie w grafie G, które odpowiadają najkrótszej ścieżce odpowiadającej e.
5. Nowo powstały graf jest eulerowski.
"""

import networkx as nx
from itertools import combinations
import matplotlib.pyplot as plt

def chinese_postman_problem(graph):
    odd_degree_nodes = [node for node in graph.nodes if graph.degree[node] % 2 != 0]
    odd_count = len(odd_degree_nodes)

    if odd_count == 0:
        
        eulerian_circuit = list(nx.eulerian_circuit(graph))
        path_text = " ⟶ ".join(str(u) for u, v in eulerian_circuit) + " ⟶ " + str(eulerian_circuit[0][0])
        
        plt.figure(figsize=(10, 8))
        pos = nx.spring_layout(graph)
        
        nx.draw(graph, pos, with_labels=True, node_size=700, node_color='lightblue', font_size=10, font_weight='bold', edge_color='gray')

        for u, v in eulerian_circuit:
            nx.draw_networkx_edges(graph, pos, edgelist=[(u, v)], edge_color='red', width=2.5)
            mid_point = (pos[u] + pos[v]) / 2
            weight = graph[u][v].get('weight', 1)
            plt.text(mid_point[0], mid_point[1], str(weight), color="white", fontsize=12, fontweight='bold', ha='center', va='center', 
                    bbox=dict(facecolor='black', edgecolor='black', boxstyle='round,pad=0.3'))
        
        x_values, y_values = zip(*pos.values())
        text_x = min(x_values) - 0.2
        text_y = max(y_values) + 0.2 

        plt.xlim(min(x_values) - 0.5, max(x_values) + 0.5)
        plt.ylim(min(y_values) - 0.5, max(y_values) + 0.5)

        plt.text(
            text_x, text_y, f"Ścieżka listonosza:\n{path_text}",
            fontsize=10, 
            bbox=dict(boxstyle="round,pad=0.3", edgecolor="black", facecolor="lightyellow")
        )
        
        plt.title("Cykl Eulera w grafie", fontsize=15)
        plt.axis("off")
        plt.show()
        
        print("Graf jest eulerowski.")
        print(f"Ścieżka listonosza: {path_text}")

    elif odd_count == 2:
        start, end = odd_degree_nodes[0], odd_degree_nodes[1]
        
        shortest_path = nx.dijkstra_path(graph, source=start, target=end)
        shortest_path_text = " ⟶ ".join(map(str, shortest_path))

        shortest_path_reversed = shortest_path[::-1]
        shortest_path_reversed_text = " ⟶ ".join(map(str, shortest_path_reversed))

        for i in range(len(shortest_path) - 1):
            u, v = shortest_path[i], shortest_path[i + 1]
            if not graph.has_edge(u, v):
                graph.add_edge(u, v, weight=1)

        eulerian_path = list(nx.eulerian_path(graph, source=start))
        eulerian_path_text = " ⟶ ".join(str(u) for u, v in eulerian_path) + " ⟶ " + str(eulerian_path[-1][1])

        postman_path = eulerian_path_text+shortest_path_reversed_text[1:]

        plt.figure(figsize=(10, 8))
        pos = nx.spring_layout(graph)

        nx.draw(graph, pos, with_labels=True, node_size=700, node_color='lightblue', font_size=10, font_weight='bold', edge_color='gray')

        for u, v in eulerian_path:
            nx.draw_networkx_edges(graph, pos, edgelist=[(u, v)], edge_color='red', width=2.5)
            mid_point = (pos[u] + pos[v]) / 2
            weight = graph[u][v].get('weight', 1)
            plt.text(mid_point[0], mid_point[1], str(weight), color="white", fontsize=12, fontweight='bold', ha='center', va='center',
                     bbox=dict(facecolor='black', edgecolor='black', boxstyle='round,pad=0.3'))

        for i in range(len(shortest_path) - 1):
            u, v = shortest_path[i], shortest_path[i + 1]
            nx.draw_networkx_edges(graph, pos, edgelist=[(u, v)], edge_color='green', width=3)

        x_values, y_values = zip(*pos.values())
        text_x = min(x_values) - 0.2
        text_y = max(y_values) + 0.2

        plt.xlim(min(x_values) - 0.5, max(x_values) + 0.5)
        plt.ylim(min(y_values) - 0.5, max(y_values) + 0.5)

        message = (
            f"Droga Eulera: {eulerian_path_text}\n"
            f"Najkrótsza droga z {start} do {end}: {shortest_path_text}\n"
            f"Trasa listonosza: {postman_path}"
        )

        plt.text(
            text_x, text_y, message,
            fontsize=10,
            bbox=dict(boxstyle="round,pad=0.3", edgecolor="black", facecolor="lightyellow")
        )

        plt.title("Ścieżka Eulera w grafie", fontsize=15)
        plt.axis("off")
        plt.show()

        print("Graf jest półeulerowski.")
        print(
            f"Droga Eulera: {eulerian_path_text}\n"
            f"Najkrótsza droga z {start} do {end}: {shortest_path_text}\n"
            f"Trasa listonosza: {postman_path}"
        )

    else:
        print("Graf nie jest ani eulerowski ani półeulerowski.")

        plt.figure(figsize=(10, 8))
        pos = nx.spring_layout(graph)
        nx.draw(graph, pos, with_labels=True, node_size=700, node_color='lightblue', font_size=12, font_weight='bold', edge_color='gray')
        for u, v in graph.edges():
            mid_point = (pos[u] + pos[v]) / 2
            weight = graph[u][v].get('weight', 1)
            plt.text(mid_point[0], mid_point[1], str(weight), color="white", fontsize=12, fontweight='bold', ha='center', va='center',
                    bbox=dict(facecolor='black', edgecolor='black', boxstyle='round,pad=0.3'))

        plt.show()

        print(f"Wierzchołki nieparzystego stopnia: {odd_degree_nodes}")
        
        odd_pairs = list(combinations(odd_degree_nodes, 2))
        G_prime = nx.Graph()
        for u, v in odd_pairs:
            G_prime.add_edge(u, v, weight=nx.dijkstra_path_length(graph, u, v))

        print("Krawędzie w G':")
        for u, v, w in G_prime.edges(data='weight'):
            print(f"{u} - {v}, waga: {w}")

        min_weight_matching = nx.algorithms.matching.min_weight_matching(G_prime)            

        plt.figure(figsize=(10, 8))
        pos = nx.spring_layout(G_prime)
        
        nx.draw(G_prime, pos, with_labels=True, node_size=700, node_color='lightblue', font_size=10, font_weight='bold', edge_color='gray')

        for u, v in G_prime.edges():
            mid_point = (pos[u] + pos[v]) / 2
            weight = G_prime[u][v].get('weight', 1)
            offset = 0.05 if pos[u][0] > pos[v][0] else -0.05
            plt.text(mid_point[0] + offset, mid_point[1] + offset, str(weight), color="white", fontsize=12, fontweight='bold', ha='center', va='center',
                    bbox=dict(facecolor='black', edgecolor='black', boxstyle='round,pad=0.3'))

        for u, v in min_weight_matching:
            nx.draw_networkx_edges(G_prime, pos, edgelist=[(u, v)], edge_color='red', width=2.5)

        matching_text = "Minimalne skojarzenie:\n"
        for u, v in min_weight_matching:
            matching_text += f"Wierzchołki {u} i {v} (waga: {G_prime[u][v]['weight']})\n"

        shortest_paths_text = "Najkrótsze ścieżki między wszystkimi parami wierzchołków w G':\n"
        for u, v in combinations(G_prime.nodes, 2):
            shortest_path = nx.shortest_path(graph, source=u, target=v, weight='weight')
            path_str =  " ⟶ ".join(map(str, shortest_path))
            shortest_path_weight = nx.shortest_path_length(graph, source=u, target=v, weight='weight')
            shortest_paths_text += f"Wierzchołki {u} i {v}. Ścieżka: {path_str} (długość: {shortest_path_weight})\n"

        message = f"{matching_text}\n{shortest_paths_text}"
        x_values, y_values = zip(*pos.values())
        text_x = min(x_values) - 0.4
        text_y = max(y_values) - 0.4

        plt.xlim(min(x_values) - 0.5, max(x_values) + 0.5)
        plt.ylim(min(y_values) - 0.5, max(y_values) + 0.5)

        plt.text(text_x, text_y, message, fontsize=10, bbox=dict(boxstyle="round,pad=0.3", edgecolor="black", facecolor="lightyellow", alpha=0.6))

        plt.title("Graf G' z minimalnym skojarzeniem i najkrótszymi ścieżkami", fontsize=15)
        plt.axis("off")
        plt.show()

        print("Minimalne skojarzenie:", min_weight_matching)

        for u, v in min_weight_matching:
            shortest_path = nx.shortest_path(graph, source=u, target=v, weight='weight')
            shortest_path_weight = nx.shortest_path_length(graph, source=u, target=v, weight='weight')
            
            graph.add_edge(u, v, weight=shortest_path_weight)
            
            print(f"Dodano krawędź między {u} a {v} o wadze {shortest_path_weight}, odpowiadającą najkrótszej ścieżce {shortest_path}")

        try:
            eulerian_circuit = list(nx.eulerian_circuit(graph))
            path_text = " ⟶ ".join(str(u) for u, v in eulerian_circuit) + " ⟶ " + str(eulerian_circuit[0][0])

            plt.figure(figsize=(10, 8))
            pos = nx.spring_layout(graph)

            nx.draw(graph, pos, with_labels=True, node_size=700, node_color='lightblue', font_size=12, font_weight='bold', edge_color='gray')

            for u, v in eulerian_circuit:
                nx.draw_networkx_edges(graph, pos, edgelist=[(u, v)], edge_color='red', width=2.5)

            for u, v, data in graph.edges(data=True):
                mid_point = (pos[u] + pos[v]) / 2
                weight = data['weight']
                plt.text(mid_point[0], mid_point[1], str(weight), color="white", fontsize=12, fontweight='bold', ha='center', va='center', bbox=dict(facecolor='black', edgecolor='black', boxstyle='round,pad=0.3'))

            x_values, y_values = zip(*pos.values())
            text_x = min(x_values) - 0.4
            text_y = max(y_values) + 0.2

            plt.xlim(min(x_values) - 0.5, max(x_values) + 0.5)
            plt.ylim(min(y_values) - 0.5, max(y_values) + 0.5)

            message = f"Cykl Eulera: {path_text}"

            plt.text(
                text_x, text_y, message,
                fontsize=12,
                bbox=dict(boxstyle="round,pad=0.3", edgecolor="black", facecolor="lightyellow")
            )

            plt.title("Cykl Eulera w grafie", fontsize=15)
            plt.axis("off")
            plt.show()

            print("Nowo utworzony graf jest eulerowski.")
            print(f"Cykl Eulera: {path_text}")

        except nx.NetworkXError:
            print("Błąd: Graf nadal nie jest eulerowski po dodaniu krawędzi.")        


def main():
    def load_edges_from_file(file_path):
        edges = []
        with open(file_path, 'r') as file:
            for line in file:
                u, v, w = map(int, line.strip().split(','))
                edges.append((u, v, w))
        return edges

    def build_graph_from_file(file_path):
        G = nx.MultiGraph()
        edges = load_edges_from_file(file_path)
        G.add_weighted_edges_from(edges)
        return G

    while True:
        print("Mamy następujące opcje: ")
        print("1 -> wczytanie krawędzi grafu z pliku krawedzie1.txt - pozwala przetestować przypadek 1.")
        print("2 -> wczytanie krawędzi grafu z pliku krawedzie2.txt - pozwala przetestować przypadek 2.")
        print("3 -> wczytanie krawędzi grafu z pliku krawedzie3.txt - pozwala przetestować przypadek 3.")
        print("4 -> zakończenie działania programu")
        user_input = input("Wybierz opcję (1, 2, 3, 4): ")

        if user_input == '1':
            file_path = 'krawedzie1.txt'
            G = build_graph_from_file(file_path)
            chinese_postman_problem(G)
        elif user_input == '2':
            file_path = 'krawedzie2.txt'
            G = build_graph_from_file(file_path)
            chinese_postman_problem(G)
        elif user_input == '3':
            file_path = 'krawedzie3.txt'
            G = build_graph_from_file(file_path)
            chinese_postman_problem(G)
        elif user_input == '4':
            print("Koniec działania programu.")
            break
        else:
            print("Niepoprawna opcja. Proszę podać jeszcze raz.")

if __name__=='__main__':
    main()