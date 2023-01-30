import pandas as pd
import seaborn as sns
import base64
from io import BytesIO
from matplotlib import pyplot as plt
from os.path import dirname, abspath, join


class Report:
    partners = {'rosbank': 'Росбанк',
                'setelem': 'ДрайвКлик'}

    @staticmethod
    def convert_date_time_fields(df: pd.DataFrame) -> None:
        df['data_bid'] = pd.to_datetime(df['data_bid'], format='%d.%m.%Y')
        df['data_credit'] = pd.to_datetime(df['data_credit'], format='%d.%m.%Y')
        df['day_of_weak_bid'] = df['data_bid'].dt.dayofweek

    @staticmethod
    def get_data() -> pd.DataFrame:
        path = dirname(dirname(abspath(__file__)))
        path = join(path, 'reports/')
        df = pd.read_csv(f'{path}data_copy.csv', delimiter=';')
        df.columns = ['bank', 'dealer', 'dealer_city', 'data_bid', 'data_credit']
        Report.convert_date_time_fields(df)
        return df

    @staticmethod
    def get_str_report(plot) -> str:
        buf = BytesIO()
        plot.savefig(buf, format="png")
        plot = base64.b64encode(buf.getbuffer())
        plot = plot.decode('utf-8')
        return plot

    @staticmethod
    def get_deal_report(partner: str | None = None) -> str:
        deals = Report.get_data()
        deals['year_credit'] = deals['data_credit'].dt.year
        deals['month_credit'] = deals['data_credit'].dt.month
        deals['day_of_weak_bid'] = deals['data_bid'].dt.dayofweek
        plt.figure(figsize=(7, 10))
        plt.title('Количество сделок')
        report = sns.heatmap(deals.pivot_table(index='month_credit', values='data_credit', columns=['year_credit'],
                                               aggfunc='count'),
                             annot=True, cbar=False, fmt='.1f', cmap="BuPu", linewidths=2, linecolor='gray')
        report = Report.get_str_report(report.figure)
        print('report done')
        return report

    @staticmethod
    def get_bid_report(partner: str | None = None) -> str:
        bid = Report.get_data()
        bid['year_bid'] = bid['data_bid'].dt.year
        bid['month_bid'] = bid['data_bid'].dt.month
        bid['day_of_weak_bid'] = bid['data_bid'].dt.dayofweek
        plt.figure(figsize=(7, 10))
        plt.title('Количество заявок')
        report = sns.heatmap(bid.pivot_table(index='month_bid', values='data_bid', columns=['year_bid'],
                                             aggfunc='count'),
                             annot=True, cbar=False, fmt='.1f', cmap="BuPu", linewidths=2, linecolor='gray')
        report = Report.get_str_report(report.figure)
        print('report done')
        return report
