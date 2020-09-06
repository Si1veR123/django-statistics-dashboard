# Django Stat Dashboard

A dashboard to display captured metrics and charts, such as devices, pages visited, 
and page actions. Staff user is required to get chart data and view dashboard. Dashboard is at
/(statsurl), usually /stats.

## Setup

1. Add `'stats_dashboard'` to INSTALLED_APPS in settings.py.  
    ```python
    INSTALLED_APPS = [
        ...,
       "stats_dashboard",
    ]
    ```

2. Add `'stats_dashboard.middleware.stat_middleware.StatMiddleware'` to MIDDLEWARE in settings.py.
    ```python
    MIDDLEWARE = [
       ...,
       "stats_dashboard.middleware.stat_middleware.StatMiddleware"
    ]
    ```

3. *Optional:* Configurate the elements to listen for clicks in settings.py.
    ```python
    STATS_PAGE_CONFIG = {
        "*": {
            "click": [
                {"selector": "button", "name": "this is name"}
            ],
        }
    }
    ```
   "*" is a regex expression for the page to listen for this click. There can be multiple pages.  
   "click" specifies the event. Currently only click events are available.  
   "selector" is the CSS selector for the element to listen to clicks on  
   "name" is the name that the event is saved as

4. *Optional:* To use custom charts, create a python file, (commonly chart.py)
    and set it in settings.py.
    ```python
    STATS_CHART_LOCATION = "yourproject.chart"
    ```
   This file specifies all of the charts to show on the dashboard. 
   More documentation [here](#making-charts).

5. On pages that you wish to be tracked, add the JavaScript file. Note that axios, a JS library is loaded
   to send requests to the server on activity (from this script). You can put this in your base template.
   ```html
   {% load static %}
   
   <body>
       <script src="{% static 'stats/stats.js' %}"></script>
   </body>
    ```

6. Add the urls in urls.py
    ```python
    import stats_dashboard.urls
    urlpatterns = [
       path("stats/", include(stats_dashboard.urls)),
    ]
    ```
   It is recommended to use stats/ as the url as by default, 
   recorded activity is sent here from the JavaScript file.
   If you wish to use another url, specify the data-root attribute on the 
   script tag e.g.  
   `<script data-root="/otherurl/" src="{% static 'stats/stats.js' %}"></script>`

## Making Charts
The charts classes and functions are at `stats_dashboard.charts`.  
Go to /yourstaturl/charts/ to get charts data for troubleshooting.  
The flow for creating charts is:
1. Import the chart manager, at  
    ```
    from stats_dashboard.charts.manager import statistic_charts
    ```
2. Import your chart type  
    ```
    from stats_dashboard.charts.types import LineChart, ScatterChart, BarChart, PieChart
    ```
3. Import the chart dataset class and  
    ```
    from stats_dashboard.charts.dataset import ChartDataset
    ```  

4. *Optional:* Import dataset style class (to add custom styles on datasets)  
    ```
    from stats_dashboard.charts.dataset_styles import DatasetStyle
    ```  
    Create your dataset styles:
    ```python
    my_blue_style = DatasetStyle(background_color="blue")
    ```
   Styles are based off of chart.js styles, however JavaScript names are changed to Python
   names e.g. `backgroundColor -> background_color`. 
   [Styles](https://www.chartjs.org/docs/latest/charts/line.html#dataset-properties)
   are here. Some chart specific styles may be found on the documentation for other charts.

5. Create your datasets:
    ```python
    my_dataset = ChartDataset(values=[10, 20, 30], style=my_blue_style)
    my_second_dataset = ChartDataset(values=[20, 30, 35])
    ```
   Default style is used if not otherwise specified. 
   Values should be calculated from your own data.
   This file is run on each request to the chart dashboard, do that the data can be retrieved
   from models.  
   For scatter graphs, data should be set in this format, with ScatterDataset:
   ```python
    ScatterDataset(values=[
           {"x": 1, "y": 3},
           {"x": 2, "y": 4},
           {"x": 3, "y": 5}
       ], 
       style=scatter_style
    )
    ```
6. Create your chart object from the datasets.
    ```python
    my_bar_chart = BarChart(
       name="My Bar Chart",
       labels=["1st Bar", "2nd Bar", "3rd Bar"],
       datasets=[
           my_dataset,
           my_second_dataset
       ]   
    )
    ```
   There should be as many labels as values in each dataset.  
   Labels: X Axis  
   Dataset Values: Y Axis  
   (Except in Pie Charts, and Scatter Charts)  
   In Scatter Charts, the dataset values contain X and Y values, so the labels
   argument shouldn't be set.

7. Add the chart to your dashboard
    ```python
    statistic_charts.add_chart(my_bar_chart)
    ```

## Preset Charts
There are some pre-made charts at `from stats_dashboard.charts.preset import *`  
They all take an optional style object.  
Some examples are `visits_time`, displaying visitors to the site, over time.  
This takes the number of seconds to look back for visitors, and a scale e.g. month.  
Another is `common_pages`, abar chart showing most visited pages.

### Use
```python
statistic_charts.add_chart(visits_time(58400, "hour", style=my_style))
statistic_charts.add_chart(browser_share(type="pie"))
```

### Other Info
3 Models, BroswerSession, PageSession and PageEvent is available at stats_dashboard.models.
These can be used to retrieve tracked user activity.

Please report any issues!
