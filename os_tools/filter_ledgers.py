from os_tools.os_interact import OSInteract, JsonOperations


class FilterLedgers:
    def __init__(self, report):
        self.os_interact = OSInteract()
        self.report = report
        self.file_path = self.os_interact.retrieve_file(self.report)
        self.json_ops = JsonOperations(self.os_interact.json_path, self.report)

    def current_report_items(self):
        properties, units, residents = self.os_interact.retrieve_report_info(
            self.file_path
        )
        current_report_items = []
        for i in range(len(properties)):
            property = properties[i]
            unit = float(units[i])
            resident = residents[i]
            json_entry = f"{property}_{unit}_{resident}"
            current_report_items.append(json_entry)
        return current_report_items

    def filter_properties(self):
        set1 = set(self.current_report_items())
        set2 = set(self.json_ops.retrieve_json())
        unique_elements = (set1 - set2) | (set2 - set1)
        properties = []
        units = []
        residents = []
        for item in unique_elements:
            prop, unit, res = item.split("_")
            properties.append(prop)
            units.append(float(unit))
            residents.append(res)
        return properties, units, residents
