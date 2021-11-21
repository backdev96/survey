from django.urls import include, path
from rest_framework.routers import DefaultRouter

from answer.views import AnswerViewSet
from question.views import QuestionViewSet

from .views import SurveyViewSet

router = DefaultRouter()
router.register('surveys', SurveyViewSet, basename='surveys')
router.register(
    r'surveys/(?P<survey_id>[0-9]+)/questions',
    QuestionViewSet, basename='questions'
)
router.register(
    r'surveys/(?P<survey_id>[0-9]+)/questions/(?P<question_id>[0-9]+)/answers',
    AnswerViewSet,
    basename='comments'
)

urlpatterns = [
    path('', include(router.urls)),
]
