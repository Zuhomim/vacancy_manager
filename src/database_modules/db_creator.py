import psycopg2
from src.config_database.config import config


class DBCreator:

    def db_connect(self):
        db_params = config()
        return db_params

    def db_create(self, db_name: str, params) -> None:

        conn = psycopg2.connect(dbname='postgres', **params)
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(f"DROP DATABASE IF EXISTS {db_name}")
        cur.execute(f"CREATE DATABASE {db_name}")

        cur.close()
        conn.close()

        conn = psycopg2.connect(dbname='hh_vacancies', **params)

        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS employers (
                    employer_id INT PRIMARY KEY,
                    employer_name VARCHAR(60),
                    url VARCHAR(60)
                )
            """)

        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS vacancies (
                    vacancy_id SERIAL PRIMARY KEY,
                    vacancy_name TEXT,
                    employer_id INT REFERENCES employers(employer_id),
                    salary INT,
                    description TEXT,
                    url VARCHAR(60)
                )
            """)

        conn.commit()
        conn.close()

    def save_data_to_db(self, data_, params):

        conn = psycopg2.connect(dbname='hh_vacancies', **params)
        conn.autocommit = True
        with conn.cursor() as cur:
            for employer in data_["employers"]:
                cur.execute(
                    """
                    INSERT INTO employers (employer_id, employer_name, url)
                    VALUES (%s, %s, %s)
                    """,
                    (int(employer['employer_id']), employer['employer_name'], employer['url'])
                )

        with conn.cursor() as cur:
            for vacancy in data_["vacancies"]:
                cur.execute(
                    """
                    INSERT INTO vacancies (vacancy_name, employer_id, salary, description, url)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (
                        vacancy['name'], (vacancy['employer_id']), (vacancy['salary_from']),
                        vacancy['description'],
                        vacancy['url']
                    )
                )

        conn.commit()
        conn.close()
