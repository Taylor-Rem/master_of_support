from selenium.webdriver.common.by import By
from redstar_ops import RedstarOps
import re


class RunRedstar:
    def __init__(self, webdriver, os_interact, csv_ops):
        self.webdriver = webdriver
        self.os_interact = os_interact
        self.csv_ops = csv_ops
        self.redstar_ops = RedstarOps(webdriver)
        self.tables = {"previous_month": -5, "current_month": -4, "bottom": -1}

    def run_redstar(self):
        file_path = self.os_interact.retrieve_file("redstar_report")
        URLs = self.csv_ops.get_url_columns(file_path)
        self.loop_through_ledgers(URLs)

    def loop_through_ledgers(self, URLs):
        for URL in URLs:
            # for i in range(2):
            self.webdriver.driver.get(URL)
            self.current_url = self.webdriver.driver.current_url
            current_month_rows = self.get_rows(self.tables["current_month"])
            bottom_rows = self.get_rows(self.tables["bottom"])
            if self.redstar_ops.redstar_status():
                self.loop_through_tables(current_month_rows, bottom_rows)

    def is_header_row(self, row):
        return row.find("td", class_="th3") is not None

    def get_rows(self, table_num):
        table = self.redstar_ops.define_table(table_num)
        rows = self.redstar_ops.get_rows(table)
        return rows

    def loop_through_tables(self, current, bottom):
        for row in current:
            self.go_back()
            if self.redstar_ops.redstar_status():
                if self.is_header_row(row):
                    continue
                transaction, amount = self.redstar_ops.retrieve_transaction_and_amount(
                    row
                )
                self.allocate_all_credits(transaction, amount)
                try:
                    if self.bottom_amount_is_amount(bottom[1], amount):
                        self.allocate_amount(transaction, amount)
                except:
                    pass

    def bottom_amount_is_amount(self, row, amount):
        bottom_amount = self.redstar_ops.retrieve_amount_from_bottom(row)
        return amount == bottom_amount

    def allocate_amount(self, transaction, amount):
        number = amount[2:]
        self.open_transaction(transaction)
        self.webdriver.send_keys(
            By.XPATH,
            "/html/body/table[2]/tbody/tr[4]/td/table/tbody/tr/td/table[2]/tbody/tr[2]/td/table/tbody/tr[2]/td[2]/form/input[4]",
            number,
            enter=True,
        )

    def allocate_all_credits(self, transaction, amount):
        if amount.startswith("(") or amount.endswith(")"):
            self.open_transaction(transaction)
            self.redstar_ops.auto_allocate()

    def open_transaction(self, transaction):
        self.webdriver.click(By.XPATH, f'//a[contains(text(), "{transaction}")]')

    def go_back(self):
        if not self.webdriver.check_webpage(self.current_url):
            self.webdriver.driver.back()
