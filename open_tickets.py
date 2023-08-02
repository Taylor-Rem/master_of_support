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
        self.res_map_op.open_property(property)
        if unit is not None:
            self.res_map_op.open_unit_and_ledger(unit, resident)
