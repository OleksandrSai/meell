from django.contrib import admin
from django.urls import path
from . import views

app_name = "shop"

urlpatterns = [
    path("", views.main_page_view, name="main_page"),
    path("weading-dresses/", views.wedding_dress_view, name="weading-dresses"),
    path("evening-dresses/", views.evening_dress_view, name="evening-dresses"),
]
