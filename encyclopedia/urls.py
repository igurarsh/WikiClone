from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.title_pag, name="title_page"),
    path("newpage",views.new_page,name="new_page"),
    path("edit/<str:title>",views.edit_page,name="edit_page"),
    path("random",views.any_page,name="random_page")
]
