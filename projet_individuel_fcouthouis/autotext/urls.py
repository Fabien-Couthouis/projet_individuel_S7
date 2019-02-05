from django.urls import path

from . import views

app_name = 'autotext'
urlpatterns = [
    path('', views.index, name='index'),
]
