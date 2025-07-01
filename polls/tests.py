from django.test import TestCase
from rest_framework.test import APITestCase, APIRequestFactory, APIClient
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from polls import views
from django.urls import reverse

class TestPoll(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = views.ListCreatePollView.as_view()
        self.uri = reverse('list_polls')
        self.user = self.setup_user()
        self.token = Token.objects.create(user=self.user)
        self.token.save()
        self.client= APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)


    @staticmethod
    def setup_user():
        User = get_user_model()
        user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="testpass1234",
            bio="This is a test user", gender="null"
        )
        return user

    def test_list_polls(self):
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, 200,
                         'Expected Response Code 200, received {0} instead.'
                         .format(response.status_code))

    def test_create_poll(self):
        data = {
            "question": "Test Poll",
            "choices": [
                {"choice_text": "Choice 1"},
                {"choice_text": "Choice 2"}
            ]
        }
        response = self.client.post(self.uri, data, format='json')
        self.assertEqual(response.status_code, 201,
                         'Expected Response Code 201, received {0} instead.'
                         .format(response.status_code))
        self.assertEqual(response.data['title'], data['title'])
        self.assertEqual(len(response.data['choices']), len(data['choices']))