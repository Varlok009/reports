import base64
from io import BytesIO
from matplotlib import pyplot
from os.path import dirname, abspath, join
import pandas as pd
import csv


class Report:
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
