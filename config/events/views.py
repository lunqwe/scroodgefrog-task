from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import *
from .models import CustomUser
from .filters import EventFilter


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
            serializer.is_valid(raise_exception=True)
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
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data
            login_response = CustomUser.objects.login_user(request, **data)
            return Response(data=login_response[0], status=login_response[1])

        except serializers.ValidationError as e:
            return Response(data={'status': "error", 'detail': error_detail(e)})
        

class CreateEventView(generics.CreateAPIView):
    queryset = Event.objects.all()
    serializer_class = CreateEventSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            response_data = {
                'status': 'success',
                'message': 'Event created successfully',
                'data': serializer.data
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        except serializers.ValidationError as e:
            return Response(data={'status': "error", 'detail': error_detail(e)}, status=status.HTTP_400_BAD_REQUEST)
            
class EventDetailView(generics.RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'details':str(e)}, status=status.HTTP_404_NOT_FOUND)

class EventListView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = EventFilter

class UpdateEventView(generics.UpdateAPIView):
    queryset = Event.objects.all()
    serializer_class = UpdateEventSerializer

    def put(self, request, event_id):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            event = Event.objects.get(id=event_id)
            for key, value in serializer.data.items():
                setattr(event, key, value)
            event.save()

            response_data = {
                'status': 'success',
                'message': 'Event created successfully',
                'data': serializer.data
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        except serializers.ValidationError as e:
            return Response(data={'status': "error", 'detail': error_detail(e)}, status=status.HTTP_400_BAD_REQUEST)


class DeleteEventView(generics.DestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = DeleteEventSerializer

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'message': 'Object deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


class EventRegisterView(generics.CreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventRegisterSerializer

    def post(self, request, event_id):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            event = get_object_or_404(Event, id=event_id)
            user = get_object_or_404(CustomUser, id=serializer.data.get('user_id'))
            if not event.attendees.filter(id=user.id).exists():
                event.attendees.add(user)
                return Response(data={'status': 'success', 'detail': 'User was registered successfully!'}, status=status.HTTP_200_OK)
            else:
                return Response(data={'status': 'error', 'detail': "User is already registered for this event."}, status=status.HTTP_409_CONFLICT)
        except serializers.ValidationError as e:
            return Response(data={'status': "error", 'detail': error_detail(e)}, status=status.HTTP_400_BAD_REQUEST)

class SearchEventView(generics.ListAPIView):
    serializer_class = EventSerializer

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        queryset = Event.objects.filter(title__icontains=query)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
