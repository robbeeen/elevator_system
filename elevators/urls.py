
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
urlpatterns = [
    path('create/', views.CreateElevators.as_view(), name="CreateElevators"),
]
routes = DefaultRouter()
routes.register('data', views.ElevatorsController, basename="data")
urlpatterns = routes.urls + urlpatterns
