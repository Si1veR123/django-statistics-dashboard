from .types import *


class ChartManager:
    """
    Stores all of the charts for this website
    """
    def __init__(self):
        self.charts = []

    def add_chart(self, chart: Chart):
        """append chart to list"""
        self.charts.append(chart)


statistic_charts = ChartManager()
