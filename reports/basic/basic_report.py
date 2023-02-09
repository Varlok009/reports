from reports.report import Report
from models.params import BaseParams


class BasicReport(Report):
    def __init__(self, params: BaseParams) -> None:
        super().__init__(params)
        self.data = self.filter_data()

    def get_basic_statement_report(self) -> str:
        statements = self.data
        return self.get_csv_report(statements)
