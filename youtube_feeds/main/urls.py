from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login-register', views.login_register, name='login_register'),
    path('logout', views.logout_view, name='logout'),
    path('share', views.share, name='share'),
    path('do-share', views.do_share, name='do_share'),
]
