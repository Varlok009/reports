import pandas as pd
from reports.report import Report
from db.data_base import DataBase as DB


class BasicReport(Report):
    def __init__(self, partners: list | None, years: list | None, months: list | None, days: bool) -> None:
        self.partners = partners
        self.years = years
        self.months = months
        self.days = days
        self.data = DB.data

    def get_basic_bid_report(self) -> str:
        bid = self.data
        bid['year_bid'] = bid['data_bid'].dt.year
        bid['month_bid'] = bid['data_bid'].dt.month
        bid['day_of_weak_bid'] = bid['data_bid'].dt.dayofweek

        if self.partners:
            bid = bid.query(f'partner in {list(self.partners)}')
        if self.years:
            bid = bid.query(f'year_bid in {list(self.years)}')
        if self.months:
            bid = bid.query(f'month_bid in {list(self.months)}')

        return self.get_csv_report(bid)
        # elif


# my_report = HeatmapReport()
# print(my_report.get_deal_report())
