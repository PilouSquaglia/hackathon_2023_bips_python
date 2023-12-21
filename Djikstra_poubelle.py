from itertools import permutations
import sys

def calculate_total_weight(graph, path):
    total_weight = 0
    for i in range(len(path) - 1):
        if graph[path[i]][path[i + 1]]['value'] != 0:
            total_weight += graph[path[i]][path[i + 1]]['weight']
    return total_weight

def is_excluded_vertex(graph, vertex):
    # Une poubelle est exclue si toutes ses liaisons ont une valeur de 0
    return all(graph[vertex][i]['value'] == 0 for i in range(len(graph)) if i != vertex)


def travelling_salesman(graph, start_vertex):
    n = len(graph)
    min_path = []
    min_weight = sys.maxsize

    # S'assurer que le sommet de départ est valide
    if start_vertex < 0 or start_vertex >= n or is_excluded_vertex(graph, start_vertex):
        return "Sommet de départ invalide", sys.maxsize

    # Identifier les poubelles à exclure
    excluded_vertices = [i for i in range(n) if is_excluded_vertex(graph, i)]

    # Considérer uniquement les poubelles non exclues pour les permutations, en commençant par le sommet de départ
    valid_vertices = [i for i in range(n) if i not in excluded_vertices and i != start_vertex]
    valid_permutations = [[start_vertex] + list(p) for p in permutations(valid_vertices)]

    for permutation in valid_permutations:
        current_weight = calculate_total_weight(graph, permutation)

        if current_weight < min_weight:
            min_weight = current_weight
            min_path = permutation

    return min_path, min_weight

def format_path(path):
    return [f"poubelle{vertex}" for vertex in path]


graph = [
    # Poubelle 1
    [{'weight': 0, 'value': 1}, {'weight': 2, 'value': 1}, {'weight': 4, 'value': 1}, {'weight': 7, 'value': 1}],

    # Poubelle 2 (ignorée car toutes ses liaisons vers poubelle 4 ont une valeur de 0)
    [{'weight': 2, 'value': 0}, {'weight': 0, 'value': 0}, {'weight': 3, 'value': 0}, {'weight': 6, 'value': 0}],

    # Poubelle 3
    [{'weight': 4, 'value': 1}, {'weight': 3, 'value': 1}, {'weight': 0, 'value': 1}, {'weight': 1, 'value': 1}],

    # Poubelle 4 (aucune liaison valide avec poubelle 2)
    [{'weight': 7, 'value': 1}, {'weight': 6, 'value': 1}, {'weight': 1, 'value': 1}, {'weight': 0, 'value': 1}]
]

path, weight = travelling_salesman(graph , 0)
formatted_path = format_path(path)
print("Chemin:", formatted_path)
print("Poids total:", weight)
