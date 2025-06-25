from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated

from polls.filters import PollsFilter
from polls.models import Polls
from polls.permissions import IsCreator
from polls.serializers import PollsSerializer


# Create your views here.

class CreatePollView(CreateAPIView):
    serializer_class = PollsSerializer  # Replace with your serializer class
    queryset = Polls.objects.all()  # Replace with your queryset
    permission_classes = [IsAuthenticated, IsCreator]# Replace with your permission classes if needed


class PollListView(ListAPIView):
    serializer_class = PollsSerializer  # Replace with your serializer class
    queryset = Polls.objects.all()  # Replace with your queryset
    filterset_class = PollsFilter  # Replace with your filterset class if needed