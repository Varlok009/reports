import pandas as pd
import seaborn as sns
import base64
from io import BytesIO
from matplotlib import pyplot as plt
from os.path import dirname, abspath, join


class Reports:
    @staticmethod
    def get_data() -> pd.DataFrame:
        path = dirname(dirname(abspath(__file__)))
        path = join(path, 'reports/')
        df = pd.read_csv(f'{path}data_copy.csv', delimiter=';')
        df.columns = ['bank', 'dealer', 'dealer_city', 'data_deal', 'data_credit']
        return df

    @staticmethod
    def convert_date_time_fields(df: pd.DataFrame) -> None:
        df['data_deal'] = pd.to_datetime(df['data_deal'])
        df['data_credit'] = pd.to_datetime(df['data_credit'])

    @staticmethod
    def get_report():
        deals = Reports.get_data()
        Reports.convert_date_time_fields(deals)
        deals['year_deal'] = deals['data_deal'].dt.year
        deals['month_deal'] = deals['data_deal'].dt.month
        # deals['day_of_weak_deal'] = deals['data_deal'].dt.dayofweek
        plt.figure(figsize=(7, 10))
        plt.title('Количество сделок')
        report = sns.heatmap(deals.pivot_table(index='month_deal', values='data_deal', columns=['year_deal'],
                                               aggfunc='count'),
                             annot=True, cbar=False, fmt='.1f', cmap="BuPu", linewidths=2, linecolor='gray')
        report = report.figure
        buf = BytesIO()
        report.savefig(buf, format="png")
        data = base64.b64encode(buf.getbuffer())
        print('report done')
        print(type(data))
        return data
        # return f"<img src='data:image/png;base64,{data}'/>"


# print(Reports.get_report())