from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:civilzation_id>/', views.civilization, name='civilization'),
    #path('newproject/<int:civilzation_id>/', views.civilization, name='new_project'),
]