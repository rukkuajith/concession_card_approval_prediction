from django.urls import path

from home import views


urlpatterns = [
    path('', views.home, name="home"),
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('home/login/',views.login, name='home/login'),
    path('home/login/login/',views.application, name='home/login/login'),
    path('login/application/',views.application, name='login/application'),
    path('application/',views.application,name='application')
]