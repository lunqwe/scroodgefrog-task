from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from .serializers import *
from .models import CustomUser


# function for detailing validation error
def error_detail(e):
    errors = e.detail
    
    error_messages = []
    for field, messages in errors.items():
        error_messages.append(f'{field}: {messages[0].__str__()}')
    
    return error_messages

# Create your views here.
class CreateUserView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CreateUserSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        try:
            if serializer.is_valid(raise_exception=True):
                print(request.data)
                data = serializer.validated_data
                user = CustomUser.objects.create_user(**data)
                if user:
                    data = {'status': 'success', 'detail': "User registered successfully!"}
                    return Response(data=data, status=status.HTTP_201_CREATED)

        except serializers.ValidationError as e:
            data = {'status': 'error', 'detail': error_detail(e)}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

    

class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            if serializer.is_valid(raise_exception=True):
                user = serializer.validated_data
                if user:
                    data = serializer.validated_data
                    login_response = CustomUser.objects.login_user(request, **data)
                    return Response(data={1})
                else:
                    return Response(data={'status': "error", 'detail': error_detail(e)})

        except serializers.ValidationError as e:
            return Response(data={'status': "error", 'detail': error_detail(e)})