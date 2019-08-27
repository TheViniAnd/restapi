from django.urls import path, include
from .views import indexViews

urlpatterns = [
    path('', indexViews)
]