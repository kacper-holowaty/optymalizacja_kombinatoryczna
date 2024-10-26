import networkx as nx
import matplotlib.pyplot as plt
import sys
import itertools as it

class Graf:
    def __init__(self):
        self.macierz_sasiedztwa = []
        self.wierzcholki = {}

    def dodaj_wierzcholek(self, etykieta):
        try:
            etykieta = int(etykieta)
            if etykieta in self.wierzcholki:
                print(f"Wierzchołek {etykieta} już istnieje.")
                return

            self.macierz_sasiedztwa.append([0] * (len(self.macierz_sasiedztwa) + 1))
            for wiersz in self.macierz_sasiedztwa[:-1]:
                wiersz.append(0)

            self.wierzcholki[etykieta] = len(self.macierz_sasiedztwa) - 1
            print(f"Dodano wierzchołek {etykieta}")

        except ValueError:
            print(f"Niepoprawny wierzchołek: {etykieta}. Musi być on liczbą całkowitą.")
            return

    def usun_wierzcholek(self, etykieta):
        try:
            etykieta = int(etykieta)
            if etykieta not in self.wierzcholki:
                print(f"Wierzchołek {etykieta} nie istnieje.")
                return

            index = self.wierzcholki[etykieta]
            self.macierz_sasiedztwa.pop(index)
            for wiersz in self.macierz_sasiedztwa:
                wiersz.pop(index)
            del self.wierzcholki[etykieta]

            nowe_wierzcholki = {}
            for i, klucz in enumerate(self.wierzcholki):
                nowe_wierzcholki[klucz] = i
            self.wierzcholki = nowe_wierzcholki
            print(f"Usunięto wierzchołek {etykieta}")

        except ValueError:
            print(f"Niepoprawny wierzchołek: {etykieta}. Musi być on liczbą całkowitą.")
            return

    def wyswietl_macierz(self):
        naglowki = ' '.join(map(str, self.wierzcholki.keys()))
        print(f"   {naglowki}")

        for etykieta in self.wierzcholki.keys():
            index = self.wierzcholki[etykieta]
            wiersz = ' '.join(str(self.macierz_sasiedztwa[index][i]) for i in range(len(self.macierz_sasiedztwa)))
            print(f"{etykieta} [{wiersz}]")


class GrafNieskierowany(Graf):
    def __init__(self):
        self.macierz_sasiedztwa = []
        self.wierzcholki = {}

    def dodaj_krawedz(self, u, v):
        try:
            u = int(u)
            v = int(v)
            if u not in self.wierzcholki or v not in self.wierzcholki:
                print(f"Nie można dodać krawędzi: jeden z wierzchołków nie istnieje.")
                return
            
            if u == v:
                print("Nie można dodać pętli do grafu!")
                return

            index_u = self.wierzcholki[u]
            index_v = self.wierzcholki[v]
            self.macierz_sasiedztwa[index_u][index_v] += 1
            self.macierz_sasiedztwa[index_v][index_u] += 1
            print(f"Dodano krawędź do grafu nieskierowanego między {u} a {v}.")
            self.wyswietl_macierz()
        except ValueError:
            print(f"Niepoprawne wierzchołki: {u}, {v}")
            return   

    def usun_krawedz(self, u, v):
        try:
            u = int(u)
            v = int(v)
            if u not in self.wierzcholki or v not in self.wierzcholki:
                print(f"Nie można usunąć krawędzi: jeden z wierzchołków nie istnieje.")
                return

            index_u = self.wierzcholki[u]
            index_v = self.wierzcholki[v]

            if self.macierz_sasiedztwa[index_u][index_v] == 0 and self.macierz_sasiedztwa[index_v][index_u] == 0:
                print(f"Krawędź między {u} a {v} nie istnieje.")
                return
    
            if self.macierz_sasiedztwa[index_u][index_v] < 2 and self.macierz_sasiedztwa[index_v][index_u] < 2:
                self.macierz_sasiedztwa[index_u][index_v] = 0
                self.macierz_sasiedztwa[index_v][index_u] = 0
            else: 
                self.macierz_sasiedztwa[index_u][index_v] -= 1
                self.macierz_sasiedztwa[index_v][index_u] -= 1
            print(f"Usunięto krawędź grafu nieskierowanego między {u} a {v}.")
            self.wyswietl_macierz()
        except ValueError:
            print(f"Niepoprawne wierzchołki: {u}, {v}")
            return

    def stopien_wierzcholka(self, etykieta):
        try:
            etykieta = int(etykieta)
            if etykieta not in self.wierzcholki:
                print(f"Wierzchołek {etykieta} nie istnieje.")
                return 

            index = self.wierzcholki[etykieta]
            stopien = sum(self.macierz_sasiedztwa[index])
            return stopien 
        except ValueError:
            print(f"Niepoprawny wierzchołek: {etykieta}")
            return

    def min_max_stopien(self):
        if not self.wierzcholki:
            print("Graf jest pusty.")
            return None, None
    
        stopnie = [sum(self.macierz_sasiedztwa[i]) for i in range(len(self.macierz_sasiedztwa))]
        min_stopien = min(stopnie)
        max_stopien = max(stopnie)
        return min_stopien, max_stopien

    def parzysty_nieparzysty_stopien(self):
        liczba_parzystych = 0
        liczba_nieparzystych = 0
        for etykieta in self.wierzcholki.keys():
            stopien = self.stopien_wierzcholka(etykieta)
            if stopien % 2 == 0:
                liczba_parzystych += 1
            else:
                liczba_nieparzystych += 1

        return liczba_parzystych, liczba_nieparzystych
    
    def posortowane_stopnie(self):
        stopnie = []
        for etykieta in self.wierzcholki.keys():
            stopien = self.stopien_wierzcholka(etykieta)
            stopnie.append(stopien)

        stopnie.sort(reverse=True)
        return stopnie


    def narysuj_graf(self):
        G = nx.MultiGraph()

        for etykieta in self.wierzcholki.keys():
            G.add_node(etykieta)

        for i in range(len(self.macierz_sasiedztwa)):
            for j in range(len(self.macierz_sasiedztwa)):
                for _ in range(self.macierz_sasiedztwa[i][j]):
                    if self.macierz_sasiedztwa[i][j] > 0:
                        G.add_edge(list(self.wierzcholki.keys())[i], list(self.wierzcholki.keys())[j])

        pos = nx.spring_layout(G)
        edge_labels = {(u, v): int(G.number_of_edges(u, v)/2) for u, v in G.edges()}

        nx.draw(G, pos, with_labels=True, arrows=False, node_color='skyblue', node_size=700, font_size=20, font_color='black', edge_color='gray')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
        plt.show()


class GrafSkierowany(Graf):
    def __init__(self):
        self.macierz_sasiedztwa = []
        self.wierzcholki = {}
    
    def dodaj_krawedz(self, u, v):
        try:
            u = int(u)
            v = int(v)
            if u not in self.wierzcholki or v not in self.wierzcholki:
                print(f"Nie można dodać krawędzi: jeden z wierzchołków nie istnieje.")
                return
            
            if u == v:
                print("Nie można dodać pętli do grafu!")
                return

            index_u = self.wierzcholki[u]
            index_v = self.wierzcholki[v]
            self.macierz_sasiedztwa[index_u][index_v] += 1
            print(f"Dodano krawędź do grafu skierowanego od {u} do {v}.")
            self.wyswietl_macierz()
        except ValueError:
            print(f"Niepoprawne wierzchołki: {u}, {v}")
            return

    def usun_krawedz(self, u, v):
        try:
            u = int(u)
            v = int(v)
            if u not in self.wierzcholki or v not in self.wierzcholki:
                print(f"Nie można usunąć krawędzi: jeden z wierzchołków nie istnieje.")
                return

            index_u = self.wierzcholki[u]
            index_v = self.wierzcholki[v]

            if self.macierz_sasiedztwa[index_u][index_v] == 0:
                print(f"Krawędź od {u} do {v} nie istnieje.")
                return
    
            if self.macierz_sasiedztwa[index_u][index_v] < 2:
                self.macierz_sasiedztwa[index_u][index_v] = 0
            else:
                self.macierz_sasiedztwa[index_u][index_v] -= 1
            print(f"Usunięto krawędź grafu skierowanego od {u} do {v}.")
            self.wyswietl_macierz()
        except ValueError:
            print(f"Niepoprawne wierzchołki: {u}, {v}")
            return

    def stopien_wierzcholka(self, etykieta):
        try:
            etykieta = int(etykieta)
            if etykieta not in self.wierzcholki:
                print(f"Wierzchołek {etykieta} nie istnieje.")
                return None, None

            index = self.wierzcholki[etykieta]
            stopien_wychodzacy = sum(self.macierz_sasiedztwa[index])
            stopien_wchodzacy = sum(self.macierz_sasiedztwa[i][index] for i in range(len(self.macierz_sasiedztwa)))
            return stopien_wchodzacy, stopien_wychodzacy
        
        except ValueError:
            print(f"Niepoprawny wierzchołek: {etykieta}")
            return None, None
    
    def narysuj_graf(self):
        G = nx.MultiDiGraph()

        for etykieta in self.wierzcholki.keys():
            G.add_node(etykieta)

        for i in range(len(self.macierz_sasiedztwa)):
            for j in range(len(self.macierz_sasiedztwa)):
                liczba_krawedzi = self.macierz_sasiedztwa[i][j]
                if liczba_krawedzi > 0:
                    for _ in range(liczba_krawedzi):
                        G.add_edge(list(self.wierzcholki.keys())[i], list(self.wierzcholki.keys())[j])

        pos = nx.spring_layout(G)

        connectionstyle = [f"arc3,rad={r}" for r in it.accumulate([0.15] * 4)]
        nx.draw(G, pos, with_labels=True, connectionstyle=connectionstyle, node_color='skyblue', node_size=700, font_size=20, font_color='black', edge_color='gray', arrows=True, arrowstyle='->', arrowsize=20)
        plt.show()
        
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
                print("7. wyświetlenie macierzy sąsiedztwa")
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
                    wchodzacy, wychodzacy = graf_skierowany.stopien_wierzcholka(v)
                    print(f"Stopień wchodzący: {wchodzacy}, stopień wychodzący: {wychodzacy}")
                elif opcja == '6':
                    graf_skierowany.narysuj_graf()
                elif opcja == '7':
                    graf_skierowany.wyswietl_macierz()
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
                print("10. wyświetlenie macierzy sąsiedztwa")
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
                    print()
                    min_stopien, max_stopien = graf_nieskierowany.min_max_stopien()
                    print(f"Stopień minimalny: {min_stopien}, stopień maksymalny: {max_stopien}")
                elif opcja == '7':
                    print()
                    parzyste, nieparzyste = graf_nieskierowany.parzysty_nieparzysty_stopien()
                    print(f"Liczba wierzchołków stopnia parzystego: {parzyste}")
                    print(f"Liczba wierzchołków stopnia nieparzystego: {nieparzyste}")
                elif opcja == '8':
                    print()
                    posortowane = graf_nieskierowany.posortowane_stopnie()
                    print(f"Posortowane stopnie wierzchołków: {posortowane}")
                elif opcja == '9':
                    graf_nieskierowany.narysuj_graf()
                elif opcja == '10':
                    graf_nieskierowany.wyswietl_macierz()
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
