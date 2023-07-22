import requests
import psycopg2


def create_database(database_name: str, params: dict) -> None:
    """Создание базы данных для сохранения данных о вакансиях"""

    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f'DROP DATABASE {database_name}')
    cur.execute(f'CREATE DATABASE {database_name}')

    cur.close()
    conn.close()


def create_tables(database_name: str, params: dict) -> None:
    """Cоздание таблиц с информацией о компаниях и вакансиях"""

    conn = psycopg2.connect(dbname=database_name, **params)
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS companies (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                city TEXT NOT NULL,
                description TEXT,
                url TEXT NOT NULL
            )
        """)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS vacancies (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                company_id INTEGER REFERENCES companies(id),
                salary_min INTEGER,
                salary_max INTEGER,
                url TEXT NOT NULL
            )                
        """)

    conn.commit()
    conn.close()


def save_to_database(database_name, company, vacancies, params) -> None:
    """Сохранение данных о вакансиях в базу данных"""

    conn = psycopg2.connect(dbname=database_name, **params)
    with conn.cursor() as cur:
        cur.execute("""
                   INSERT INTO companies (id, name, city, description, url)
                   VALUES (%s, %s, %s, %s, %s)
                   """,
                    (int(company['id']), company['name'], company['area']['name'],
                     company['description'].replace('<strong>', '').replace('</strong>', '').replace('<p>', '').replace(
                         '</p>', ''),
                     company['alternate_url'])
                    )

        for item in vacancies['items']:
            from_ = None
            to_ = None
            if item['salary']:
                from_ = item['salary']['from']
                to_ = item['salary']['to']
            cur.execute(f"""
                            INSERT INTO vacancies (name, company_id, salary_min, salary_max, url)
                            VALUES (%s, %s, %s, %s, %s)""",
                        (item['name'], item['employer']['id'], from_, to_, item['alternate_url'])
                        )

    conn.commit()
    conn.close()


def get_request(url):
    """Получение данных с API HH"""
    data = requests.get(url)
    return data.json()
