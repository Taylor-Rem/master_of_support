from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


class RedstarOps:
    def __init__(self, webdriver):
        self.webdriver = webdriver

    def redstar_status(self):
        try:
            element = self.webdriver.driver.find_element(
                By.XPATH,
                '//font[@color="red"]/ancestor::td[@class="td1" or @class="td2"]',
            )
            return True
        except NoSuchElementException:
            return False

    def choose_table(self, num):
        return f"/html/body/table[2]/tbody/tr[4]/td/table/tbody/tr/td/table[last(){num}]/tbody/tr[2]/td/table/tbody"

    def define_table(self, table_num):
        table_elements = self.webdriver.driver.find_elements(
            By.XPATH, self.choose_table(table_num)
        )
        table = table_elements[0] if table_elements else None
        return table

    def get_rows(self, table):
        if table:
            soup = BeautifulSoup(table.get_attribute("innerHTML"), "html.parser")
            rows = soup.find_all("tr")
            return rows
        else:
            return None

    def retrieve_transaction_and_amount(self, row):
        cells = row.find_all("td")
        transaction = cells[2].get_text(strip=True)
        amount = cells[3].get_text(strip=True)
        return transaction, amount

    def retrieve_amount_from_bottom(self, row):
        cells = row.find_all("td")
        amount = cells[1].get_text(strip=True)
        return amount

    def auto_allocate(self):
        self.webdriver.click(By.NAME, "realloc_trid")
        self.webdriver.click(By.NAME, "update")
