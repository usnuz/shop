from django.urls import path
from .views import *


urlpatterns = [
    path('sign-up/', sign_up),
    path('login/', log_in),
    path('logout/', log_out),
]
