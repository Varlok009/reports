import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from reports.report import Report


class HeatmapReport(Report):
    def get_heatmap_deal_report(self, partner: str | None = None) -> str:
        deals = self.get_data()
        deals['year_credit'] = deals['data_credit'].dt.year
        deals['month_credit'] = deals['data_credit'].dt.month
        deals['day_of_weak_bid'] = deals['data_bid'].dt.dayofweek
        plt.figure(figsize=(7, 10))
        plt.title('Количество сделок')
        report = sns.heatmap(deals.pivot_table(index='month_credit', values='data_credit', columns=['year_credit'],
                                               aggfunc='count'),
                             annot=True, cbar=False, fmt='.1f', cmap="BuPu", linewidths=2, linecolor='gray')
        report = self.get_str_report(report.figure)
        print('report done')
        return report

    def get_heatmap_bid_report(self) -> str:
        bid = self.get_data()
        bid['year_bid'] = bid['data_bid'].dt.year
        bid['month_bid'] = bid['data_bid'].dt.month
        bid['day_of_weak_bid'] = bid['data_bid'].dt.dayofweek
        plt.figure(figsize=(7, 10))
        plt.title('Количество заявок')
        report = sns.heatmap(bid.pivot_table(index='month_bid', values='data_bid', columns=['year_bid'],
                                             aggfunc='count'),
                             annot=True, cbar=False, fmt='.1f', cmap="BuPu", linewidths=2, linecolor='gray')
        report = self.get_str_report(report.figure)
        print('report done')
        return report


# my_report = HeatmapReport()
# print(my_report.get_deal_report())
