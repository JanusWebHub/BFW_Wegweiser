
import os
import matplotlib.pyplot as plt
from collections import deque

nutzer_eingabe = input("Geben Sie bitte den Zielpunkt ein (ost_1, ost_2, nord_1, nord_2, nord_west_1, west_1, west_2, sued_west):__ ")
print(nutzer_eingabe)

print("Aktueller Ordner:")
print(os.getcwd())

print("\nDateien in diesem Ordner:")
print(os.listdir())

karte = plt.imread("E:\TN_Daten\Schmitz\Code_Projekts\Wegweiser_Projekt\Grundriss_mit_Knotenpunkten.png")

plt.imshow(karte)
plt.axis("off")
plt.show()


startpunkt = (675, 400)

knotenpunkte = {
    
    "knoten_1": (680, 318),#nach osten oder knoten_2
    "knoten_2": (556, 314),#nach norden oder westen
    "knoten_3": (624, 185),#nord_1 oder nord_2
    "knoten_4": (327, 349)#nach nord_west,west oder sued_west
}

checkpoints = {
    
    "ost_1": (769, 330),
    "ost_2": (880, 340),
    
    "nord_1": (511, 185),
    "nord_2": (777, 176),

    "nord_west_1": (163, 82),

    "west_1": (165, 349),
    "west_2": (96, 394),

    "sued_west": (255, 485)

}

verbindungen = {
    
    "verbindung1": ["startpunkt", "knoten_1"],

    "verbindung2": ["knoten_1", "ost_1"],
    "verbindung3": ["ost_1", "ost_2"],

    "verbindung4": ["knoten_1", "knoten_2"],
    "verbindung5": ["knoten_2", "knoten_3"],
    "verbindung6": ["knoten_3", "nord_1"],
    "verbindung7": ["knoten_3", "nord_2"],

    "verbindung8": ["knoten_2", "knoten_4"],
    "verbindung9": ["knoten_4", "nord_west_1"],
    "verbindung10": ["knoten_4", "west_1"],
    "verbindung11": ["knoten_4", "sued_west"],

    "verbindung12": ["west_1", "west_2"]

}

# 1. Baue aus verbindungen eine Adjazenzliste
def build_graph(verbindungen):
    graph = {}
    for verbindung in verbindungen.values():
        punkt_a = verbindung[0]
        punkt_b = verbindung[1]
        
        # Beide Richtungen hinzufügen (weil Wege bidirektional sind)
        if punkt_a not in graph:
            graph[punkt_a] = []
        if punkt_b not in graph:
            graph[punkt_b] = []
        
        graph[punkt_a].append(punkt_b)
        graph[punkt_b].append(punkt_a)
        

    
    return graph
    
# 2. Suche den Pfad (BFS = Breitensuche)
def find_path(graph, start, goal):
    from collections import deque
    
    visited = set()
    queue = deque([(start, [start])])
    visited.add(start)
    
    while queue:
        current, path = queue.popleft()
        
        if current == goal:
            return path
        
        for neighbor in graph.get(current, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    
    return None  # Kein Pfad gefunden


# Graph bauen
graph = build_graph(verbindungen)

# Nutzer-Eingabe nehmen
ziel = nutzer_eingabe.strip()

# Pfad finden
weg = find_path(graph, "startpunkt", ziel)

print(f"Pfad: {weg}")

