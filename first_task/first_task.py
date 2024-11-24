import json
import numpy as np


matrix = np.load("../data/first_task.npy")

matrix_results = {
    'sum': 0,
    'avr': 0,
    'sumMD': 0,
    'avrMD': 0,
    'sumSD': 0,
    'avrSD': 0,
    'max': matrix[0][0],
    'min': matrix[0][0],
}

for i in range(matrix.shape[0]):
    for j in range(matrix.shape[1]):
        cell = matrix[i][j]
        matrix_results['sum'] += cell
        if cell < matrix_results['min']:
            matrix_results['min'] = cell
        if cell > matrix_results['max']:
            matrix_results['max'] = cell
        if i == j:
            matrix_results['sumMD'] += cell
        if j == matrix.shape[1] - i - 1:
            matrix_results['sumSD'] += cell

matrix_results['avr'] = matrix_results['sum'] / matrix.size
matrix_results['avrMD'] = matrix_results['sumMD'] / matrix.shape[0]
matrix_results['avrSD'] = matrix_results['sumSD'] / matrix.shape[0]

for key in matrix_results.keys():
    matrix_results[key] = float(matrix_results[key])

with open('first_task_result.json', 'w') as f:
    json.dump(matrix_results, f)

normalized_matrix = matrix / matrix_results['sum']
np.save("first_task_result.npy", normalized_matrix)