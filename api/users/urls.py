from django.urls import path
from users.views import LoginAPIView, RegisterUserAPIView

path('login/', LoginAPIView.as_view()),

urlpatterns = [
    path('login/', LoginAPIView.as_view()),
    path('register/', RegisterUserAPIView.as_view()),
]
