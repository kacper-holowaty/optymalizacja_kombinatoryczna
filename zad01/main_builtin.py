import networkx as nx
import matplotlib.pyplot as plt
import sys
import numpy as np
import itertools as it

class Graf:
    def __init__(self):
        self.graph = None 

    def dodaj_wierzcholek(self, v):
        try:
            v = int(v)
            if not self.graph.has_node(v):
                self.graph.add_node(v)
            else:
                print(f"Wierzchołek {v} już istnieje.")
                return
        except ValueError:
            print(f"Niepoprawny wierzchołek: {v}")
            return
    
    def usun_wierzcholek(self, v):
        try:
            v = int(v)
            if not self.graph.has_node(v):
                print(f"Wierzchołek {v} nie istnieje")
                return
            self.graph.remove_node(v)
        except ValueError:
            print(f"Nie poprawny wierzchołek: {v}")
            return
        
    def dodaj_krawedz(self, u, v):
        try:
            u = int(u)
            v = int(v)
            if not self.graph.has_node(u) or not self.graph.has_node(v):
                print(f"Któryś z wierzchołków nie istnieje.")
                return
            self.graph.add_edge(u, v)
        except ValueError:
            print(f"Niepoprawne wierzchołki: {u}, {v}")
            return

    def usun_krawedz(self, u, v):
        try:
            u = int(u)
            v = int(v)
            if not self.graph.has_edge(u, v):
                print(f"Podana krawędź nie istnieje.")
                return
            self.graph.remove_edge(u, v)
        except ValueError:
            print(f"Nie poprawne wierzchołki: {u}, {v}")
            return   


class GrafNieskierowany(Graf):
    def __init__(self):
        self.graph = nx.MultiGraph()

    def stopien_wierzcholka(self, v):
        try:
            v = int(v)
            if self.graph.has_node(v):
                return self.graph.degree(v)
            else:
                print(f"Wierzchołek {v} nie istnieje.")
                return None 
            
        except ValueError:
            print(f"Nie poprawny wierzchołek: {v}")
            return

    def min_max_stopien(self):
        if len(self.graph) == 0:
            print("Graf jest pusty.")
            return None, None
    
        stopnie = [self.graph.degree(v) for v in self.graph.nodes()]
        min_stopien = min(stopnie)
        max_stopien = max(stopnie)
        return min_stopien, max_stopien

    def parzysty_nieparzysty_stopien(self):
        if len(self.graph) == 0:
            print("Graf jest pusty")
            return None

        stopnie = [s for _, s in self.graph.degree()]
        parzyste = sum(1 for s in stopnie if s % 2 == 0)
        nieparzyste = sum(1 for s in stopnie if s % 2 == 1)
        return parzyste, nieparzyste
    
    def posortowane_stopnie(self):
        if len(self.graph) == 0:
            print("Graf jest pusty.")
            return None

        stopnie = [s for _, s in self.graph.degree()]
        return sorted(stopnie, key=lambda x: x, reverse=True)

    def narysuj_graf(self):
        pos = nx.spring_layout(self.graph)
        edge_labels = {(u, v): len(self.graph[u][v]) for u, v in self.graph.edges()}
    
        nx.draw(self.graph, pos, with_labels=True, arrows=False, node_color='skyblue', node_size=700, font_size=20, font_color='black', edge_color='gray')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels)
        plt.show()
        

    def macierz_sasiedztwa(self):
        liczba_wierzcholkow = len(self.graph.nodes())
        macierz = np.zeros((liczba_wierzcholkow, liczba_wierzcholkow), dtype=int)

        for krawedz in self.graph.edges(data=True):
            i = krawedz[0]
            j = krawedz[1]
            macierz[i][j] += 1
            macierz[j][i] += 1

        return macierz


class GrafSkierowany(Graf):
    def __init__(self):
        self.graph = nx.MultiDiGraph()
    
    def stopnie_wierzcholkow_graf_skierowany(self,v):
        try:
            v = int(v)
            if not self.graph.has_node(v):
                print(f"Wierzchołek {v} nie istnieje")
                return None, None

            return self.graph.in_degree(v), self.graph.out_degree(v)
            
        except ValueError:
            print(f"Nie poprawny wierzchołek: {v}")
            return None, None
    
    def narysuj_graf(self):
        pos = nx.spring_layout(self.graph)
        connectionstyle = [f"arc3,rad={r}" for r in it.accumulate([0.15] * 4)]
        nx.draw(self.graph, pos, with_labels=True, connectionstyle=connectionstyle, node_color='skyblue', node_size=700, font_size=20, font_color='black', edge_color='gray', arrows=True, arrowstyle='->', arrowsize=20)
        plt.show()

    def macierz_sasiedztwa(self):
        liczba_wierzcholkow = len(self.graph.nodes())
        macierz = np.zeros((liczba_wierzcholkow, liczba_wierzcholkow), dtype=int)

        for krawedz in self.graph.edges(data=True):
            i = krawedz[0]
            j = krawedz[1]        
            macierz[i][j] += 1
    
        return macierz


def main():
    file_name = "krawedzie.txt"
    if len(sys.argv) > 1:
        if sys.argv[1] == "-s":
            graf_skierowany = GrafSkierowany()
            try:
                with open(file_name, 'r') as file:
                    for line in file:
                        current = line.strip().split(', ')
                        i = int(current[0])
                        j = int(current[1])
                        graf_skierowany.dodaj_wierzcholek(i)
                        graf_skierowany.dodaj_wierzcholek(j)
                        graf_skierowany.dodaj_krawedz(i, j)
            except FileNotFoundError:
                print(f"Plik '{file_name}' nie istnieje. Utworzono nowy, pusty graf.")

            while True:
                print()
                print("1. dodaj krawędź")
                print("2. usuń krawędź")
                print("3. dodaj wierzchołek")
                print("4. usuń wierzchołek")
                print("5. stopień wierzchołka (stopień wchodzący i wychodzący)")
                print("6. narysowanie grafu")
                print("7. wypisz macierz sąsiedztwa")
                print("8. zakończ program")
                opcja = input("Wybierz opcję: ")
                if (opcja == '1'):
                    u = input("Podaj pierwszy wierzchołek: ")
                    v = input("Podaj drugi wierzchołek: ")
                    graf_skierowany.dodaj_krawedz(u, v)
                elif opcja == '2':
                    u = input("Podaj pierwszy wierzchołek: ")
                    v = input("Podaj drugi wierzchołek: ")
                    graf_skierowany.usun_krawedz(u, v)
                elif opcja == '3':
                    v = input("Podaj wierzchołek: ")
                    graf_skierowany.dodaj_wierzcholek(v)
                elif opcja == '4':
                    v = input("Podaj wierzchołek: ")
                    graf_skierowany.usun_wierzcholek(v)
                elif opcja == '5':
                    v = input("Podaj wierzchołek: ")
                    wchodzacy, wychodzacy = graf_skierowany.stopnie_wierzcholkow_graf_skierowany(v)
                    print(f"Stopień wchodzący: {wchodzacy}, stopień wychodzący: {wychodzacy}")
                elif opcja == '6':
                    graf_skierowany.narysuj_graf()
                elif opcja == '7':
                    macierz = graf_skierowany.macierz_sasiedztwa()
                    print("Macierz sąsiedztwa:")
                    for row in macierz:
                        print(row)
                elif opcja == '8':
                    break    
                else:
                    print("Nieprawidłowa opcja!")
            
        elif sys.argv[1] == "-n":
            graf_nieskierowany = GrafNieskierowany()
            try:
                with open(file_name, 'r') as file:
                    for line in file:
                        current = line.strip().split(', ')
                        i = int(current[0])
                        j = int(current[1])
                        graf_nieskierowany.dodaj_wierzcholek(i)
                        graf_nieskierowany.dodaj_wierzcholek(j)
                        graf_nieskierowany.dodaj_krawedz(i, j)
            except FileNotFoundError:
                print(f"Plik '{file_name}' nie istnieje. Utworzono nowy, pusty graf.")

            while True:
                print()
                print("1. dodaj krawędź")
                print("2. usuń krawędź")
                print("3. dodaj wierzchołek")
                print("4. usuń wierzchołek")
                print("5. stopień wierzchołka")
                print("6. minimalny i maksymalny stopień grafu")
                print("7. liczba wierzchołków stopnia parzystego i nieparzystego")
                print("8. posortowane stopnie wierzchołków")
                print("9. narysowanie grafu")
                print("10. wypisz macierz sąsiedztwa")
                print("11. zakończ program")
                opcja = input("Wybierz opcję: ")
                if (opcja == '1'):
                    u = input("Podaj pierwszy wierzchołek: ")
                    v = input("Podaj drugi wierzchołek: ")
                    graf_nieskierowany.dodaj_krawedz(u, v)
                elif opcja == '2':
                    u = input("Podaj pierwszy wierzchołek: ")
                    v = input("Podaj drugi wierzchołek: ")
                    graf_nieskierowany.usun_krawedz(u, v)
                elif opcja == '3':
                    v = input("Podaj wierzchołek: ")
                    graf_nieskierowany.dodaj_wierzcholek(v)
                elif opcja == '4':
                    v = input("Podaj wierzchołek: ")
                    graf_nieskierowany.usun_wierzcholek(v)
                elif opcja == '5':
                    v = input("Podaj wierzchołek: ")
                    stopien = graf_nieskierowany.stopien_wierzcholka(v)
                    print(f"Stopień wierzchołka: {stopien}")
                elif opcja == '6':
                    min_stopien, max_stopien = graf_nieskierowany.min_max_stopien()
                    print(f"Stopień minimalny: {min_stopien}, stopień maksymalny: {max_stopien}")
                elif opcja == '7':
                    parzyste, nieparzyste = graf_nieskierowany.parzysty_nieparzysty_stopien()
                    print(f"Liczba wierzchołków stopnia parzystego: {parzyste}")
                    print(f"Liczba wierzchołków stopnia nieparzystego: {nieparzyste}")
                elif opcja == '8':
                    posortowane = graf_nieskierowany.posortowane_stopnie()
                    print(f"Posortowane stopnie wierzchołków: {posortowane}")
                elif opcja == '9':
                    graf_nieskierowany.narysuj_graf()
                elif opcja == '10':
                    macierz = graf_nieskierowany.macierz_sasiedztwa()
                    print("Macierz sąsiedztwa:")
                    for row in macierz:
                        print(row)
                elif opcja == '11':
                    break    
                else:
                    print("Nieprawidłowa opcja!")
        else:
            print("Niepoprawny argument. Użyj -s dla grafu skierowanego lub -n dla grafu nieskierowanego.")
    else:
        print("Podaj argument: -s (graf skierowany) lub -n (graf nieskierowany).")

if __name__ == "__main__":
    main()
