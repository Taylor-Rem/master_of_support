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
            self.webdriver.driver.get(URL)
            (
                self.prepaid_rent_amount,
                self.current_url,
                self.current_month_rows,
                self.bottom_rows,
            ) = self.redstar_ops.scrape_page()

            if self.webdriver.element_status(By.XPATH, '//td//font[@color="red"]'):
                self.loop_through_tables()

    def loop_through_tables(self):
        for row in self.current_month_rows:
            if self.webdriver.element_status(By.XPATH, '//td//font[@color="red"]'):
                if self.is_header_row(row):
                    continue
                (
                    transaction,
                    amount,
                ) = self.redstar_ops.retrieve_transaction_and_amount(row)
                amount_num = self.webdriver.get_number_from_string(amount)
                self.bottom_ops(transaction, amount_num)
                self.redstar_ops.allocate_cents(amount_num, self.prepaid_rent_amount)
                self.go_back()
        for row in self.current_month_rows:
            self.redstar_ops.allocate_all_credits(
                amount, self.redstar_ops.return_last_element(transaction)
            )

    def bottom_ops(self, transaction, amount):
        for bottom_row in self.bottom_rows:
            if self.is_header_row(bottom_row):
                continue
            self.redstar_ops.bottom_ops(transaction, amount, bottom_row)

    def is_header_row(self, row):
        return row.find("td", class_="th3") is not None

    def go_back(self):
        if not self.webdriver.check_webpage(self.current_url):
            self.webdriver.driver.back()

            # self.redstar_ops.allocate_rule_compliance(
            #     transaction,
            #     self.redstar_ops.return_last_element("Rent"),
            # )
