from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('vlog', views.vlog_view, name= 'vlog'),
    path('aboutus', views.aboutus, name= 'aboutus')
]
