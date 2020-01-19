from psycopg2 import connect
from os import getenv


class DatabaseManager:

    def __init__(self):
        self._con = connect(
            host=getenv('POSTGRES_HOST', '127.0.1.0'), database='tesouro_direto',
            user=getenv('POSTGRES_USER', 'backer-medieval'),
            port=getenv('POSTGRES_PORT', '5432'),
            password=getenv('POSTGRES_PASSWORD', None)
        )
        self._cur = self._con.cursor()

    def __del__(self):
        self._cur.close()
        self._con.commit()
        self._con.close()

    def _get_data(self, query: str) -> list:
        self._cur.execute(query)
        return self._cur.fetchall()

    def get_dict_public_titles_from_database(self) -> dict:
        query = 'SELECT id, name FROM public_titles;'
        data = self._get_data(query)

        names_to_ids = {}
        for d in data:
            company_id, company_name = d
            names_to_ids[company_name] = company_id

        return names_to_ids

    def save_public_title(self, name, due_date) -> int:
        query = '''
            INSERT INTO public_titles(name, due_date)
            VALUES(%s, %s) RETURNING id;
        '''
        self._cur.execute(query, (name, due_date))
        self._con.commit()
        return self._cur.fetchone()[0]

    def save_public_title_value(self, public_title_id, tax, unit_price) -> int:
        query = '''
            INSERT INTO public_title_values(public_title_id, tax, unit_price)
            VALUES(%s, %s, %s) RETURNING id;
        '''
        self._cur.execute(query, (public_title_id, tax, unit_price))
        self._con.commit()
