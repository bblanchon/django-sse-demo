from django.urls import path
from clock.views import clock_view

urlpatterns = [
    path('', clock_view),
]
