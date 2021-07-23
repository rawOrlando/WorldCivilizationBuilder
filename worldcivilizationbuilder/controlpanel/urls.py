from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:civilzation_id>/', views.civilization, name='civilization'),
    path('details/<int:civilzation_id>/', views.civilization_details, name='civilization_details'),
    #path('newproject/<int:civilzation_id>/', views.civilization, name='new_project'),
]