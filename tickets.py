from selenium.webdriver.common.by import By
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
        self.resmap_ops.open_property(property)
        if unit is not None:
            self.resmap_ops.open_unit_and_ledger(unit, resident)


class TicketLedgerOps:
    def __init__(self, webdriver):
        self.webdriver = webdriver
        self.manageportal_ops = ManageportalOps(webdriver)

    def change_ticket_status(self, icon, back):
        self.webdriver.switch_to_primary_tab()
        self.manageportal_ops.resolve_ticket(icon, back)
