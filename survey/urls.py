from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import SurveyViewSet

# Router register.
router = DefaultRouter()
router.register('surveys', SurveyViewSet, basename='surveys')
# router.register('answers', AnswerViewSet, basename='answers')

urlpatterns = [
    path('', include(router.urls)),
]