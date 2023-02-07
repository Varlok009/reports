import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from reports.report import Report
from db.data_base import DataBase as DB
import calendar, locale


class HeatmapReport(Report):
    def __init__(self, partners: list | None, years: list | None, months: list | None, days: bool, aggr: str) -> None:
        self.partners = partners
        self.years = years
        self.months = months
        self.days = days
        self.data = self.filter_data()
        self.aggr = aggr

    def filter_data(self) -> pd.DataFrame:
        data = DB.data
        if self.partners:
            data = data.query(f'partner in {list(self.partners)}')
        if self.years:
            data = data.query(f'year_statement in {list(self.years)}')
        if self.months:
            data = data.query(f'month_statement in {list(self.months)}')
        return data

    def set_heatmap_settings(self) -> None:
        locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
        if self.days:
            self.x_axis_labels = [day.capitalize() for day in calendar.day_abbr if day]
        if not self.months:
            self.y_axis_labels = [month.capitalize() for month in calendar.month_abbr if month]
        else:
            self.y_axis_labels = [month.capitalize() for month_number, month in enumerate(calendar.month_abbr, start=0)
                                  if month_number in self.months]

    def get_heatmap_credit_report(self) -> str:
        credit = self.data
        credit = credit.query(f'funded_status_at != "NaN"')
        plt.title('Кредиты')
        plt.figure(figsize=(12, 6))
        self.set_heatmap_settings()
        report = sns.heatmap(credit.pivot_table(index='month_statement', values='price',
                                                columns='year_statement' if not self.days else 'day_of_weak_statement',
                                                aggfunc=self.aggr),
                             xticklabels=self.x_axis_labels if self.days else 'auto',
                             yticklabels=self.y_axis_labels,
                             annot=True, cbar=False, fmt='.1f', cmap="BuPu", linewidths=2, linecolor='gray')
        report = self.get_str_report(report.figure)
        return report

    def get_heatmap_statement_report(self) -> str:
        statement = self.data
        plt.title('Заявки')
        plt.figure(figsize=(12, 6))
        self.set_heatmap_settings()
        report = sns.heatmap(statement.pivot_table(index='month_statement', values='price',
                                                   columns='year_statement' if not self.days else 'day_of_weak_statement',
                                                   aggfunc=self.aggr),
                             xticklabels=self.x_axis_labels if self.days else 'auto',
                             yticklabels=self.y_axis_labels,
                             annot=True, cbar=False, fmt='.1f', cmap="BuPu", linewidths=2, linecolor='gray')
        report = self.get_str_report(report.figure)
        return report


# my_report = HeatmapReport()
# print(my_report.get_deal_report())
