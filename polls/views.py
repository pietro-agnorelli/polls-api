from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, GenericAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView, \
    ListCreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from polls.filters import PollsFilter#, ChoicesFilter
from polls.models import Polls, Choices, Votes
from polls.permissions import IsCreatorOrReadOnly
from polls.serializers import VotesSerializer, PollsChoicesSerializer, ChoicesSerializer


# Create your views here.

class ListCreatePollView(ListCreateAPIView):
    serializer_class = PollsChoicesSerializer
    queryset = Polls.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]


class DetailPollView(RetrieveUpdateDestroyAPIView):
    serializer_class = PollsChoicesSerializer
    queryset = Polls.objects.all()
    permission_classes = [IsCreatorOrReadOnly]
'''
class DetailPollsView(GenericAPIView):
    permission_classes = [IsCreatorOrReadOnly]

    def get(self, request, *args, **kwargs):
        try:
            poll = Polls.objects.get(id=kwargs['pk'])
        except Polls.DoesNotExist:
            return Response({"error": "Poll not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = PollsSerializer(poll)
        choices = Choices.objects.filter(poll=poll)
        choices_serializer = ChoicesSerializer(choices, many=True)
        response = {'poll': serializer.data, 'choices': choices_serializer.data}
        return Response(response, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        try:
            poll = Polls.objects.get(id=kwargs['pk'])
        except Polls.DoesNotExist:
            return Response({"error": "Poll not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ChoicesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(poll=kwargs['pk'])
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        try:
            poll = Polls.objects.get(id=kwargs['pk'])
        except Polls.DoesNotExist:
            return Response({"error": "Poll not found"}, status=status.HTTP_404_NOT_FOUND)
        try:
            choice = Choices.objects.get(id=request.data.get('id'), poll=poll)
        except Choices.DoesNotExist:
            return Response({"error": "Choice not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ChoicesSerializer(choice, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
'''

class VoteView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = VotesSerializer

    def post(self, request, pk):
        serializer = VotesSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        try:
            poll = Polls.objects.get(id=pk)
        except Polls.DoesNotExist:
            return Response({"error": "Poll not found"}, status=status.HTTP_404_NOT_FOUND)
        try:
            choice = Choices.objects.get(id=serializer.validated_data['choice'].id)
        except Choices.DoesNotExist:
            return Response({"error": "Choice not found"}, status=status.HTTP_404_NOT_FOUND)
        if not poll.is_active:
            return Response({"error": "Poll is not active"}, status=status.HTTP_400_BAD_REQUEST)
        if not choice.poll_id == poll.id:
            return Response({"error": "Choice does not belong to the poll"}, status=status.HTTP_400_BAD_REQUEST)
        existing_vote = Votes.objects.filter(poll=poll, user=request.user).first()
        if existing_vote:
            existing_vote.delete()
        serializer.save()
        return Response({"message": "Vote recorded successfully"}, status=status.HTTP_201_CREATED)




class ResultsView(RetrieveAPIView):
    def retrieve(self, request, **kwargs):
        try:
            poll = Polls.objects.get(id=kwargs['pk'])
        except Polls.DoesNotExist:
            return Response({"error": "Poll not found"}, status=status.HTTP_404_NOT_FOUND)
        if not poll.is_active:
            return Response({"error": "Poll is not active"}, status=status.HTTP_400_BAD_REQUEST)
        choices = Choices.objects.filter(poll=poll)
        results = {choice.choice_text: choice.votes.count() for choice in choices}
        return Response({"poll": poll.question, "results": results}, status=status.HTTP_200_OK)