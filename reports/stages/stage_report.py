import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from reports.report import Report
from db.data_base import DataBase as DB
from models.params import StageParams


class StageReport(Report):
    def __init__(self, params: StageParams) -> None:
        super().__init__(params)
        self.stage = self.params.get('stage')
        self.data = self.filter_data()

    def filter_data(self) -> pd.DataFrame:
        data = super().filter_data()
        data = data.query(f'{self.stage}_status_at != "NaN"')
        data[f'time_to_{self.stage}'] = (data[f'{self.stage}_status_at'] - data['date_create_anketa']
                                         ).dt.components.minutes
        return data

    def get_time_report(self) -> str:
        statement = self.data
        plt.title('Время на финансирование')
        plt.figure(figsize=(10, 10))
        report = sns.heatmap(statement.pivot_table(index='month_statement', values=f"time_to_{self.stage}",
                                                   columns=['year_statement'],
                                                   aggfunc=self.aggr),
                             annot=True, cbar=False, fmt='.1f', cmap="BuPu", linewidths=2, linecolor='gray')
        report = self.get_png_report(report.figure)
        return report
