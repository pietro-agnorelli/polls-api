from rest_framework import serializers
from .models import Polls, Choices, Votes


class ChoicesSerializer(serializers.ModelSerializer):
    poll = serializers.PrimaryKeyRelatedField(queryset=Polls.objects.all())
    class Meta:
        model = Choices
        fields = ['id', 'poll', 'choice_text']


class PollsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Polls
        fields = ['id', 'question', 'pub_date', 'is_active', 'creator']
        read_only_fields = ['pub_date', 'creator']

class CreatePollsSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.username')
    choices = ChoicesSerializer(many=True, read_only=True)

    class Meta:
        model = Polls
        fields = ['id', 'question', 'is_active', 'creator', 'choices']

    def create(self, validated_data):
        choices_data = validated_data.pop('choices')
        poll = Polls.objects.create(**validated_data)
        for choice_data in choices_data:
            Choices.objects.create(poll=poll, **choice_data)
        return poll


class VotesSerializer(serializers.ModelSerializer):
    poll = serializers.PrimaryKeyRelatedField(queryset=Polls.objects.all())
    choice = serializers.PrimaryKeyRelatedField(queryset=Choices.objects.all())
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Votes
        fields = ['id', 'poll', 'choice', 'user']