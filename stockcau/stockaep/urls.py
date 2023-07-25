from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name='index'),
    path('create', views.add_inventary, name='create'),
    path('create/trade', views.mi_vista, name='create-trade'),
    path('login', views.login,name='login'),
    path("register", views.register, name='register'),
    path('logout', views.logout, name='logout')
]