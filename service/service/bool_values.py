import json
import os


def writing_false_value():
    """Записывает значение False в файл поле первого запуска."""
    try:
        file_name = 'is_first_start.json'
        with open(os.path.join(
            'secret/', file_name
        ), 'w') as config_file:
            json.dump({
                "is_first": "False"
            }, config_file)
    except Exception as error:
        print(f'Ошибка при попытке записать данные в файл {file_name}. Проверьте его наличие: ', error)


def read_value():
    """Считывает Булево значение из файла."""
    try:
        file_name = 'is_first_start.json'
        with open(os.path.join(
            'secret/', file_name
        ), 'r') as config_file:
            json_data = json.load(config_file)
    except Exception as error:
        print(f'Ошибка при попытке чтения данных из файла {file_name}. Проверьте его наличие: ', error)

    return json_data.get('is_first')
