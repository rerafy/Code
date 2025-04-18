from django.urls import path
from . import views
from .views import get_onedrive_files

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('SCAnalysis/', views.diagram_view, name='diagram'),
    path('fault-analysis/', views.fault_analysis_view, name='fault_analysis'),
    path('Title_Box/', views.fault_analysis_view, name='Title_Box'),
    path("onedrive/", get_onedrive_files),
]


