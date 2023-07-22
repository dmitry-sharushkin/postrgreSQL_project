import psycopg2
from config import config


class DBManager:
    def __init__(self, params=config()):
        self.conn = psycopg2.connect(dbname='hh_vacancies', **params)

    def get_companies_and_vacancies_count(self):
        """Получение списка всех компаний и количества вакансий у каждой компании"""

        cur = self.conn.cursor()
        cur.execute("""
                SELECT companies.name, COUNT(vacancies.id)
                FROM companies JOIN vacancies ON vacancies.company_id = companies.id
                GROUP BY companies.name;
            """)
        return cur.fetchall()

    def get_all_vacancies(self):
        """Получение списка всех вакансий с указанием названия компании, названия вакансии и
    зарплаты и ссылки на вакансию."""
        cur = self.conn.cursor()
        cur.execute("""
                SELECT companies.name, vacancies.name, vacancies.salary_min, vacancies.salary_max, vacancies.url
                FROM vacancies JOIN companies ON vacancies.company_id = companies.id;
            """)
        return cur.fetchall()

    def get_avg_salary(self):
        """Получение средней зарплаты по вакансиям."""

        cur = self.conn.cursor()
        cur.execute("""
                SELECT AVG(vacancies.salary_max)
                FROM vacancies;
            """)
        return cur.fetchone()

    def get_vacancies_with_higher_salary(self):
        """Получение списка всех вакансий, у которых зарплата выше средней по всем вакансиям."""

        cur = self.conn.cursor()
        cur.execute(f"""
                SELECT companies.name, vacancies.name, vacancies.salary_min, vacancies.salary_max, vacancies.url
                FROM vacancies JOIN companies ON vacancies.company_id = companies.id
                WHERE vacancies.salary_max > ({self.get_avg_salary()[0]});
            """)
        return cur.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        """получаем список всех вакансий, в названии которых содержатся переданные в метод слова, например 'python'"""

        cur = self.conn.cursor()
        cur.execute(f"""
                   SELECT *
                   FROM vacancies WHERE vacancies.name LIKE '%{keyword}%';
               """)
        return cur.fetchall()
