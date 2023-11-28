import json


class JSONSaver:
    """Класс записи и получения данных в директории json"""

    @staticmethod
    def write_json(data):
        """Метод записи файла в директорию json"""

        with open(f"../json/vacancies.json", 'w', encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    @staticmethod
    def read_json():
        """Метод получения данных из файла в директории json"""

        with open(f"../../json/vacancies.json", 'rt', encoding="utf-8") as f:
            vacancies = json.load(f)

        return vacancies
