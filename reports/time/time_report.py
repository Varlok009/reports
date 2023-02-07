import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
from reports.report import Report
from db.data_base import DataBase as DB
import calendar, locale


class TimeReport(Report):
    def __init__(self,
                 partners: set | None, years: set | None, months: set | None,
                 days: bool, aggr: str,
                 stage: str
                 ) -> None:
        self.partners = partners
        self.years = years
        self.months = months
        self.days = days
        self.aggr = aggr
        self.stage = stage
        self.data = self.filter_data()

    def filter_data(self) -> pd.DataFrame:
        data = DB.data
        if self.partners:
            data = data.query(f'partner in {list(self.partners)}')
        if self.years:
            data = data.query(f'year_statement in {list(self.years)}')
        if self.months:
            data = data.query(f'month_statement in {list(self.months)}')
        data = data.query(f'{self.stage}_status_at != "NaN"')
        data[f'time_to_{self.stage}'] = (data[f'{self.stage}_status_at'] - data['date_create_anketa']
                                         ).dt.components.minutes
        return data

    def get_time_report(self) -> str:
        statement = self.data
        plt.title('Время на финансирование')
        print(statement)
        plt.figure(figsize=(10, 10))
        report = sns.heatmap(statement.pivot_table(index='month_statement', values=f"time_to_{self.stage}",
                                                   columns=['year_statement'],
                                                   aggfunc=self.aggr),
                             annot=True, cbar=False, fmt='.1f', cmap="BuPu", linewidths=2, linecolor='gray')
        report = self.get_str_report(report.figure)
        return report


# my_report = HeatmapReport()
# print(my_report.get_deal_report())
