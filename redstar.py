from selenium.webdriver.common.by import By
from redstar_ops import RedstarOps
import re


class RunRedstar:
    def __init__(self, webdriver, os_interact, csv_ops):
        self.webdriver = webdriver
        self.os_interact = os_interact
        self.csv_ops = csv_ops
        self.redstar_ops = RedstarOps(webdriver)
        # self.prepaid_rent_amount = self.webdriver.return_element(
        #     By.XPATH,
        #     "/html/body/table[2]/tbody/tr[4]/td/table/tbody/tr/td/table[3]/tbody/tr[2]/td/table/tbody/tr[3]/td[5]",
        # )
        self.tables = {"previous_month": -5, "current_month": -4, "bottom": -1}

    def run_redstar(self):
        file_path = self.os_interact.retrieve_file("redstar_report")
        URLs = self.csv_ops.get_url_columns(file_path)
        self.loop_through_ledgers(URLs)

    def loop_through_ledgers(self, URLs):
        for URL in URLs:
            self.webdriver.driver.get(URL)
            self.retrieve_page_info()
            if self.redstar_ops.redstar_status():
                self.loop_through_tables()

    def retrieve_page_info(self):
        self.prepaid_rent_amount = self.webdriver.get_number_from_string(
            self.webdriver.return_element(
                By.XPATH,
                "/html/body/table[2]/tbody/tr[4]/td/table/tbody/tr/td/table[3]/tbody/tr[2]/td/table/tbody/tr[3]/td[5]",
            )
        )
        self.current_url = self.webdriver.driver.current_url
        self.current_month_rows = self.get_rows(self.tables["current_month"])
        self.bottom_rows = self.get_rows(self.tables["bottom"])

    def get_rows(self, table_num):
        table = self.redstar_ops.define_table(table_num)
        rows = self.redstar_ops.get_rows(table)
        return rows

    def loop_through_tables(self):
        for row in self.current_month_rows:
            if self.redstar_ops.redstar_status():
                if self.redstar_ops.is_header_row(row):
                    continue
                transaction, amount = self.redstar_ops.retrieve_transaction_and_amount(
                    row
                )
                amount_num = self.webdriver.get_number_from_string(amount)
                self.redstar_ops.bottom_ops(transaction, amount_num, self.bottom_rows)
                self.redstar_ops.allocate_all_credits(transaction, amount)
                if amount_num == self.prepaid_rent_amount:
                    self.redstar_ops.open_transaction("Rental")
                    self.redstar_ops.allocate_cents(amount_num)
                self.go_back()

    def go_back(self):
        if not self.webdriver.check_webpage(self.current_url):
            self.webdriver.driver.back()
