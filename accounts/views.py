from django.shortcuts import render
from .serializers import *
from .models import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView,GenericAPIView
from rest_framework.permissions import IsAuthenticated



# Create your views here.

class RegisterUser(CreateAPIView):

    serializer_class = RegisterUserSerializer
    queryset = User.objects.all()



    def post(self,request):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data, status = status.HTTP_201_CREATED)

        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class LoginAPIView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutAPIView(GenericAPIView):
    serializer_class = LogoutSerializer

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

class ViewUser(APIView):

    serializer_class = RegisterUserSerializer
    permission_classes = [IsAuthenticated]


    def get(self,request):

        user = User.objects.all()
        if user.exists():
            serializer = RegisterUserSerializer(user,many=True)
            return Response(serializer.data)

        else:
            return Response(status=status.HTTP_404_NOT_FOUND)