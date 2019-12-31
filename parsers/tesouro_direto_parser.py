from re import findall
import logging
from datetime import datetime
from os import getcwd


class TesouroDiretoParser:
    def __init__(self, html_text_to_parser):
        self._public_title_table_patt = r'<tr class=\"camposTesouroDireto ?\">\s+<td(.*?)>(.*?)</td>\s+<td(.*?)>(' \
                                          r'.*?)</td>\s+<td(.*?)>(.*?)</td>\s+<td(.*?)>(.*?)</td>\s+<td(.*?)>(' \
                                          r'.*?)</td>\s+</tr> '
        self._updated_at_patt = r'Atualizado em: <b>([\d/:\s]+)</b>'
        self._html_text_to_parser = html_text_to_parser
        self._file_path = f'{getcwd()}/static_data/last_update.data'

        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            level=logging.INFO)

    def _convert_to_float(self, brazilian_float_string):
        float_string = brazilian_float_string.replace('.', '')
        float_string = float_string.replace(',', '.')
        float_string = float_string.replace('R$', '')

        return float(float_string)

    def _get_last_update_crawled(self):
        with open(self._file_path,  'r') as f:
            return f.readline()

    def _save_last_update(self, date):
        with open(self._file_path, 'w') as f:
            logging.info(f'Last update: {date}')
            return f.write(date)

    def get_public_title_values(self):
        public_titles = []

        last_update_crawled = self._get_last_update_crawled()
        last_update_website = findall(self._updated_at_patt, self._html_text_to_parser)[0]
        if last_update_crawled == last_update_website:
            return []

        self._save_last_update(last_update_website)

        match = findall(self._public_title_table_patt, self._html_text_to_parser)
        for m in match:
            public_titles.append({
                'name': m[1].strip(),
                'due_date': datetime.strptime(m[3], '%d/%m/%Y'),
                'tax': self._convert_to_float(m[5]),
                'unit_price': self._convert_to_float(m[9])
            })

        return public_titles
