from database.manager import DatabaseManager
from network.custom_request import CustomRequest
from parsers.tesouro_direto_parser import TesouroDiretoParser


class TesouroDiretoSpider:
    def __init__(self):
        self._database_manager = DatabaseManager()
        self._dict_public_titles = self._database_manager.get_dict_public_titles_from_database()

        url = 'http://www.tesouro.fazenda.gov.br/tesouro-direto-precos-e-taxas-dos-titulos'
        cr = CustomRequest()
        html = cr.get(url, {})

        self._tesouro_direto_parser = TesouroDiretoParser(html)
        self.tesouros_direto_values = self._tesouro_direto_parser.get_public_title_values()

    def run(self):
        for value in self.tesouros_direto_values:
            if value['name'] not in self._dict_public_titles:
                self._dict_public_titles[value['name']] = self._database_manager.save_public_title(
                    value['name'], value['due_date']
                )

            public_title_id = self._dict_public_titles[value['name']]
            self._database_manager.save_public_title_value(
                public_title_id, value['tax'], value['minimum_value'], value['unit_price']
            )
