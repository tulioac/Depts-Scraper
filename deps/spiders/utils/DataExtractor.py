class DataExtractor:
    def __init__(self, response):
        self.response = response

    def __extract_presence_info(self, xpath_id):
        try:
            presences = []

            for i in range(1, 4):
                presence_xpath = f'//*[@id="atuacao-section"]/div[2]/ul[2]/li[{xpath_id}]/dl/dd[{i}]/text()'

                presence_days = int(
                    self.response.xpath(presence_xpath).get().strip().split(" ")[0]
                )

                presences.append(presence_days)

            return presences
        except:
            return None

    def __get_presence_data(
        self,
    ):
        plenary_xpath_id, commission_xpath_id = [1, 2]

        plenary_presences = self.__extract_presence_info(plenary_xpath_id)
        commissions_presences = self.__extract_presence_info(commission_xpath_id)

        return plenary_presences, commissions_presences

    def __extract_basic_info(self, xpath_id):
        info_xpath = f'//*[@id="identificacao"]/div/div/div[3]/div/div/div[2]/div[1]/ul/li[{xpath_id}]/text()'

        info = self.response.xpath(info_xpath).get().strip()

        return info

    def __get_basic_data(self):

        name_xpath_id, birth_date_xpath_id = [1, 5]

        name = self.__extract_basic_info(name_xpath_id)
        birth_date = self.__extract_basic_info(birth_date_xpath_id)

        return name, birth_date

    def __trips_data(self):
        xpath = '//*[@id="recursos-section"]/ul/li[5]/div/a/text()'

        trips_element = self.response.xpath(xpath).get()

        trips = 0

        if trips_element:
            trips = int(trips_element)

        return trips

    def __expenses_accumulator(self, table_css_selector):
        total_expenses = 0
        expenses_dict = {}

        table_element = self.response.css(table_css_selector)

        rows = table_element.css("tbody > tr")

        for row in rows:
            monthElement, expenseElement, _ = row.css("td")
            month = str(monthElement.css("::text").get()).lower()
            expense = float(
                expenseElement.css("::text").get().replace(".", "").replace(",", ".")
            )

            expenses_dict[month] = expense
            total_expenses += expense

        return expenses_dict, total_expenses

    def __get_parliamentary_expenses(self):
        expenses_dict, total_expenses = self.__expenses_accumulator(
            "table#gastomensalcotaparlamentar"
        )

        return expenses_dict, total_expenses

    def __get_cabinet_expenses(self):
        expenses_dict, total_expenses = self.__expenses_accumulator(
            "table#gastomensalverbagabinete"
        )

        return expenses_dict, total_expenses

    def __get_salary(self):
        salaryText = self.response.xpath(
            '//*[@id="recursos-section"]/ul/li[2]/div/a/text()'
        ).get()

        salary = float(salaryText.split("\n")[1].replace(".", "").replace(",", "."))

        return salary

    def run(self, gender):

        name, birth_date = self.__get_basic_data()

        plenary_presences, commissions_presences = self.__get_presence_data()

        trips = self.__trips_data()

        (
            parliamentary_expenses,
            total_parliamentary_expenses,
        ) = self.__get_parliamentary_expenses()

        (
            cabinet_expenses,
            total_cabinet_expenses,
        ) = self.__get_cabinet_expenses()

        salary = self.__get_salary()

        dep_data = {
            "nome": name,
            "genero": gender,
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
            "gasto_abr_par": parliamentary_expenses.get("abr"),
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
            "gasto_abr_gab": cabinet_expenses.get("abr"),
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

        return dep_data
