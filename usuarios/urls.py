from django.urls import path
from .views import LoginView, RegistroView,logout_view

app_name='usuarios'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('registro/', RegistroView.as_view(), name='registro'),
    path('logout/', logout_view, name='logout'),
]
