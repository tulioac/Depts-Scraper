import scrapy

from .utils.DataExtractor import DataExtractor


class QuotesSpider(scrapy.Spider):
    name = "deputadas"

    def start_requests(self):

        deps_file = open("lista_deputadas.txt", "r")

        deps_urls = deps_file.read().splitlines()

        for url in deps_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        data_extractor = DataExtractor(response)

        name, birth_date = data_extractor.get_basic_data()

        plenary_presences, commissions_presences = data_extractor.get_presence_data()

        trips = data_extractor.trips_data()

        (
            parliamentary_expenses,
            total_parliamentary_expenses,
        ) = data_extractor.get_parliamentary_expenses()

        (
            cabinet_expenses,
            total_cabinet_expenses,
        ) = data_extractor.get_cabinet_expenses()

        salary = data_extractor.get_salary()

        dep_data = {
            "nome": name,
            "genero": "F",
            "data_nascimento": birth_date,
            "presença_plenario": plenary_presences[0] if plenary_presences else None,
            "ausencia_plenario": plenary_presences[1] if plenary_presences else None,
            "ausencia_justificada_plenario": plenary_presences[2]
            if plenary_presences
            else None,
            "presenca_comissao": commissions_presences[0]
            if commissions_presences
            else None,
            "ausencia_comissao": commissions_presences[1]
            if commissions_presences
            else None,
            "ausencia_justificada_comissao": commissions_presences[2]
            if commissions_presences
            else None,
            "quant_viagem": trips,
            "gasto_total_par": total_parliamentary_expenses,
            "gasto_jan_par": parliamentary_expenses.get("jan"),
            "gasto_fev_par": parliamentary_expenses.get("fev"),
            "gasto_mar_par": parliamentary_expenses.get("mar"),
            "gasto_abr_par ": parliamentary_expenses.get("abr"),
            "gasto_mai_par": parliamentary_expenses.get("mai"),
            "gasto_jun_par": parliamentary_expenses.get("jun"),
            "gasto_jul_par": parliamentary_expenses.get("jul"),
            "gasto_ago_par": parliamentary_expenses.get("ago"),
            "gasto_set_par": parliamentary_expenses.get("set"),
            "gasto_out_par": parliamentary_expenses.get("out"),
            "gasto_nov_par": parliamentary_expenses.get("nov"),
            "gasto_dez_par": parliamentary_expenses.get("dez"),
            "gasto_total_gab": total_cabinet_expenses,
            "gasto_jan_gab": cabinet_expenses.get("jan"),
            "gasto_fev_gab": cabinet_expenses.get("fev"),
            "gasto_mar_gab": cabinet_expenses.get("mar"),
            "gasto_abr_gab ": cabinet_expenses.get("abr"),
            "gasto_mai_gab": cabinet_expenses.get("mai"),
            "gasto_jun_gab": cabinet_expenses.get("jun"),
            "gasto_jul_gab": cabinet_expenses.get("jul"),
            "gasto_ago_gab": cabinet_expenses.get("ago"),
            "gasto_set_gab": cabinet_expenses.get("set"),
            "gasto_out_gab": cabinet_expenses.get("out"),
            "gasto_nov_gab": cabinet_expenses.get("nov"),
            "gasto_dez_gab": cabinet_expenses.get("dez"),
            "salario_bruto": salary,
        }

        yield dep_data
