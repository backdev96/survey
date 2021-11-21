from django.core.exceptions import ValidationError
from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers

from question.models import Question
from question.serializers import QuestionCreateSerializer

from .models import Survey, User


# Survey Serializers !!!!
class SurveyListSerializer(serializers.ModelSerializer):
    '''Survey list serializer shows short info about all surveys'''
    class Meta:
        fields = (
            'id',
            'name',
            'description',
        )
        model = Survey



class SurveyCreateSerializer(SurveyListSerializer):
    '''Survey create serializer shows full picture of survey'''

    class Meta(SurveyListSerializer.Meta):
        fields = ('questions', 'author') + SurveyListSerializer.Meta.fields
        read_only_fields = ('author',)

    questions = QuestionCreateSerializer(many=True)
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    def validate_questions(self, value):
        # Validate similar questions in one survey
        if (
            self.context['request']._request.method == 'POST'
            or self.context['request']._request.method == 'PUT'
            or self.context['request']._request.method == 'PATCH'
        ):

            list_of_quest_text = []
            for question in value:
                list_of_quest_text.append(question['text'])
            unique_question_text = set(list_of_quest_text)

            if len(unique_question_text) != len(value):
                raise ValidationError(
                    'Question with this text already exists in this survey.'
                )
        return value

    def create(self, validated_data):
        # As I have nested serializer I have to rewrite create method

        author_data = validated_data.pop('author')
        questions_data = validated_data.pop('questions')
        survey = Survey.objects.create(author=author_data, **validated_data)
        for question_data in questions_data:
            Question.objects.create(survey=survey, author=author_data, **question_data)

        return survey

    def update(self, instance: Survey, validated_data):
        # As I have nested serializer I have to rewrite update method

        questions_data = validated_data.pop('questions')
        questions = instance.questions.all()
        questions = list(questions)
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get(
                                                  'description',
                                                  instance.description
                                                 )
        instance.save()

        request = self.context.get('request')
        author = request.user
        for question_data in questions_data:
            question = questions.pop(0)
            question.text = question_data.get('text', question.text)
            question.correct_answer = question_data.get(
                                                      'correct_answer',
                                                      question.correct_answer
                                                     )
            question.survey = instance
            question.author = author
            question.save()

        return instance
