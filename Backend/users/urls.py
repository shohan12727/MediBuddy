from django.urls import path 
from .views import * 

app_name = 'users'

urlpatterns = [
    path('register/',RegisterView.as_view(), name = 'register'),
    path('login/', LoginView.as_view(),name='login'),
    path('csrf/',csrf),
    path('current_users/',current_user),
    path('logout/',logout)
]
