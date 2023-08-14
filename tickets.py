from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from webpage_ops import ManageportalOps


class OpenTickets:
    def __init__(self, webdriver, scrape, resmap_ops):
        self.webdriver = webdriver
        self.scrape = scrape
        self.resmap_ops = resmap_ops

    def open_ticket(self):
        self.webdriver.switch_to_primary_tab()
        property, unit, resident = self.scrape.scrape_ticket()
        print(property, unit, resident)
        self.webdriver.new_tab()
        self.webdriver.open_program(self.webdriver.res_map_url)
        self.resmap_ops.open_ledger(property, unit, resident)


class TicketLedgerOps:
    def __init__(self, webdriver, resmap_ops):
        self.webdriver = webdriver
        self.resmap_ops = resmap_ops
        self.manageportal_ops = ManageportalOps(webdriver)

    def change_ticket_status(self, icon, back):
        self.webdriver.switch_to_primary_tab()
        self.manageportal_ops.resolve_ticket(icon, back)

    def delete_all_late_fees(self):
        rows = self.resmap_ops.get_rows(self.resmap_ops.tables["current_month"])
        for row in rows:
            if self.resmap_ops.is_header_row(row):
                continue
            transaction, amount = self.resmap_ops.retrieve_transaction_and_amount(row)
            if "Late" in transaction:
                late_fee_element = self.webdriver.return_elements("Late Fee")
                self.webdriver.click_element(late_fee_element[-1])
                self.webdriver.click(By.NAME, "delete")
                alert = self.webdriver.driver.switch_to.alert
                alert.accept()

    def credit_all_charges(self):
        add_credit_btn = self.webdriver.return_last_element("Add Credit")
        self.webdriver.click_element(add_credit_btn)
        table_elements = self.webdriver.driver.find_elements(
            By.XPATH,
            "/html/body/table[2]/tbody/tr[4]/td/table/tbody/tr/td/form/table[2]/tbody/tr[2]/td/table/tbody",
        )
        table = table_elements[0] if table_elements else None
        print(table)
        # rows = self.resmap_ops.get_rows(table)
        # for row in rows:
        #     if self.resmap_ops.is_header_row(row):
        #         continue
        #     transaction, amount = self.resmap_ops.retrieve_transaction_and_amount(row)
        #     print(transaction, amount)
        # dropdown = self.webdriver.driver.find_element(By.NAME, "ttid")
        # select = Select(dropdown)
        # select.select_by_visible_text("Rent")
