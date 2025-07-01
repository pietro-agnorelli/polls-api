from django.urls import path
from .views import ListCreatePollView, DetailPollView, VoteView, ResultsView


urlpatterns = [
    path('<int:pk>/', DetailPollView.as_view(), name='detail_poll'),
    path('', ListCreatePollView.as_view(), name='list_polls'),
    path('<int:pk>/vote/', VoteView.as_view(), name='vote_poll'),
    path('<int:pk>/results/', ResultsView.as_view(), name='poll_results'),
]