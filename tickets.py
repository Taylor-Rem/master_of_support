from selenium.webdriver.common.by import By

from webpage_ops import ManageportalOps


class OpenTickets:
    def __init__(self, webdriver, resmap_ops):
        self.webdriver = webdriver
        self.resmap_ops = resmap_ops

    def open_ticket(self):
        self.webdriver.switch_to_primary_tab()
        property, unit, resident = self.resmap_ops.scrape.scrape_ticket()
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

    def loop(self, operation, is_concession=False):
        rows = self.resmap_ops.get_rows(
            By.XPATH,
            self.resmap_ops.scrape.choose_table(
                self.resmap_ops.scrape.tables["current_month"]
            ),
        )
        for row in rows:
            if self.resmap_ops.is_header_row(row, "th3"):
                continue
            (
                transaction,
                amount,
            ) = self.resmap_ops.scrape.retrieve_transaction_and_amount(row)

        if operation == "allocate_all":
            self.resmap_ops.allocate_all_credits(
                amount, self.webdriver.return_last_element(transaction)
            )

        if operation == "credit_all_charges":
            self.resmap_ops.credit_all_charges(is_concession)

        if operation == "delete_all_charges":
            self.resmap_ops.delete_charges(transaction)

        if operation == "delete_all_late_fees":
            self.resmap_ops.delete_charges("Late")
