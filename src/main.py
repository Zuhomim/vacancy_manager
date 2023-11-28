from src.api_modules.head_hunter_api import HeadHunterAPI
from src.config_database.config import config
from src.database_modules.db_creator import DBCreator
from src.database_modules.db_manager import DBManager
from src.utils.json_saver import JSONSaver
from src.utils.utils import get_employers_from_txt

# Интерактив с пользователем (со списком команд)
if __name__ == '__main__':
    params = config()

    hh_api = HeadHunterAPI()
    db_creator = DBCreator()
    db_manager = DBManager()
    json_saver = JSONSaver()

    employers = hh_api.get_employers(get_employers_from_txt('./employers.txt'))

    vacancy_name = input(f'Добрый день, для начала поиска введите название Вакансии: \n')

    vacancies = hh_api.get_vacancies(vacancy_name, 5, get_employers_from_txt('./employers.txt'))

    data = {"employers": employers, "vacancies": vacancies}

    vacancies_count = len(vacancies)

    print(f'Найдено {vacancies_count} вакансий по Вашему запросу\n'
          f'{"-" * 150}')

    while True:

        print(
            f'Доступные команды: \n1 - Записать вакансии в JSON\n2 - Создать базу данных в postgres'
            f'\n3 - Записать данные в базу postgres\n4 - Выйти из программы\n'
            f'4 - Получить список всех компаний и количество вакансий у каждой компании\n'
            f'5 - Получить список всех вакансий с указанием названия компании, '
            f'названия вакансии и зарплаты и ссылки на вакансию\n'
            f'6 - Получить среднюю зарплату по вакансиям\n'
            f'7 - Получить список всех вакансий, у которых зарплата выше средней по всем вакансиям\n'
            f'8 - Получить список всех вакансий, в названии которых содержатся переданные в метод слова')

        command = input('Введите номер команды: \n')

        if command == '0':
            print("-" * 150)
            break
        elif command == '1':
            json_saver.write_json(vacancies)
            print("-" * 150)
            continue
        elif command == '2':
            db_creator.db_create('hh_vacancies', params)
            print("-" * 150)
            continue
        elif command == '3':
            db_creator.save_data_to_db(data, params)
            print("-" * 150)
            continue
        elif command == '4':
            print(db_manager.get_companies_and_vacancies_count())
            print("-" * 150)
            continue
        elif command == '5':
            print(db_manager.get_all_vacancies())
            print("-" * 150)
            continue
        elif command == '6':
            print(db_manager.get_avg_salary())
            print("-" * 150)
            continue
        elif command == '7':
            print(db_manager.get_vacancies_with_higher_salary())
            print("-" * 150)
            continue
        elif command == '8':
            searching_words = input(
                'Для поиска по ключевым словам в названии вакансии введите слова через пробел'
                '(пример: инженер аналитик):\n')
            words = searching_words.split()

            if type(words) == list:
                print(db_manager.get_vacancies_with_keyword(words))
                print("-" * 150)
            else:
                print('Введены некорректные данные')
            continue
