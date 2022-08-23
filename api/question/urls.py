from django.urls import include, path
from rest_framework.routers import DefaultRouter

from question.views import QuestionViewSet


router = DefaultRouter()
router.register('answers', QuestionViewSet, basename='answers')

urlpatterns = [
    path('', include(router.urls)),
]
