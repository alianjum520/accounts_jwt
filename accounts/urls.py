from django.urls import path
from .views import *


urlpatterns = [

    path('register/',RegisterUser.as_view()),
    path('login/',LoginAPIView.as_view()),
    path('login/logout/',LogoutAPIView.as_view()),
    path('login/users/',ViewUser.as_view())

]