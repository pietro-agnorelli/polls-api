from rest_framework import serializers
from .models import Polls, Choices, Votes


class ChoicesSerializer(serializers.ModelSerializer):
    poll = serializers.PrimaryKeyRelatedField(queryset=Polls.objects.all())
    class Meta:
        model = Choices
        fields = ['id',  'choice_text', 'poll']


class PollsChoicesSerializer(serializers.ModelSerializer):
    choices = ChoicesSerializer(many=True, required=False)
    creator = serializers.ReadOnlyField(source='creator.username')

    class Meta:
        model = Polls
        fields = ['id', 'question', 'pub_date', 'is_active', 'creator', 'choices']
        read_only_fields = ['pub_date', 'creator']

    def validate(self, attrs):
        attrs['creator'] = self.context['request'].user
        return attrs

    def create(self, validated_data):
        choices_data = validated_data.pop('choices', [])
        poll = Polls.objects.create(**validated_data)
        for choice_data in choices_data:
            Choices.objects.create(poll=poll, **choice_data)
        return poll

    def update(self, instance, validated_data):
        choices_data = self.context['request'].data.get('choices', [])
        instance = super().update(instance, validated_data)

        if choices_data:
            instance.choices.all().delete()
            for choice_data in choices_data:
                Choices.objects.create(poll=instance, **choice_data)

        return instance


class VotesSerializer(serializers.ModelSerializer):
    poll = serializers.PrimaryKeyRelatedField(queryset=Polls.objects.all())
    choice = serializers.PrimaryKeyRelatedField(queryset=Choices.objects.all())
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Votes
        fields = ['id', 'poll', 'choice', 'user']

    def validate(self, attrs):
        attrs['user'] = self.context['request'].user
        return attrs