from datetime import datetime
import os


class OSInteract:
    def __init__(self):
        now = datetime.now()
        year = now.year
        month = now.month
        day = now.day
        username = "taylorremund"
        self.root_path = f"/Users/{username}/Desktop/Reports/{year}/{month}/"
        self.reports_path = os.path.join(self.root_path, f"{day}/")
        self.json_path = os.path.join(self.root_path, "json_reports/")
        self.reports = [
            "zero_report",
            "double_report",
            "redstar_report",
            "moveout_report",
        ]

    def create_folders(self):
        for report in self.reports:
            report_path = os.path.join(self.reports_path, report)
            if not os.path.exists(report_path):
                os.makedirs(report_path)
        if not os.path.exists(self.json_path):
            os.makedirs(self.json_path)

    def retrieve_file(self, report):
        try:
            path = os.path.join(self.reports_path, report)
            file_name = os.listdir(path)[-1]
            file_path = os.path.join(path, file_name)
            return file_path
        except:
            return None
