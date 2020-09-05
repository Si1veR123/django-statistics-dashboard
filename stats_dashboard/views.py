from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from stats_dashboard.models import BrowserSession, PageSession, PageEvent
from stats_dashboard.charts.manager import statistic_charts
from django.conf import settings
import importlib
import json
import re


def stats_dashboard(request):
    if not request.user.is_staff:
        return HttpResponse(status=401)
    return render(request, "stats/index.html", {
        "browser_sessions": BrowserSession.objects,
        "page_session": PageSession.objects,
        "page_events": PageEvent.objects,
    })


@csrf_exempt
def activity(request: HttpRequest):
    """
    Any user activity is sent as a request here
    """
    if request.method != "POST":
        # only post requests are allowed
        # HTTP 405 is an invalid method
        response = HttpResponse(status=405)
        # set allow header to POST
        response["Allow"] = "POST"
        return response

    data = json.loads(request.body)

    # get all pages with a foreign key to the current browser session
    # stat session is added at middleware
    pages = request.stat_session.pagesession_set

    if data["type"] == "navigate":
        referer = request.META.get("Referer", None)
        # on a NEW navigation, create page session instance
        to = data["info"]

        create_first = False
        # get last viewed page session
        try:
            last_viewed = pages.get(last_viewed=True)
        except PageSession.DoesNotExist:
            create_first = True

        # check whether the new page is different to previous, else could be refresh
        if create_first or last_viewed.page != to:
            if not create_first:
                last_viewed.last_viewed = False
                last_viewed.save()
            new_page = PageSession.objects.create(
                page=to,
                browser_session=request.stat_session,
                referer=referer,
                last_viewed=True
            )

    elif data["type"] == "new_to_website":
        try:
            last_viewed = pages.filter(last_viewed=True)
            # once new to website is true, can't change back. stops against refresh overriding a true value to false
            if not last_viewed[0].new_to_website:
                last_viewed.update(new_to_website=data["info"])
        except:
            pass

    elif data["type"] == "click":
        try:
            PageEvent.objects.create(
                page_session=pages.get(last_viewed=True),
                type="click",
                info=data["info"],
            )
        except PageSession.DoesNotExist:
            pass

    return HttpResponse()


def config(request):
    """
    Returns the config for a given path, e.g. what to send to activity api
    """
    if request.method != "GET":
        # only get requests are allowed
        # HTTP 405 is an invalid method
        response = HttpResponse(status=405)
        # set allow header to GET
        response["Allow"] = "GET"
        return response

    path = request.GET["page"]

    config_for_path = {
        "click": [],
    }

    for re_path, configs in settings.STATS_PAGE_CONFIG.items():
        if re_path == "*" or re.match(re_path, path):
            for config_name, config_value in configs.items():
                config_for_path[config_name] = config_value

    return JsonResponse(config_for_path)


def all_charts(request: HttpRequest):
    if not request.user.is_staff:
        return JsonResponse([], safe=True)

    try:
        chart_file = importlib.import_module(settings.STATS_CHART_LOCATION)
    except ModuleNotFoundError:
        return JsonResponse([], safe=True)

    charts = statistic_charts.charts
    json_charts = []
    for chart in charts:
        json_charts.append(chart.get_json_data())

    return JsonResponse(json_charts, safe=False)
