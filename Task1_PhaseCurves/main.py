import json
import sys
from application import Application

SAMPLE_FILENAME = 'sample.json'

if __name__ == "__main__":
    input_file = None
    input_data = None
    try:
        input_file = open(sys.argv[1])
    except IndexError:
        print("Файл с входными данными не задан. Открываю файл по умолчанию.")
        input_file = open(SAMPLE_FILENAME)
    except Exception as e:
        print("При открытии файла с данными произошла ошибка!")
        print(e)
        exit(1)

    try:
        input_data = json.load(input_file)
    except TypeError:
        print("Некорректный формат файла!")

    app = Application(input_data)
    app.start()

