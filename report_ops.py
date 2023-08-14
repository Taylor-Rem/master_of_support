from filter_ledgers import FilterLedgers


class ReportOperations:
    def __init__(self, webdriver, resmap_ops, report):
        self.webdriver = webdriver
        self.resmap_ops = resmap_ops
        self.filter_ledgers = FilterLedgers(report)
        self.json_ops = self.filter_ledgers.json_ops
        self.temp_storage = self.json_ops.retrieve_json()
        self.current_index = 0
        (
            self.properties,
            self.units,
            self.residents,
        ) = self.filter_ledgers.filter_properties()
        self.open_ledger()

    def open_ledger(self):
        self.property = self.properties[self.current_index]
        self.unit = self.units[self.current_index]
        self.resident = self.residents[self.current_index]
        print(self.property, self.unit, self.resident)
        self.resmap_ops.open_ledger(self.property, self.unit, self.resident)

    def next_ledger(self):
        self.current_index += 1
        self.open_ledger()

    def add_button(self):
        self.add_to_json()
        self.next_ledger()

    def skip_button(self):
        self.next_ledger()

    def add_to_json(self):
        json_entry = f"{self.property}_{str(self.unit)}_{self.resident}"
        self.temp_storage.append(json_entry)
        self.json_ops.write_json(self.temp_storage)
