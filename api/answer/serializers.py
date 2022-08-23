from rest_framework import serializers

from .models import Answer


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = (
            'id',
            'answer',
            'respondent',
            'question'
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
        '''
        Call the instance's validate() method and
        raise error if user has already added an answer for this question.
        '''
        question_id = self.context.get('request').parser_context['kwargs']['question_id']
        if (Answer.objects.filter(question_id=question_id, respondent=self.context['request'].user).exists()
                and self.context['request'].method == 'POST'):
            raise serializers.ValidationError('This user has already added answer for this question')
        return data
