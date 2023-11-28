import requests


class HeadHunterAPI:

    def get_request(self, keyword: str, count_page: int, employers: list, field_name: str) -> list:
        """Метод получения вакансий по API hh.ru"""

        params = {
            "page": 0,
            "per_page": 50,
            "text": keyword.lower(),
            "employer_id": employers
        }
        all_vacancies = []
        vacancies_json = requests.get(f"https://api.hh.ru/{field_name}", params=params).json()

        if "items" in vacancies_json:
            vacancies = vacancies_json["items"]
        else:
            vacancies = vacancies_json

        if count_page > 1:
            for i in range(count_page):
                params["page"] = i
                all_vacancies.extend(vacancies)
        else:
            all_vacancies.append(vacancies)

        return all_vacancies

    def get_vacancies(self, keyword: str, count_page: int, employers: list) -> list:
        """Метод получения списка вакансий для postgreSQL (параметры:
        name, employer_id, description, company_name, salary_from, salary_to, url"""

        all_vacancies = []
        vacancies = self.get_request(keyword.lower(), count_page, employers, "vacancies")
        for vacancy in vacancies:
            if vacancy["salary"]:
                salary_from = vacancy["salary"]["from"] if vacancy["salary"]["from"] else 0
                salary_to = vacancy["salary"]["to"] if vacancy["salary"]["to"] else 0
            else:
                salary_from = 0
                salary_to = 0

            all_vacancies.append({
                "name": vacancy["name"],
                "employer_id": int(vacancy["employer"]["id"]),
                "description": vacancy["snippet"]["responsibility"] if vacancy["snippet"]["responsibility"] else "",
                "company_name": vacancy["employer"]["name"] if vacancy["employer"]["name"] else "",
                "salary_from": int(salary_from),
                "salary_to": int(salary_to),
                "url": str(vacancy["alternate_url"]) if vacancy["alternate_url"] else ""
            })

        return all_vacancies

    def get_employers(self, employer_list: list):
        """Метод получения списка компаний для postgreSQL (с параметрами:
        employer_id, employer_name, url"""

        all_employers = []
        for employer_ in employer_list:
            field_name = f"employers/{employer_}"

            employer = self.get_request("", 1, [], field_name)[0]
            all_employers.append({
                "employer_id": int(employer["id"]),
                "employer_name": str(employer["name"]),
                "url": str(employer["alternate_url"]) if employer["alternate_url"] else employer["url"]

            })

        return all_employers
