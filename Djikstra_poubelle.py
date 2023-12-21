from itertools import permutations

def calculate_total_weight(matrix, path):
    total_weight = 0
    for i in range(len(path) - 1):
        total_weight += matrix[path[i]][path[i + 1]]
    return total_weight

def travelling_salesman(matrix, start_vertex):
    n = len(matrix)
    min_path = []
    min_weight = float('inf')

    # Vérifier si le point de départ est valide
    if start_vertex < 0 or start_vertex >= n:
        return "Point de départ invalide", min_weight

    # Générer toutes les permutations des sommets, en excluant le point de départ
    vertices = list(range(n))
    vertices.remove(start_vertex)
    permutations_of_vertices = permutations(vertices)

    for perm in permutations_of_vertices:
        current_path = [start_vertex] + list(perm)
        current_weight = calculate_total_weight(matrix, current_path)

        if current_weight < min_weight:
            min_weight = current_weight
            min_path = current_path

    return min_path, min_weight

def format_path(path):
    return ["poubelle" + str(vertex) for vertex in path]

# Exemple d'utilisation
matrix = [
    [0, 2, 9, 10],
    [1, 0, 6, 4],
    [15, 7, 0, 8],
    [6, 3, 12, 0]
]
start_vertex = 0  # Index du point de départ

path, weight = travelling_salesman(matrix, start_vertex)
formatted_path = format_path(path)
print("Chemin:", formatted_path)
print("Poids total:", weight)
