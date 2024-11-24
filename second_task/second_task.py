import os.path
import numpy as np


matrix = np.load("../data/second_task.npy")
x, y, z = [], [], []

for i in range(matrix.shape[0]):
    for j in range(matrix.shape[1]):
        cell = matrix[i][j]
        if cell > 505: #вариант 5
            x.append(i)
            y.append(j)
            z.append(cell)

np.savez("second_task_result", x=x, y=y, z=z)
np.savez_compressed("second_task_result_compressed", x=x, y=y, z=z)

# сжатый файл меньше на ~ 6000 байт
npz_size = os.path.getsize('second_task_result.npz')
npz_compressed_size = os.path.getsize('second_task_result_compressed.npz')
size_comparison = (f'npz size = {npz_size} Bytes\n'
                   f'npz compressed size = {npz_compressed_size} bytes\n'
                   f'diff = {npz_size - npz_compressed_size} bytes\n')

with open('size_comparison.txt', 'w') as f:
    f.write(size_comparison)
print(size_comparison)
