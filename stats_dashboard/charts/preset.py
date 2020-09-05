from .types import LineChart, PieChart, BarChart
from .dataset import ChartDataset
from stats_dashboard.models import BrowserSession, PageSession
import datetime, calendar


class InvalidChartType(Exception):
    pass


def visits_time(visit_time=15768000, scale="month", style=None) -> LineChart:
    """
    load the 'visits over time' line chart, which displays
    browser sessions over a set period of time to a set scale
    """

    allowed_scales = ("year", "month", "week", "day", "hour", "minute")

    if scale not in allowed_scales[:-1]:
        raise Exception("Invalid time scale. Should be in ", str(allowed_scales[:-1]))

    if visit_time != 0:
        # get the start time for the graph from the chart visit time
        first_time = datetime.datetime.today() - datetime.timedelta(seconds=visit_time)

        # set the time to the start of its scale e.g. if scale is month, reset day to 1
        if scale == "month":
            time_replacement_kwargs = {"day": 1}
        else:
            time_replacement_kwargs = {allowed_scales[allowed_scales.index(scale) + 1]: 1}

        first_time = first_time.replace(tzinfo=datetime.timezone.utc, **time_replacement_kwargs)

    else:
        # if it is 0, get all visits
        first_time = datetime.datetime.fromtimestamp(0)

    # filter the browser session to greater than the start time
    visits_time_queryset = BrowserSession.objects.filter(start_time__gte=first_time)
    # get each record's start time
    x_unfiltered = [time["start_time"] for time in visits_time_queryset.values("start_time")]

    # y and x axis values, populated later
    y = []
    x = []

    # current time is used to create the x axis scale. starts at the first time
    current_time = first_time

    # if seeing all visits, set the current time to the earliest browser session
    if visit_time == 0:
        earliest_visit = datetime.datetime.now(datetime.timezone.utc)
        for visit in x_unfiltered:
            if visit < earliest_visit:
                earliest_visit = visit
        current_time = earliest_visit

    # this loop adds times to the x axis values from start time to now, in intervals of the set scale
    while datetime.datetime.now(datetime.timezone.utc) >= current_time:
        x.append(current_time)
        if scale == "month":
            # add number of days in current month
            current_time += datetime.timedelta(days=calendar.monthrange(current_time.year, current_time.month)[1])
        elif scale == "year":
            # add number of days in current year
            current_time += datetime.timedelta(days=366 if calendar.isleap(current_time.year) else 365)
        else:
            # add 1 of the set scale, e.g. if scale is week, kwargs is weeks=1
            time_add_kwargs = {scale + "s": 1}
            current_time += datetime.timedelta(**time_add_kwargs)
    x.append(current_time)

    # for each time interval check each browser session and create a count of sessions in that interval
    for label in x:
        count = 0
        for date in x_unfiltered:
            if label.year == date.year:
                if scale == "year":
                    count += 1
                    continue

                # check week without month as weeks can overlap months
                if label.isocalendar()[1] == date.isocalendar()[1]:
                    if scale == "week":
                        count += 1
                        continue

                if label.month == date.month:
                    if scale == "month":
                        count += 1
                        continue
                    if label.day == date.day:
                        if scale == "day":
                            count += 1
                            continue
                        if label.hour == date.hour:
                            if scale == "hour":
                                count += 1
                                continue

        y.append(count)

    visits_time_chart = LineChart(
        name="Visits over time" + " ({})".format(scale),
        labels=x,
        datasets=[ChartDataset(y, style)],
        time_unit=scale
    )

    return visits_time_chart


def browser_share(style=None, type="pie"):

    browser_count = {"Other/Unknown": 0}

    browsers = [b["browser"] for b in BrowserSession.objects.all().values("browser")]

    for browser in browsers:
        if browser is None or browser == "":
            browser_count["Other/Unknown"] += 1
            continue

        if browser not in browser_count.keys():
            browser_count[browser] = 0
        browser_count[browser] += 1

    x = list(browser_count.keys())
    y = list(browser_count.values())

    if type == "pie":
        ChosenChart = PieChart
    elif type == "bar":
        ChosenChart = BarChart
    else:
        raise InvalidChartType

    browser_share_chart = ChosenChart(
        name="Browser Share",
        labels=x,
        datasets=[
            ChartDataset(y, style),
        ]
    )

    return browser_share_chart


def device_share(style=None, type="pie"):

    device_count = {"Other/Unknown": 0}

    devices = [b["device"] for b in BrowserSession.objects.all().values("device")]

    for device in devices:
        if device is None or device == "":
            device_count["Other/Unknown"] += 1
            continue

        if device not in device_count.keys():
            device_count[device] = 0
        device_count[device] += 1

    x = list(device_count.keys())
    y = list(device_count.values())

    if type == "pie":
        ChosenChart = PieChart
    elif type == "bar":
        ChosenChart = BarChart
    else:
        raise InvalidChartType

    device_share_chart = ChosenChart(
        name="Device Share",
        labels=x,
        datasets=[
            ChartDataset(y, style),
        ]
    )

    return device_share_chart


def common_pages(style=None):
    all_pages = PageSession.objects.all()

    all_urls = [page["page"] for page in all_pages.values("page")]

    page_count = {}

    for url in all_urls:
        if url not in page_count.keys():
            page_count[url] = 0
        page_count[url] += 1

    common_pages_chart = BarChart(
        name="Common Pages",
        labels=list(page_count.keys()),
        datasets=[
            ChartDataset(list(page_count.values()), style)
        ],
        options={
            "scales": {
                "yAxes": [{
                    "ticks": {
                        "stepSize": 1
                    }
                }]
            }
        }
    )

    return common_pages_chart
