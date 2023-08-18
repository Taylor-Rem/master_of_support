from resmap_tools.webpage_ops import ManageportalOps


class OpenTickets:
    def __init__(self, webdriver, resmap_ops):
        self.webdriver = webdriver
        self.resmap_ops = resmap_ops
        self.manageportal_ops = ManageportalOps(webdriver)

    def change_ticket_status(self, icon, back):
        self.webdriver.switch_to_primary_tab()
        self.manageportal_ops.resolve_ticket(icon, back)

    def open_ticket(self):
        self.webdriver.switch_to_primary_tab()
        property, unit, resident = self.resmap_ops.scrape.scrape_ticket()
        print(property, unit, resident)
        self.webdriver.new_tab()
        self.webdriver.open_program(self.webdriver.res_map_url)
        self.resmap_ops.open_ledger(property, unit, resident)
