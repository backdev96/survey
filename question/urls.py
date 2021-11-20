from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import QuestionViewSet

# Router register.
router = DefaultRouter()
# router.register('answers', AnswerViewSet, basename='answers')
router.register('questions', QuestionViewSet, basename='questions')


urlpatterns = [
    path('', include(router.urls)),
]
