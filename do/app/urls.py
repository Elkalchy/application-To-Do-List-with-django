from django.urls import path
from . import views

urlpatterns = [
    path('', views.index,name='index'),
    path('login/', views.login_view,name='login'),
    path('logout/', views.logout_view,name='logout'),
    path('sign_up/', views.sign_up,name='sign_up'),

    path('ajouter/', views.ajouter,name='ajouter'),
    path('toggle_task/<int:task_id>/', views.toggle_task, name='toggle_task'),

]