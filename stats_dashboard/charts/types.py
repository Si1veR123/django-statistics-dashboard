import typing
from .dataset import ChartDataset


class Chart:
    def __init__(
                self,
                name: str = "",
                labels: list = None,
                datasets: typing.List[ChartDataset] = None,
                options: dict = None,
                include_zero: bool = False
            ):

        self.name = name
        self.type = ""
        self.include_zero = include_zero

        if labels is None:
            labels = []
        self.labels = labels

        if include_zero:
            self.labels.insert(0, 0)

        if datasets is None:
            datasets = []
        self.datasets = datasets

        if not options:
            self.options = {}
        else:
            self.options = options

        legend_options = self.options.get("legend")
        if legend_options:
            try:
                legend_options["display"] = False
            except:
                pass
        else:
            self.options["legend"] = {"display": False}

    def get_json_data(self):
        json_data = {
            "data": {
                "labels": self.labels,
                "datasets": [dataset.get_format(self.include_zero) for dataset in self.datasets]
            },
            "options": self.options,
            "type": self.type,
            "name": self.name
        }

        return json_data


class BarChart(Chart):
    def __init__(
                self,
                name: str = "",
                labels: list = None,
                datasets: typing.List[ChartDataset] = None,
                options: dict = None,
                include_zero: bool = False
            ):

        super().__init__(name, labels, datasets, options, include_zero)
        self.type = "bar"


class LineChart(Chart):
    def __init__(
                self,
                name: str = "",
                labels: list = None,
                datasets: typing.List[ChartDataset] = None,
                options: dict = None,
                include_zero: bool = False,
                time_unit: str = None
            ):

        super().__init__(name, labels, datasets, options, include_zero)
        self.type = "line"
        self.time_unit = time_unit

        if time_unit is None:
            return

        try:
            self.options["scales"]
        except KeyError:
            self.options["scales"] = {}

        try:
            self.options["scales"]["xAxes"]
        except KeyError:
            self.options["scales"]["xAxes"] = []

        self.options["scales"]["xAxes"] = self.options["scales"]["xAxes"] + [{"type": "time", "time": {"unit": self.time_unit}}]


class PieChart(Chart):
    def __init__(
                self,
                name: str = "",
                labels: list = None,
                datasets: typing.List[ChartDataset] = None,
                options: dict = None,
                include_zero: bool = False,
            ):

        super().__init__(name, labels, datasets, options, include_zero)
        self.type = "pie"


class ScatterChart(Chart):
    def __init__(
                self,
                name: str = "",
                labels: list = None,
                datasets: typing.List[ChartDataset] = None,
                options: dict = None,
                include_zero: bool = False,
            ):

        super().__init__(name, labels, datasets, options, include_zero)
        self.type = "scatter"

