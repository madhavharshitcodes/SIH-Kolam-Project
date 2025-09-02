from django.urls import path
from . import views

urlpatterns = [
    # This maps the root URL ('/') to our index view
    path('', views.index, name='index'),
]
