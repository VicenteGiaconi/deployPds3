from django.urls import path
from . import views

urlpatterns = [
    path("", views.home.as_view()),
    path("logout", views.logout_view.as_view()),
    path("controller", views.controller_view.as_view(), name='controller'),
    path("casillero/<int:id>", views.casillero_view.as_view(), name='casillero'),
    path("casillero/<int:id>/edit", views.casillero_edit.as_view(), name='casillero_edit')
]