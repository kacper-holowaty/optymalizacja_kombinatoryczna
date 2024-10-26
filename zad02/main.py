import random
import networkx as nx
import matplotlib.pyplot as plt

class Graph:
    def __init__(self, edges):
        self.edges = edges
        self.vertices = set()
        for u, v in self.edges:
            self.vertices.add(u)
            self.vertices.add(v)

    def remove_incident_edges(self, vertex):
        incident_edges = [(u, v) for u, v in self.edges if u == vertex or v == vertex]
        self.edges = [(u, v) for u, v in self.edges if u != vertex and v != vertex]
        return incident_edges

    def draw_graph(self, removed_edges, current_edges, incident_edges, message):
        G = nx.Graph()
        G.add_edges_from(self.edges + removed_edges + current_edges + incident_edges)

        plt.figure(figsize=(8, 6))
        pos = nx.spring_layout(G)

        nx.draw(G, pos, with_labels=True, node_size=700, node_color='lightblue', 
                font_size=10, font_weight='bold', edge_color='gray')

        if removed_edges:
            nx.draw_networkx_edges(G, pos, edgelist=removed_edges, edge_color='red', width=2.5)        

        if incident_edges:
            nx.draw_networkx_edges(G, pos, edgelist=incident_edges, edge_color='green', width=2.5)

        if current_edges:
            nx.draw_networkx_edges(G, pos, edgelist=current_edges, edge_color='blue', width=2.5)

        x_values, y_values = zip(*pos.values())
        text_x = min(x_values) - 0.2
        text_y = max(y_values) + 0.2 

        plt.xlim(min(x_values) - 0.5, max(x_values) + 0.5)
        plt.ylim(min(y_values) - 0.5, max(y_values) + 0.5)

        plt.text(text_x, text_y, message, fontsize=10, bbox=dict(boxstyle="round,pad=0.3", edgecolor="black", facecolor="lightyellow"))
        plt.show()

def approx_vertex_cover(graph):
    print(f"W grafie mamy następujące krawędzie: {graph.edges}")
    vertex_cover = set()
    removed_edges = []
    while graph.edges:
        u, v = random.choice(graph.edges)
        vertex_cover.add(u)
        vertex_cover.add(v)

        incident_edges = graph.remove_incident_edges(u) + graph.remove_incident_edges(v)

        message = (f"Wybrano krawędź: ({u}, {v})\n"
                   f"Pozostałe krawędzie: {graph.edges}\n"
                   f"Obecne pokrycie wierzchołkowe: {vertex_cover}")
        
        current_edges = [(u, v)]
        graph.draw_graph(removed_edges, current_edges, incident_edges, message)

        removed_edges.extend(incident_edges)

    return vertex_cover

filename = "krawedzie.txt"
def read_edges_from_file(filename):
    edges = set()
    with open(filename, 'r') as file:
        for line in file:
            u, v = line.strip().split(',')
            u, v = u.strip(), v.strip()
            if u != v:
                edge = tuple(sorted((u, v)))
                edges.add(edge)
    return list(edges)

edges = read_edges_from_file(filename)
graph = Graph(edges)

vertex_cover = approx_vertex_cover(graph)
print(f"Przybliżone pokrycie wierzchołkowe: {vertex_cover}")