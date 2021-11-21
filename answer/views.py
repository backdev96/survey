from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.response import Response

from question.models import Question

from .models import Answer
from .serializers import AnswerSerializer


class AnswerViewSet(viewsets.ModelViewSet):
    serializer_class = AnswerSerializer

    def get_queryset(self, *args, **kwargs):
        question = get_object_or_404(Question, pk=self.kwargs.get('question_id'),
                                     survey__id=self.kwargs.get("survey_id"))
        queryset = question.answer_question.all()
        return queryset

    @swagger_auto_schema(
        operation_summary='Delete answer',
    )
    def destroy(self, request, *args, **kwargs):
        instance = get_object_or_404(Answer, pk=self.kwargs.get('pk'))
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        operation_summary='Create answer',
        request_body=AnswerSerializer,
        responses={201: AnswerSerializer()},
    )
    def perform_create(self, request, *args, **kwargs):
        question = get_object_or_404(Question, pk=self.kwargs.get('question_id'),
                                     survey__id=self.kwargs.get("survey_id"))
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save(respondent=self.request.user, question=question)
        response_serializer = AnswerSerializer(instance, context={"request": request})
        headers = self.get_success_headers(response_serializer.data)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED, headers=headers)
