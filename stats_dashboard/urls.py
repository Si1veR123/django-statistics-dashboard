from django.urls import path
from . views import *


urlpatterns = [
    path("", stats_dashboard),
    path("activity/", activity),
    path("config/", config),
    path("charts/", all_charts),
]
