from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import CustomUser, CustomUserManager, Event


class CreateUserViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        data = {
            "email": "test@example.com",
            "username": "testusername",
            "password": "testpassword",
            "password2": "testpassword",
            "full_name": "Test User"
        }
        response = self.client.post('/api/sign-up/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(CustomUser.objects.filter(email="test@example.com").exists())

    def test_create_user_failure(self):
        data = {
            "email": "",  # invalid email
            "username": "testusername",
            "password": "testpassword",
            "password2": "testpassword",
            "full_name": "Test User"
        }
        response = self.client.post('/api/sign-up/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(email='test@gmail.com', username='test', full_name='Test User', password="testpassword")

    def test_login_success(self):
        data = {
            "email": "test@gmail.com",
            "password": "testpassword"
        }
        response = self.client.post('/api/login/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertTrue('token' in response.data)

    def test_login_failure(self):
        data = {
            "email": "test@gmail.com",
            "password": "wrongpassword"
        }
        response = self.client.post('/api/login/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CreateEventViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(email='test@gmail.com', username='test', full_name='Test User', password="testpassword")

    def test_create_event_success(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "organizer_id": self.user.id,
            "title": "Test Event",
            "description": "Test Event Description",
            "date": "2024-04-20T12:00:00Z",
            "location": "Test Location"
        }
        response = self.client.post('/api/events/create/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Event.objects.filter(title="Test Event").exists())

    def test_create_event_failure(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "organizer": self.user.id,
            "title": "",  # Missing required field
            "description": "Test Event Description",
            "date": "2024-04-20T12:00:00Z",
            "location": "Test Location"
        }
        response = self.client.post('/api/events/create/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class EventDetailViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(email='test@gmail.com', username='test', full_name='Test User', password="testpassword")
        self.event = Event.objects.create(organizer=self.user, title="Test Event", description="Test Event Description", date="2024-04-20T12:00:00Z", location="Test Location")

    def test_retrieve_event_success(self):
        event = Event.objects.filter(id=self.event.id)
        response = self.client.get(f'/api/events/details/{self.event.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_event_failure(self):
        response = self.client.get('/api/events/details/999')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class EventListViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(email='test@gmail.com', username='test', full_name='Test User', password="testpassword")
        self.event1 = Event.objects.create(organizer=self.user, title="Test Event 1", description="Test Event Description 1", date="2024-04-20T12:00:00Z", location="Test Location 1")
        self.event2 = Event.objects.create(organizer=self.user, title="Test Event 2", description="Test Event Description 2", date="2024-04-21T12:00:00Z", location="Test Location 2")

    def test_list_events(self):
        response = self.client.get('/api/events/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)


class UpdateEventViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create(email="test@example.com", password="testpassword", full_name="Test User")
        self.event = Event.objects.create(organizer=self.user, title="Test Event", description="Test Event Description", date="2024-04-20T12:00:00Z", location="Test Location")

    def test_update_event_success(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "title": "Updated Test Event",
            "description": "Updated Test Event Description",
            "date": "2024-04-21T12:00:00Z",
            "location": "Updated Test Location"
        }
        response = self.client.put(f'/api/events/update/{self.event.pk}', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.event.refresh_from_db()
        self.assertEqual(self.event.title, "Updated Test Event")

    def test_update_event_failure(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "title": "",  # Missing required field
            "description": "Updated Test Event Description",
            "date": "2024-04-21T12:00:00Z",
            "location": "Updated Test Location"
        }
        response = self.client.put(f'/api/events/update/{self.event.pk}', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteEventViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create(email="test@example.com", password="testpassword", full_name="Test User")
        self.event = Event.objects.create(organizer=self.user, title="Test Event", description="Test Event Description", date="2024-04-20T12:00:00Z", location="Test Location")

    def test_delete_event(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/api/events/delete/{self.event.id}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Event.objects.filter(title="Test Event").exists())


class EventRegisterViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create(email="test@example.com", password="testpassword", full_name="Test User")
        self.event = Event.objects.create(organizer=self.user, title="Test Event", description="Test Event Description", date="2024-04-20T12:00:00Z", location="Test Location")

    def test_register_event_success(self):
        self.client.force_authenticate(user=self.user)
        data = {"user_id": self.user.id}
        response = self.client.post(f'/api/events/register/{self.event.id}', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.event.attendees.filter(id=self.user.id).exists())

    def test_register_event_failure(self):
        self.client.force_authenticate(user=self.user)
        self.event.attendees.add(self.user)
        data = {"user_id": self.user.id}
        response = self.client.post(f'/api/events/register/{self.event.id}', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertTrue(self.event.attendees.filter(id=self.user.id).exists())


class SearchEventViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create(email="test@example.com", password="testpassword", full_name="Test User")
        self.event1 = Event.objects.create(organizer=self.user, title="Test Event 1", description="Test Event Description 1", date="2024-04-20T12:00:00Z", location="Test Location 1")
        self.event2 = Event.objects.create(organizer=self.user, title="Test Event 2", description="Test Event Description 2", date="2024-04-21T12:00:00Z", location="Test Location 2")

    def test_search_event(self):
        response = self.client.get('/api/events/', {'q': 'Event'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['title'], "Test Event 1")