from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers

from survey.models import Survey, User

from .models import Answer, Question


# Answer Serializers.
class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = (
            'id',
            'answer',
            'respondent',
            'question'
            # 'respondent',
        )
    question = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )
    respondent = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    def validate(self, data):
        '''Call the instance's validate() method and
        raise error if user has already added a review for this tittle.
        '''
        question_id = self.context.get('request').parser_context['kwargs']['question_id']
        if (Answer.objects.filter(question_id=question_id, respondent=self.context['request'].user).exists()
            and self.context['request'].method == 'POST'):
            raise serializers.ValidationError('This user has already added answer for this question')
        return data

class ResponseAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = (
            'answer',
            'answered_at',
            'correct'
        )
    
    # answer = serializers.SerializerMethodField()
    correct = serializers.SerializerMethodField()

    # def get_answer(self, obj):
    #     request = self.context.get('request')
    #     respondent = self.request.user
    #     answer = Answer.objects.get(question=obj, respondent=respondent)
    #     return AnswerSerializer(answer).data

    def get_correct(self, obj):
        # request = self.context.get('request')
        # respondent = request.user
        # answer = Answer.objects.get(question=obj, respondent=respondent)
        # correct = answer.correct
        return obj.correct

