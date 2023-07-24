-- Создание базы данных для сохранения данных о вакансиях

DROP DATABASE hh_vacancies
CREATE DATABASE hh_vacancies

-- Cоздание таблиц с информацией о компаниях и вакансиях"""

CREATE TABLE IF NOT EXISTS companies (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                city TEXT NOT NULL,
                description TEXT,
                url TEXT NOT NULL
            )

CREATE TABLE IF NOT EXISTS vacancies (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                company_id INTEGER REFERENCES companies(id),
                salary_min INTEGER,
                salary_max INTEGER,
                url TEXT NOT NULL
            )

-- Сохранение данных о вакансиях в базу данных

INSERT INTO companies (id, name, city, description, url)
                   VALUES (%s, %s, %s, %s, %s)

INSERT INTO vacancies (name, company_id, salary_min, salary_max, url)
                            VALUES (%s, %s, %s, %s, %s)

-- Получение списка всех компаний и количества вакансий у каждой компании

SELECT companies.name, COUNT(vacancies.id)
FROM companies JOIN vacancies ON vacancies.company_id = companies.id
GROUP BY companies.name;

-- Получение списка всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию

SELECT companies.name, vacancies.name, vacancies.salary_min, vacancies.salary_max, vacancies.url
FROM vacancies JOIN companies ON vacancies.company_id = companies.id;

-- Получение средней зарплаты по вакансиям

SELECT AVG(vacancies.salary_max)
FROM vacancies;

-- Получение списка всех вакансий, у которых зарплата выше средней по всем вакансиям

SELECT companies.name, vacancies.name, vacancies.salary_min, vacancies.salary_max, vacancies.url
FROM vacancies JOIN companies ON vacancies.company_id = companies.id
WHERE vacancies.salary_max > ({self.get_avg_salary()[0]});

-- Получение списка всех вакансий, в названии которых содержатся переданные в метод слова, например 'python'

SELECT *
FROM vacancies WHERE vacancies.name LIKE '%{keyword}%'
