from itertools import permutations
from fastapi import *
import json
import pandas as pd
import numpy as np


app = FastAPI()

file_path = 'data_2023-01-16.json'  # Remplacez par le chemin d'accès à votre fichier

# Chemin vers le fichier de sortie sur votre système
output_file_path = r'C:\Users\nicol\OneDrive\Bureau\Python\python_hackathon\data_triee.json'


try:
    with open(file_path, 'r') as file:
        poubelles_data = json.load(file)
    #print("Contenu du fichier JSON :", poubelles_data)
except Exception as e:
    print(f"Erreur lors de la lecture du fichier JSON : {e}")


def calculate_total_weight(matrix, path):
    total_weight = 0
    for i in range(len(path) - 1):
        total_weight += matrix[path[i]][path[i + 1]]
    return total_weight

def travelling_salesman(matrix, start_vertex, end_vertex):
    n = len(matrix)
    min_path = []
    min_weight = float('inf')

    # Vérifier si les points de départ et d'arrivée sont valides
    if start_vertex < 0 or start_vertex >= n or end_vertex < 0 or end_vertex >= n:
        return "Points de départ ou d'arrivée invalides", min_weight

    # Générer toutes les permutations des sommets, en excluant les points de départ et d'arrivée
    vertices = list(range(n))
    vertices.remove(start_vertex)
    vertices.remove(end_vertex)
    permutations_of_vertices = permutations(vertices)

    for perm in permutations_of_vertices:
        current_path = [start_vertex] + list(perm) + [end_vertex]
        current_weight = calculate_total_weight(matrix, current_path)

        if current_weight < min_weight:
            min_weight = current_weight
            min_path = current_path

    return min_path, min_weight



def create_json_file(path, poubelles_info, output_file):
    formatted_path = []
    for vertex in path:
        if vertex == 0:  # Vérifier si le sommet actuel est le dépôt
            # Ajouter les coordonnées du dépôt
            depot_coords = poubelles_info.get("start")
            formatted_path.append({"latitude": depot_coords[0], "longitude": depot_coords[1]})
        else:
            vertex_info = poubelles_info.get(str(vertex))
            if vertex_info:
                # Ajouter les informations des poubelles
                formatted_path.append({"latitude": vertex_info["Latitude"], "longitude": vertex_info["Longitude"]})
            else:
                # Gérer le cas où les informations de la poubelle ne sont pas trouvées
                formatted_path.append({"latitude": None, "longitude": None})

    # Écrire les données formatées dans un fichier JSON
    with open(output_file, 'w') as file:
        json.dump(formatted_path, file, indent=4)

@app.get("/travelling")
def travelling():
    matrix = [
        [0, 2, 9, 10],
        [1, 0, 6, 4],
        [15, 7, 0, 8],
        [6, 3, 12, 0]
    ]
    start = 0
    path, weight = travelling_salesman(matrix , start)
    create_json_file(path , poubelles_data , output_file_path)
    file_json = {}
    with open('data_triee.json', 'r') as file:
        file_json = json.load(file)
    print(file_json)
    return file_json


try:
    df = pd.read_excel('matrice_mise_a_jour_1.xlsx', engine='openpyxl')
except Exception as e:
    print(f"Erreur lors de la lecture du fichier Excel : {e}")


# Supprimer la première colonne (contenant les coordonnées)
df = df.drop(df.columns[0], axis=1)
# Supprimer la première ligne si elle contient des coordonnées ou des noms de colonnes non désirés
df = df.iloc[1:]
# Convertir le DataFrame en matrice
matrice = df.to_numpy()
# Remplacement des NaN par des 0
matrice_sans_nan = np.nan_to_num(matrice)

print(matrice_sans_nan)

# Exemple d'utilisation
matrix = [
        [0, 2, 9, 10],
        [1, 0, 6, 4],
        [15, 7, 0, 8],
        [6, 3, 12, 0]
    ]
start_vertex = 0  # Remplacez par votre point de départ
n = len(matrix)
end_vertex = n-1  # Remplacez par votre point d'arrivée

"""# Exemple d'utilisation de l'algorithme TSP
path, weight = travelling_salesman(matrice_sans_nan, start_vertex)
# Exemple d'utilisation de l'algorithme TSP (assurez-vous d'avoir les bons paramètres pour 'path' et 'poubelles_data')
create_json_file(path, poubelles_data, output_file_path)
"""
# Exemple d'utilisation de l'algorithme TSP
path, weight = travelling_salesman(matrix, start_vertex , end_vertex)
print(path)