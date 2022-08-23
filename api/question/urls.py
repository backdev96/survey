from django.urls import include, path
from question.views import QuestionViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('answers', QuestionViewSet, basename='answers')

urlpatterns = [
    path('', include(router.urls)),
]
