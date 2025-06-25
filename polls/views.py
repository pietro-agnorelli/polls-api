from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, ListAPIView, GenericAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from polls.filters import PollsFilter#, ChoicesFilter
from polls.models import Polls, Choices, Votes
from polls.permissions import IsCreatorOrReadOnly
from polls.serializers import PollsSerializer, ChoicesSerializer, CreatePollsSerializer, VotesSerializer


# Create your views here.

class CreatePollView(CreateAPIView):
    serializer_class = CreatePollsSerializer
    queryset = Polls.objects.all()
    permission_classes = [IsAuthenticated]

class ListPollsView(ListAPIView):
    serializer_class = CreatePollsSerializer
    queryset = Polls.objects.all()
    filterset_class = PollsFilter

class VoteView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = VotesSerializer

    def post(self, request):
        serializer = VotesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            poll = Polls.objects.get(serializer.poll)
        except Polls.DoesNotExist:
            return Response({"error": "Poll not found"}, status=status.HTTP_404_NOT_FOUND)
        try:
            choice = Choices.objects.get(serializer.choice)
        except Choices.DoesNotExist:
            return Response({"error": "Choice not found"}, status=status.HTTP_404_NOT_FOUND)
        if not poll.is_active:
            return Response({"error": "Poll is not active"}, status=status.HTTP_400_BAD_REQUEST)
        if not choice.poll_id == poll.id:
            return Response({"error": "Choice does not belong to the poll"}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({"message": "Vote recorded successfully"}, status=status.HTTP_201_CREATED)

    def put(self, request):
        serializer = VotesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            vote = Votes.objects.get(poll=serializer.poll, user=request.user)
        except Votes.DoesNotExist:
            return Response({"error": "Vote not found"}, status=status.HTTP_404_NOT_FOUND)
        try:
            choice = Choices.objects.get(serializer.choice)
        except Choices.DoesNotExist:
            return Response({"error": "Choice not found"}, status=status.HTTP_404_NOT_FOUND)
        if not serializer.poll.is_active:
            return Response({"error": "Poll is not active"}, status=status.HTTP_400_BAD_REQUEST)
        if not choice.poll_id == serializer.poll.id:
            return Response({"error": "Choice does not belong to the poll"}, status=status.HTTP_400_BAD_REQUEST)
        # Update the vote
        vote.choice = serializer.choice
        vote.save()
        return Response({"message": "Vote updated successfully"}, status=status.HTTP_202_ACCEPTED)


class ResultsView(RetrieveAPIView):
    def retrieve(self, request, **kwargs):
        try:
            poll = Polls.objects.get(request.data.get('poll_id'))
        except Polls.DoesNotExist:
            return Response({"error": "Poll not found"}, status=status.HTTP_404_NOT_FOUND)
        if not poll.is_active:
            return Response({"error": "Poll is not active"}, status=status.HTTP_400_BAD_REQUEST)
        choices = Choices.objects.filter(poll=poll)
        results = {choice.choice_text: choice.votes.count() for choice in choices}
        return Response({"poll": poll.question, "results": results}, status=status.HTTP_200_OK)