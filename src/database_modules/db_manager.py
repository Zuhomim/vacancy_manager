from src.config_database.config import config
import psycopg2


class DBManager:
    params_ = config()

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании"""
        conn = psycopg2.connect(dbname='hh_vacancies', **self.params_)
        with conn.cursor() as cur:
            cur.execute("""
                SELECT employer_id, employers.employer_name AS employer_name, COUNT(*) AS vacancy_count FROM vacancies
                JOIN employers USING(employer_id)
                GROUP BY vacancies.employer_id, employers.employer_name
                ORDER BY vacancy_count DESC;
            """)

            data = cur.fetchall()

        conn.commit()
        conn.close()

        return data

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию"""
        conn = psycopg2.connect(dbname='hh_vacancies', **self.params_)
        with conn.cursor() as cur:
            cur.execute("""
                SELECT employers.employer_name, vacancy_name, salary, employers.url FROM vacancies
                JOIN employers USING(employer_id);
            """)

            data = cur.fetchall()

        conn.commit()
        conn.close()

        return data

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям"""
        conn = psycopg2.connect(dbname='hh_vacancies', **self.params_)
        with conn.cursor() as cur:
            cur.execute("""
                SELECT ROUND(AVG(salary)) FROM vacancies
                WHERE salary > 0;
            """)

            data = cur.fetchall()

        conn.commit()
        conn.close()

        return data

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        conn = psycopg2.connect(dbname='hh_vacancies', **self.params_)
        with conn.cursor() as cur:
            cur.execute("""
                SELECT * FROM vacancies
                WHERE salary > (SELECT AVG(salary) FROM vacancies WHERE salary > 0);
            """)

            data = cur.fetchall()

        conn.commit()
        conn.close()

        return data

    def get_vacancies_with_keyword(self, words: list[str]):
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова"""
        conn = psycopg2.connect(dbname='hh_vacancies', **self.params_)
        data = []
        with conn.cursor() as cur:
            for word in words:
                cur.execute(f"""
                    SELECT * FROM vacancies
                    WHERE vacancy_name LIKE '%{word}%';
                """)

                subtotal_data = cur.fetchall()
                data.extend(subtotal_data)

        conn.commit()
        conn.close()

        return data
