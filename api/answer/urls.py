from django.urls import include, path
from rest_framework.routers import DefaultRouter

from answer.views import AnswerViewSet


router = DefaultRouter()
router.register('answers', AnswerViewSet, basename='answers')

urlpatterns = [
    path('', include(router.urls)),
]
