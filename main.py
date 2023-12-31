from config import config
from utils import *


def main():
    params = config()

    create_database('hh_vacancies', params)
    create_tables('hh_vacancies', params)

    employees_id = [1959252, 581458, 5657254, 3529, 586, 12550, 15478, 5694, 3127, 2324020]

    for employer in employees_id:
        company = get_request(f'https://api.hh.ru/employers/{employer}')
        vacancies = get_request(f'https://api.hh.ru/vacancies?employer_id={employer}&per_page=50')

        save_to_database('hh_vacancies', company, vacancies, params)


if __name__ == '__main__':
    main()
