from selenium.webdriver.common.by import By
from redstar_ops import RedstarOps


class RunRedstar:
    def __init__(self, webdriver, os_interact, csv_ops):
        self.webdriver = webdriver
        self.os_interact = os_interact
        self.csv_ops = csv_ops
        self.redstar_ops = RedstarOps(webdriver)

    def run_redstar(self):
        file_path = self.os_interact.retrieve_file("redstar_report")
        URLs = self.csv_ops.get_url_columns(file_path)
        self.loop_through_ledgers(URLs)

    def loop_through_ledgers(self, URLs):
        for URL in URLs:
            # for i in range(3):
            self.webdriver.driver.get(URL)
            self.current_url = self.webdriver.driver.current_url
            table = self.redstar_ops.define_table(-4)
            rows = self.redstar_ops.get_rows(table)
            self.loop_through_table(rows)

    def loop_through_table(self, rows):
        for row in rows:
            if not self.redstar_ops.redstar_status():
                break
            if row.find("td", class_="th3"):
                continue
            transaction, amount = self.redstar_ops.return_transaction_and_amount(row)
            self.allocate_all_credits(transaction, amount)
            self.go_back()

    def allocate_all_credits(self, transaction, amount):
        if amount.startswith("(") or amount.endswith(")"):
            self.open_transaction(transaction)
            self.redstar_ops.auto_allocate()

    def open_transaction(self, transaction):
        self.webdriver.click(By.XPATH, f'//a[contains(text(), "{transaction}")]')

    def go_back(self):
        if not self.webdriver.check_webpage(self.current_url):
            self.webdriver.driver.back()
