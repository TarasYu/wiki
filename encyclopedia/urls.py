from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("new_page", views.new_page, name="NewPage"),
    path("saveEdited", views.save_edited, name="saveEdited"),
    path("edit/<str:title>", views.editEntry, name="edit"),
    path("save_page", views.new_page, name="noSave"),
    path("random_page", views.random_page, name="random_page"),
    path("<str:title>", views.article, name="article"),

  
]
