from rest_framework import serializers
from .models import Polls


class PollsSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.username')

    class Meta:
        model = Polls
        fields = ['id', 'question', 'pub_date', 'is_active', 'creator']