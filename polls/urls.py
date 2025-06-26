from django.urls import path
from .views import CreatePollView, ListPollsView, VoteView, ResultsView


urlpatterns = [
    path('', ListPollsView.as_view(), name='list_polls'),
    path('create/', CreatePollView.as_view(), name='create_poll'),
    path('<int:pk>/vote/', VoteView.as_view(), name='vote_poll'),
    path('<int:pk>/results/', ResultsView.as_view(), name='poll_results'),
]