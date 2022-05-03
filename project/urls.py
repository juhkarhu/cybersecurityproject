from django.urls import path

from . import views

app_name = 'project'
urlpatterns = [
    path('', views.index, name='index'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('add_new_post/', views.add_new_post, name='add_new_post'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
]