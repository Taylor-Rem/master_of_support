from selenium.webdriver.common.by import By
from redstar_ops import RedstarOps


class RunRedstar:
    def __init__(self, webdriver, os_interact):
        self.webdriver = webdriver
        self.os_interact = os_interact
        self.redstar_ops = RedstarOps(webdriver)

    def run_redstar(self):
        file_path = self.os_interact.retrieve_file("redstar_report")
        URLs = self.os_interact.csv_ops.get_url_columns(file_path)
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
            self.rule_compliance = False
            if self.webdriver.element_status(By.XPATH, '//td//font[@color="red"]'):
                self.loop_through_tables()

    def loop_through_tables(self):
        # First loop to check Elements
        for row in self.current_month_rows:
            if self.is_header_row(row):
                continue
            (
                transaction,
                amount,
            ) = self.redstar_ops.retrieve_transaction_and_amount(row)
            if "RULE COMPLIANCE CREDIT" in transaction:
                self.rule_compliance = True
                self.rule_compliance_amount = amount

        if self.rule_compliance:
            self.redstar_ops.reallocate_rule_compliance(
                self.rule_compliance_amount, self.current_url
            )

        # Second loop to perform all actions
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
                self.webdriver.go_back(self.current_url)

        # Third loop to allocate all credits
        for row in self.current_month_rows:
            if self.is_header_row(row):
                continue
            (
                transaction,
                amount,
            ) = self.redstar_ops.retrieve_transaction_and_amount(row)
            self.redstar_ops.allocate_all_credits(
                amount, self.webdriver.return_last_element(transaction)
            )

    def bottom_ops(self, transaction, amount):
        for bottom_row in self.bottom_rows:
            if self.is_header_row(bottom_row):
                continue
            self.redstar_ops.bottom_ops(transaction, amount, bottom_row)

    def is_header_row(self, row):
        return row.find("td", class_="th3") is not None
