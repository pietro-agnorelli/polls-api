from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from authentication.serializers import RegistrationSerializer


# Create your views here.

class RegistrationView(APIView):
    permission_classes = []
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.create(user=user)
            return Response({'token':token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = []
    def post(self, request):
        user = authenticate(
            username=request.data.get('username'),
            password=request.data.get('password'))
        if not user:
            return Response({'error': 'Bad credentials'}, status=status.HTTP_400_BAD_REQUEST)
        token = Token.objects.get(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)





