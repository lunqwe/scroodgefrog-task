from django.urls import path
from .views import CreateUserView, LoginView, CreateEventView, UpdateEventView, EventDetailView, EventListView, EventRegisterView, DeleteEventView, SearchEventView

urlpatterns = [
    path('sign-up/', CreateUserView.as_view(), name='create_user'),
    path('login/', LoginView.as_view(), name='login'),
    path('events/', EventListView.as_view(), name='event-list'),
    path('events/create/', CreateEventView.as_view(), name='create-event'),
    path('events/update/<int:event_id>', UpdateEventView.as_view(), name='update-event'),
    path('events/details/<int:pk>', EventDetailView.as_view(), name='get-event'),
    path('events/delete/<int:pk>', DeleteEventView.as_view(), name='delete-event'),
    path('events/register/<int:event_id>', EventRegisterView.as_view(), name='register-to-event'),
    path('events/search/', SearchEventView.as_view(), name='search-event'),
]
