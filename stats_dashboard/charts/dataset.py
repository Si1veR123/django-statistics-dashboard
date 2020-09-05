from .dataset_styles import site_default_style


class ChartDataset:
    def __init__(self, values=None, style=None):
        if values is None:
            values = []

        if style is None:
            style = site_default_style

        self.values = values
        self.style = style

    def get_format(self, include_zero):
        values = [0] + self.values if include_zero else self.values
        return {**{"data": values}, **self.style.get_dictionary()}


class ScatterDataset(ChartDataset):
    def get_format(self, include_zero):
        values = [{"x": 0, "y": 0}] + self.values if include_zero else self.values
        return {**{"data": values}, **self.style.get_dictionary()}
