from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


class CreditOps:
    def __init__(self, webdriver):
        self.webdriver = webdriver
        self.credit_functions = CreditFunctions(webdriver)

    def credit_charge(self, is_concession):
        self.credit_functions.get_name_and_bill_amount()
        self.credit_functions.define_select()
        self.credit_functions.fill_select(is_concession)
        self.credit_functions.send_credit_keys()


class CreditFunctions:
    def __init__(self, webdriver):
        self.webdriver = webdriver

    def get_name_and_bill_amount(self):
        rows = self.get_rows(By.XPATH, "//tr[contains(@class, 'td')]")
        row = rows[-1]
        columns = row.find_all("td")
        bill_amount_str = columns[2].text.strip()
        bill_amount_replace = bill_amount_str.replace("$", "").replace(" ", "")

        self.name = columns[0].text.strip()
        self.bill_amount = float(bill_amount_replace)

    def define_select(self):
        select_element = self.webdriver.driver.find_element(
            By.XPATH, "//select[@name='ttid']"
        )
        self.select = Select(select_element)

    def fill_select(self, is_concession):
        if (self.name == "Rent" or "Home Rental") and is_concession:
            self.select.select_by_visible_text(f"{self.name} Concession")
        else:
            self.select.select_by_visible_text(self.name)

    def send_credit_keys(self):
        credit_input = self.webdriver.driver.find_element(
            By.XPATH, "//input[@type='text' and @name='amount']"
        )
        self.webdriver.send_keys_element(credit_input, self.bill_amount)
        comments = self.webdriver.driver.find_element(
            By.XPATH, "//textarea[@name='comments']"
        )
        self.webdriver.send_keys_element(comments, "charge concession")
        self.webdriver.click(By.XPATH, "//input[@type='submit' and @name='submit1']")
