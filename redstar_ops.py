from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time


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
        try:
            cells = row.find_all("td")
            amount = cells[1].get_text(strip=True)
            return amount
        except:
            return None

    def auto_allocate(self):
        self.webdriver.click(By.NAME, "realloc_trid")
        self.webdriver.click(By.NAME, "update")

    def bottom_amount_is_amount(self, row, amount):
        bottom_amount = self.retrieve_amount_from_bottom(row)
        return amount == bottom_amount

    def is_header_row(self, row):
        return row.find("td", class_="th3") is not None

    def allocate_amount(self, transaction, bottom_row, amount):
        if self.bottom_amount_is_amount(bottom_row, amount):
            self.open_transaction(transaction)
            self.webdriver.send_keys(
                By.XPATH,
                "/html/body/table[2]/tbody/tr[4]/td/table/tbody/tr/td/table[2]/tbody/tr[2]/td/table/tbody/tr[2]/td[2]/form/input[4]",
                amount,
                True,
            )

    def open_transaction(self, transaction):
        elements = self.webdriver.driver.find_elements(
            By.XPATH, f'//a[contains(text(), "{transaction}")]'
        )
        if elements:
            self.webdriver.click_element(elements[-1])
        else:
            self.webdriver.click(By.XPATH, f'//a[contains(text(), "{transaction}")]')

    def allocate_all_credits(self, transaction, amount):
        if amount.startswith("(") or amount.endswith(")"):
            self.open_transaction(transaction)
            self.auto_allocate()

    def bottom_ops(self, transaction, amount, bottom):
        for bottom_row in bottom:
            if self.is_header_row(bottom_row):
                continue
            self.allocate_amount(transaction, bottom_row, amount)

    def allocate_cents(self, amount):
        try:
            full_charge = float(
                self.webdriver.driver.find_element(
                    By.XPATH,
                    "/html/body/table[2]/tbody/tr[4]/td/table/tbody/tr/td/form/table/tbody/tr[2]/td/table/tbody/tr[2]/td[2]/input",
                ).get_attribute("value")
            )
            current_allocation_element = self.allocation_elements(2)
            current_allocation_value = float(
                current_allocation_element.get_attribute("value")
            )
            if full_charge == current_allocation_value:
                self.subtract_current_allocation(
                    current_allocation_element, current_allocation_value, amount
                )
                additional_rent_element = self.allocation_elements(3)
                self.webdriver.send_keys_element(additional_rent_element, amount, True)
            if current_allocation_value == 0:
                self.webdriver.send_keys_element(
                    current_allocation_element, amount, True
                )
        except:
            pass

    def subtract_current_allocation(
        self, current_allocation_element, current_allocation_value, amount
    ):
        new_allocation = round(current_allocation_value - amount, 2)
        self.webdriver.send_keys_element(
            current_allocation_element, new_allocation, True
        )

    def allocation_elements(self, num):
        return self.webdriver.driver.find_element(
            By.XPATH,
            f"/html/body/table[2]/tbody/tr[4]/td/table/tbody/tr/td/table[2]/tbody/tr[2]/td/table/tbody/tr[{num}]/td[2]/form/input[4]",
        )
