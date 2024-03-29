from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.response import Response
from survey.models import Survey

from .models import Question
from .serializers import QuestionCreateSerializer, QuestionSerializer


class QuestionViewSet(viewsets.ModelViewSet):

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return QuestionSerializer
        return QuestionCreateSerializer

    def get_queryset(self, *args, **kwargs):
        survey = get_object_or_404(Survey, pk=self.kwargs.get('survey_id'))
        return survey.questions.all()

    @swagger_auto_schema(
        operation_summary='Get list of questions',
    )
    def list(self, request, *args, **kwargs):
        return super(QuestionViewSet, self).list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='Get question',
    )
    def retrieve(self, request, *args, **kwargs):
        return super(QuestionViewSet, self).retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='Delete question',
    )
    def destroy(self, request, *args, **kwargs):
        instance = get_object_or_404(Question, pk=self.kwargs.get('pk'))
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        operation_summary='Create Question',
        request_body=QuestionCreateSerializer,
        responses={201: QuestionSerializer()},
    )
    def create(self, request, *args, **kwargs):
        survey = get_object_or_404(Survey, pk=self.kwargs.get('survey_id'))
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save(author=self.request.user, survey=survey)
        response_serializer = QuestionCreateSerializer(instance)
        headers = self.get_success_headers(response_serializer.data)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @swagger_auto_schema(
        operation_summary='Update question',
        request_body=QuestionCreateSerializer,
        responses={200: QuestionCreateSerializer()},
    )
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance: Question = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        response = QuestionCreateSerializer(instance, context=self.get_serializer_context()).data
        return Response(response)

    @swagger_auto_schema(
        operation_summary='Patch question',
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
