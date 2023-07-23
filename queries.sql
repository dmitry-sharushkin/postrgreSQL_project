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