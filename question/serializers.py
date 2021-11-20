from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers

from survey.models import Survey, User

from .models import Answer, Question


# Question Serializers.
class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'text')
        model = Question


class QuestionCreateSerializer(QuestionSerializer):
    class Meta(QuestionSerializer.Meta):
        fields = ('correct_answer', ) + QuestionSerializer.Meta.fields


class QuestionCreateWithSurveySerializer(QuestionCreateSerializer):
    class Meta(QuestionCreateSerializer.Meta):
        fields = ('survey', 'author') + QuestionCreateSerializer.Meta.fields
        read_only_fields = ('author',)

    survey = serializers.PrimaryKeyRelatedField(
            many=False,
            queryset=Survey.objects.all()
        )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )


# Answer Serializers.
class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = (
            'answer',
        )

    def validate(self, attrs):
        request = self.context.get('request')
        question = self.context['question']

        respondent = request.user
        attrs['question'] = question
        attrs['respondent'] = respondent
        return attrs


class ResponseAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = (
            'answer',
            'creation_date',
            'correct'
        )

    answer = serializers.SerializerMethodField()
    correct = serializers.SerializerMethodField()

    def get_answer(self, obj):
        request = self.context.get('request')
        respondent = request.user
        answer = Answer.objects.get(question=obj, respondent=respondent)
        return AnswerSerializer(answer).data

    def get_correct(self, obj):
        request = self.context.get('request')
        respondent = request.user
        answer = Answer.objects.get(question=obj, respondent=respondent)
        correct = answer.correct
        return correct

