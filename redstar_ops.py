from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from transaction_ops import TransactionOps
from bs4 import BeautifulSoup


class RedstarOps:
    def __init__(self, webdriver):
        self.webdriver = webdriver
        self.transaction_ops = TransactionOps(webdriver)
        self.tables = {"previous_month": -5, "current_month": -4, "bottom": -1}

    def choose_table(self, num):
        return f"/html/body/table[2]/tbody/tr[4]/td/table/tbody/tr/td/table[last(){num}]/tbody/tr[2]/td/table/tbody"

    def define_table(self, table_num):
        table_elements = self.webdriver.driver.find_elements(
            By.XPATH, self.choose_table(table_num)
        )
        table = table_elements[0] if table_elements else None
        return table

    def retrieve_amount_from_bottom(self, row):
        try:
            cells = row.find_all("td")
            amount = cells[1].get_text(strip=True)
            return self.webdriver.get_number_from_string(amount)
        except:
            return None

    def scrape_page(self):
        prepaid_rent_amount = self.webdriver.get_number_from_string(
            self.webdriver.return_element(
                By.XPATH,
                "/html/body/table[2]/tbody/tr[4]/td/table/tbody/tr/td/table[3]/tbody/tr[2]/td/table/tbody/tr[3]/td[5]",
            )
        )
        current_url = self.webdriver.driver.current_url
        current_month_rows = self.get_rows(self.tables["current_month"])
        bottom_rows = self.get_rows(self.tables["bottom"])
        return prepaid_rent_amount, current_url, current_month_rows, bottom_rows

    def get_rows(self, table_num):
        table = self.define_table(table_num)
        if table:
            soup = BeautifulSoup(table.get_attribute("innerHTML"), "html.parser")
            rows = soup.find_all("tr")
            return rows
        else:
            return None

    def reallocate_rule_compliance(self, compliance_amount, current_url):
        self.webdriver.click_element(self.webdriver.return_last_element("Rent"))
        self.transaction_ops.subtract_compliance_from_rent(compliance_amount)
        self.webdriver.go_back(current_url)

    def allocate_all_credits(self, amount, element):
        if amount.startswith("(") or amount.endswith(")"):
            self.webdriver.click_element(element)
            self.transaction_ops.auto_allocate()

    def allocate_cents(self, amount_num, prepaid_amount):
        if amount_num == prepaid_amount:
            try:
                self.webdriver.click_element(
                    self.webdriver.return_last_element("Home Rental")
                )
                self.transaction_ops.allocate_cents(amount_num)
            except:
                self.webdriver.click_element(self.webdriver.return_last_element("Rent"))
                self.transaction_ops.allocate_cents(amount_num)

    def retrieve_transaction_and_amount(self, row):
        cells = row.find_all("td")
        transaction = cells[2].get_text(strip=True)
        amount = cells[3].get_text(strip=True)
        return transaction, amount

    def bottom_ops(self, transaction, amount, bottom_row):
        bottom_amount = self.retrieve_amount_from_bottom(bottom_row)
        if bottom_amount == amount:
            self.webdriver.click_element(
                self.webdriver.return_last_element(transaction)
            )
            self.transaction_ops.allocate_amount(amount)
