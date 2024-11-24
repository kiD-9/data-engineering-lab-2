import csv
import json
import msgpack
import pickle
import math
import os.path


def remove_unnecessary_columns_and_cast(data):
    columns_to_remove = ['age', 'waistline', 'sight_left', 'sight_right', 'BLDS', 'tot_chole', 'HDL_chole', 'LDL_chole',
                         'triglyceride', 'hemoglobin', 'urine_protein', 'serum_creatinine', 'SGOT_AST', 'SGOT_ALT',
                         'gamma_GTP']
    columns_to_cast = ['height', 'weight', 'hear_left', 'hear_right', 'SBP', 'DBP', 'SMK_stat_type_cd']
    for row in data:
        for column in columns_to_remove:
            row.pop(column)
        for column in columns_to_cast:
            row[column] = float(row[column])


def find_all_parameters(data):
    # sex, height, weight, hear_left, hear_right, SBP, DBP, SMK_stat_type_cd, DRK_YN
    maximums, minimums, sums, averages, standard_deviations = {}, {}, {}, {}, {}
    columns_to_calculate = ['height', 'weight', 'SBP', 'DBP']
    for column in columns_to_calculate:
        maximums[column] = data[0][column]
        minimums[column] = data[0][column]
        sums[column] = 0
        averages[column] = 0
        standard_deviations[column] = 0

    frequencies = {'males': 0, 'hear_left_normal': 0, 'hear_right_normal': 0, 'never_smoked': 0,
                'used_to_smoke_but_quit': 0, 'still_smoke': 0, 'drinks_alcohol': 0}

    for row in data:
        for key, value in row.items():
            if key in columns_to_calculate:
                sums[key] += value
                if value > maximums[key]:
                    maximums[key] = value
                if value < minimums[key]:
                    minimums[key] = value
            elif key == 'sex':
                frequencies['males'] += value == 'Male'
            elif key == 'hear_left':
                frequencies['hear_left_normal'] += value == 1
            elif key == 'hear_right':
                frequencies['hear_right_normal'] += value == 1
            elif key == 'SMK_stat_type_cd':
                if value == 1:
                    frequencies['never_smoked'] += 1
                elif value == 2:
                    frequencies['used_to_smoke_but_quit'] += 1
                elif value == 3:
                    frequencies['still_smoke'] += 1
            elif key == 'DRK_YN':
                frequencies['drinks_alcohol'] += value == 'Y'

    for column in columns_to_calculate:
        averages[column] = sums[column] / len(data)
        sum_pow = 0
        for row in data:
            sum_pow += ((row[column] - averages[column]) ** 2)

        standard_deviations[column] = round(math.sqrt(sum_pow / len(data)), 4)
        averages[column] = round(averages[column], 4)

    for k, v in frequencies.items():
        frequencies[k] = round(v / len(data), 4)

    return {'maximums': maximums, 'minimums': minimums, 'averages': averages, 'sums': sums,
            'standard_deviations': standard_deviations, 'frequencies': frequencies}


def read_csv():
    extracted_csv = []
    with open("../data/fifth_task.csv", newline='', encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter=',', quotechar='"')
        for row in reader:
            extracted_csv.append(row)

    return extracted_csv


def write_parameters_to_json(parameters):
    with open("fifth_task_parameters.json", "w", encoding="utf-8") as file:
        json.dump(parameters, file)


def write_data_to_all_types(data):
    with open("fifth_task_result.csv", "w", encoding="utf-8", newline='') as file:
        writer = csv.DictWriter(file, delimiter=',', quotechar='"', fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    with open("fifth_task_result.json", "w", encoding="utf-8", newline='') as file:
        json.dump(data, file)
    with open("fifth_task_result.msgpack", "wb") as file:
        packed = msgpack.packb(data)
        file.write(packed)
    with open('fifth_task_result.pkl', 'wb') as file:
        pickle.dump(data, file)


def calculate_and_output_size_comparison():
    csv_size = round(os.path.getsize('fifth_task_result.csv') / 1024 / 1024, 3)
    json_size = round(os.path.getsize('fifth_task_result.json') / 1024 / 1024, 3)
    msgpack_size = round(os.path.getsize('fifth_task_result.msgpack') / 1024 / 1024, 3)
    pkl_size = round(os.path.getsize('fifth_task_result.pkl') / 1024 / 1024, 3)
    size_comparison = (f'csv size = {csv_size} MiB\n'
                       f'json size = {json_size} MiB\n'
                       f'msgpack size = {msgpack_size} MiB\n'
                       f'pkl size = {pkl_size} MiB\n\n'
                       f'CSV is the smallest, JSON is the biggest. Their diff is {json_size - csv_size} MiB')

    with open('size_comparison.txt', 'w') as f:
        f.write(size_comparison)
    print(size_comparison)

# dataset - https://www.kaggle.com/datasets/sooyoungher/smoking-drinking-dataset/data
# взято 300 тыс. строк из ~ 1 млн. строк в датасете (~ 32 Мбайта)
data = read_csv()
remove_unnecessary_columns_and_cast(data)
parameters = find_all_parameters(data)
write_parameters_to_json(parameters)
write_data_to_all_types(data)
calculate_and_output_size_comparison()
