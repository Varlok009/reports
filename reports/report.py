import base64
from io import BytesIO
from matplotlib import pyplot
from os.path import dirname, abspath, join
from db.data_base import DataBase as DB
import pandas as pd
from models.params import BaseParams
import csv


class Report:
    def __init__(self, params: BaseParams) -> None:
        self.params = params.dict()
        self.partners = self.params.get('partners')
        self.dealers = self.params.get('dealers')
        self.years = self.params.get('years')
        self.months = self.params.get('months')
        self.days = self.params.get('days')
        self.aggr = self.params.get('aggr')

    def filter_data(self) -> pd.DataFrame:
        data = DB.data
        if self.partners:
            data = data.query(f'partner in {list(self.partners)}')
        if self.dealers:
            data = data.query(f'dealer in {list(self.dealers)}')
        if self.years:
            data = data.query(f'year_statement in {list(self.years)}')
        if self.months:
            data = data.query(f'month_statement in {list(self.months)}')
        return data

    @staticmethod
    def get_str_report(plot: pyplot) -> str:
        buf = BytesIO()
        plot.savefig(buf, format="png")
        plot = base64.b64encode(buf.getbuffer())
        plot = plot.decode('utf-8')
        return plot

    @staticmethod
    def get_png_report(plot: pyplot) -> str:
        path = dirname(dirname(abspath(__file__)))
        path = join(path, 'reports/heatmaps/')
        file_path = f"{path}report.png"
        plot.savefig(file_path)
        return file_path

    @staticmethod
    def get_csv_report(data: pd.DataFrame) -> str:
        path = dirname(dirname(abspath(__file__)))
        path = join(path, 'reports/basic/')
        file_path = f"{path}report.csv"
        data.to_csv(file_path, encoding='utf-8', sep=';', index=False)
        return file_path
