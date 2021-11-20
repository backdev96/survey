from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
# from .permissions import OwnerOrReadOnly
from rest_framework.decorators import action
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin, RetrieveModelMixin,
                                   UpdateModelMixin)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import Question, User
from .serializers import (AnswerSerializer, QuestionCreateWithSurveySerializer,
                          QuestionSerializer, ResponseAnswerSerializer)


class QuestionViewSet(
    GenericViewSet,
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin
):
    queryset = Question.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return QuestionSerializer
        return QuestionCreateWithSurveySerializer

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
        request_body=QuestionCreateWithSurveySerializer,
        responses={201: QuestionSerializer()},
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save(author=self.request.user)
        response_serializer = QuestionCreateWithSurveySerializer(instance)
        headers = self.get_success_headers(response_serializer.data)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @swagger_auto_schema(
        operation_summary='Update question',
        request_body=QuestionCreateWithSurveySerializer,
        responses={200: QuestionCreateWithSurveySerializer()},
    )
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance: Question = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        response = QuestionCreateWithSurveySerializer(instance, context=self.get_serializer_context()).data
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response(response)

    @swagger_auto_schema(
        operation_summary='Patch question',
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        methods=['POST'],
        operation_summary='Answer question',
        request_body=AnswerSerializer,
        responses={200: ResponseAnswerSerializer()},
    )
    @action(detail=True, methods=['POST'])
    def answer(self, request, *args, **kwargs):
        question: Question = self.get_object()

        context = {
            **self.get_serializer_context(),
            'question': question,

        }

        serializer = AnswerSerializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(ResponseAnswerSerializer(question, context=context).data)
