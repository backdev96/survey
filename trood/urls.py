from django.contrib import admin
from django.urls import include, path
# from rest_framework.authtoken import views

from .yasg import urlpatterns as doc_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('surveys/', include('survey.urls')),
    path('questions/', include('question.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]

urlpatterns += doc_urls
