from rest_framework import serializers

from .models import Question


# Question Serializers.
class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'text')
        model = Question


class QuestionCreateSerializer(QuestionSerializer):
    class Meta(QuestionSerializer.Meta):
        fields = ('correct_answer', 'survey', 'author') + QuestionSerializer.Meta.fields
        read_only_fields = ('author',)

    survey = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
