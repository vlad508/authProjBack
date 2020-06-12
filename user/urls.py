from django.urls import path

from user import views

urlpatterns = [
    path('account/social/', views.auth_social_view),
    path('account/register/', views.register_new_user),
    path('account/login/', views.login),
    path('', views.home_page)
]
