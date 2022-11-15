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

    def get_presence_data(
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

    def get_basic_data(self):

        name_xpath_id, birth_date_xpath_id = [1, 5]

        name = self.__extract_basic_info(name_xpath_id)
        birth_date = self.__extract_basic_info(birth_date_xpath_id)

        return name, birth_date

    def trips_data(self):
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

    def get_parliamentary_expenses(self):
        expenses_dict, total_expenses = self.__expenses_accumulator(
            "table#gastomensalcotaparlamentar"
        )

        return expenses_dict, total_expenses

    def get_cabinet_expenses(self):
        expenses_dict, total_expenses = self.__expenses_accumulator(
            "table#gastomensalverbagabinete"
        )

        return expenses_dict, total_expenses

    def get_salary(self):
        salaryText = self.response.xpath(
            '//*[@id="recursos-section"]/ul/li[2]/div/a/text()'
        ).get()

        salary = float(salaryText.split("\n")[1].replace(".", "").replace(",", "."))

        return salary
