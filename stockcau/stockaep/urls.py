from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name='index'),
    path('create', views.add_inventary, name='create'),
    path('reload', views.reload, name='reload'),
    path('login', views.login,name='login'),
    path("register", views.register, name='register'),
    path('logout', views.logout, name='logout'),
    path('delete/<str:id>', views.delete, name='delete'),
    path('edit/<str:id>', views.edit, name='edit'),
    path('test', views.test, name = 'test'),
    path('get-info', views.get_info, name='get-info'),
    path('notifications', views.notificaciones, name='notifications'),
    path('action', views.accion_notificacion, name='action')
]