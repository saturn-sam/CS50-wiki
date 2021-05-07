from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("edit/<str:title>", views.edit_wiki, name="edit-wiki"),
    path("create", views.create_wiki, name="create-wiki"),
    path("random/wiki/", views.random_page, name="random-page")
]
