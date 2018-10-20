from django.urls import path
from django.conf.urls import url
from django.conf import settings

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('summoner', views.summoner, name="summoner"),
    path('initialize', views.initialize, name="intialize"),
    #path('gains', views.gains, name='gains'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', views.logout_view, name="logout"),
]