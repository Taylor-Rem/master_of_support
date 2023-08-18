from tool.report_ops import ReportOperations
from tool.tickets import OpenTickets

from FrontEnd.helper_windows import HelperWidget, LedgerOps


class TicketHelper(HelperWidget):
    def __init__(self, main_app):
        super().__init__(main_app, "Ticket Helper")
        self.icons = {
            "In Progress": "scatter_plot",
            "Resolved": "done_outline",
            "Back": "arrow_back",
        }

        self.open_btn = self.create_button("🤖 Open Ticket", self.open_ticket)
        self.in_progress_btn = self.create_button(
            "🔵 In Progress",
            lambda: (
                self.change_ticket_status(self.icons["In Progress"], self.icons["Back"])
            ),
        )
        self.resolve_btn = self.create_button(
            "✅ Resolve", lambda: (self.change_ticket_status(self.icons["Resolved"]))
        )
        self.open_ticket_op = OpenTickets(main_app.webdriver, main_app.resmap_ops)
        self.add_back_btn()

    def open_ticket(self):
        self.main_app.switch_window(self.main_app.ticket_ops)
        self.open_ticket_op.open_ticket()

    def change_ticket_status(self, icon, back=None):
        self.open_ticket_op.change_ticket_status(icon, back)


class TicketOps(LedgerOps):
    def __init__(self, main_app):
        super().__init__(main_app, "Ticket Ops")
        self.create_ledger_buttons()


class ChooseReport(HelperWidget):
    def __init__(self, main_app):
        super().__init__(main_app, "Choose Report")
        self.zero_btn = self.create_button(
            "Zero Report", lambda: (self.open_report("zero_report"))
        )
        self.double_btn = self.create_button(
            "Double Report", lambda: (self.open_report("double_report"))
        )
        self.moveout_btn = self.create_button(
            "Moveout Report", lambda: (self.open_report("moveout_report"))
        )
        self.os_interact = main_app.os_interact
        self.add_back_btn()

    def open_report(self, report):
        try:
            report_ops = ReportOperations(
                self.main_app.webdriver, self.main_app.resmap_ops, report
            )
            report_helper_window = ReportHelper(self.main_app, report_ops, report)
            self.main_app.stack.addWidget(report_helper_window)
            self.main_app.switch_window(report_helper_window)
        except:
            print("Report Complete!")


class ReportHelper(LedgerOps):
    def __init__(self, main_app, report_ops=None, report="_"):
        self.report_ops = report_ops
        super().__init__(main_app, report.replace("_", " "))
        self.complete_btn = self.create_button("✅ Add", self.add_report)
        self.skip_btn = self.create_button("⛔️ Skip", self.skip_report)
        self.go_to_former_btn = self.create_button("Go to Former", self.go_to_former)
        self.create_ledger_buttons()

    def add_report(self):
        try:
            self.report_ops.add_button()
        except:
            self.main_app.stack.setCurrentWidget(self.main_app.choose_report)
            print("Report Complete!")

    def skip_report(self):
        try:
            self.report_ops.skip_button()
        except:
            self.main_app.stack.setCurrentWidget(self.main_app.choose_report)
            print("Report Complete!")

    def go_to_former(self):
        self.report_ops.go_to_former()


class RedstarWindow(HelperWidget):
    def __init__(self, main_app):
        super().__init__(main_app, "Red Star")
        self.redstar = self.main_app.redstar
        self.redstar_helper_btn = self.create_button(
            "Redstar Helper", self.redstar_helper
        )
        self.run_report_btn = self.create_button("Run Report", self.run_report)
        self.add_back_btn()

    def redstar_helper(self):
        self.redstar.redstar_ops.open_ledger()
        self.main_app.switch_window(self.main_app.redstar_helper)

    def run_report(self):
        self.redstar.auto_redstar.loop_through_ledgers()


class RedstarHelper(LedgerOps):
    def __init__(self, main_app):
        super().__init__(main_app, "Red Star Helper")
        self.redstar = self.main_app.redstar
        self.next_ledger_btn = self.create_button(
            "Next Ledger", lambda: self.cycle_ledger(True)
        )
        self.prev_ledger_btn = self.create_button(
            "Prev Ledger", lambda: self.cycle_ledger(False)
        )
        self.create_ledger_buttons()

    def cycle_ledger(self, next):
        self.redstar.redstar_ops.cycle_ledger(next)
