import pandas as pd
from os.path import dirname, abspath, join


class DataBase:
    data = None

    @classmethod
    def set_data(cls) -> None:
        if cls.data is None:
            path = dirname(dirname(abspath(__file__)))
            path = join(path, 'db/')
            df = pd.read_csv(f'{path}sql.csv', delimiter=';')
            # df.columns = ['partner', 'dealer', 'dealer_city', 'data_bid', 'data_credit']
            cls.__convert_date_time_fields(df)
            cls.data = df
            print('Upload new data set')

    @staticmethod
    def __convert_date_time_fields(df: pd.DataFrame) -> None:
        df['date_create_anketa'] = pd.to_datetime(df['date_create_anketa'])
        df['date_create_statement'] = pd.to_datetime(df['date_create_statement'])
        df['pre_approved_status_at'] = pd.to_datetime(df['pre_approved_status_at'])
        df['approved_status_at'] = pd.to_datetime(df['approved_status_at'])
        df['funded_status_at'] = pd.to_datetime(df['funded_status_at'])

        df['year_statement'] = df['date_create_statement'].dt.year
        df['month_statement'] = df['date_create_statement'].dt.month
        df['day_of_weak_statement'] = df['date_create_statement'].dt.dayofweek

        df['year_credit'] = df['funded_status_at'].dt.year
        df['month_credit'] = df['funded_status_at'].dt.month
        df['day_of_weak_credit'] = df['funded_status_at'].dt.dayofweek



