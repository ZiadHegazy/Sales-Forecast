from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import CreateUpdateForecast, AvailableQuarters, GetHistory, UpdateForecastList, Login

urlpatterns = [
    path("forecast",CreateUpdateForecast.as_view(),name="create"),
    path("updateForecastList",UpdateForecastList.as_view(),name="updateList"),
    path("getAvailableQuarters",AvailableQuarters.as_view(),name="quarters"),
    path("getHistory",GetHistory.as_view(),name="history"),
    path("login",Login.as_view(),name="login"),
    path("refreshToken",TokenRefreshView.as_view(),name="refreshToken")
]
