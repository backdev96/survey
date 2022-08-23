from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin, RetrieveModelMixin,
                                   UpdateModelMixin)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from .models import Survey
from .permissions import OwnerOrReadOnly
from .serializers import SurveyCreateSerializer, SurveyListSerializer


class SurveyViewSet(
    GenericViewSet,
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
):
    queryset = Survey.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, OwnerOrReadOnly,)

    def get_serializer_class(self):
        if self.action == "list":
            return SurveyListSerializer
        return SurveyCreateSerializer

    @swagger_auto_schema(
        operation_summary="Get list of surveys",
    )
    def list(self, request, *args, **kwargs):
        return super(SurveyViewSet, self).list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Get Survey",
    )
    def retrieve(self, request, *args, **kwargs):
        return super(SurveyViewSet, self).retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete Survey",
    )
    def destroy(self, request, *args, **kwargs):
        instance = get_object_or_404(Survey, pk=self.kwargs.get("pk"))
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        operation_summary="Create Survey",
        request_body=SurveyCreateSerializer(),
        responses={201: SurveyCreateSerializer()},
    )
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            instance: Survey = serializer.save(author=self.request.user)
        except ValueError as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

        response_serializer = SurveyCreateSerializer(instance, context={"request": request})
        headers = self.get_success_headers(response_serializer.data)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @swagger_auto_schema(
        operation_summary="Update survey",
        request_body=SurveyCreateSerializer,
        responses={200: SurveyCreateSerializer()},
    )
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance: Survey = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save(author=self.request.user)
        response = SurveyCreateSerializer(instance, context=self.get_serializer_context()).data
        if getattr(instance, "_prefetched_objects_cache", None):
            instance._prefetched_objects_cache = {}
        return Response(response)

    @swagger_auto_schema(
        operation_summary="Patch survey",
    )
    def partial_update(self, request, *args, **kwargs):
        # Partial update calls update internally, so there"s no need to manually redefine the logic
        return super().partial_update(request, *args, **kwargs)
