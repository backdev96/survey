from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken import views

from .yasg import urlpatterns as doc_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('survey/', include('survey.urls')),
    path('users/', include('users.urls')),
    path('question/', include('answer.urls')),
    path('answer/', include('question.urls')),
    path('api-token-auth/', views.obtain_auth_token),
]

urlpatterns += doc_urls
