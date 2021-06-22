from user.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status


class ViewsTestCase(TestCase):
    """Test suite for the api views."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.user = User.objects.create(username="johndoe", is_superuser=True, )
        self.user.set_password('johnpassword')
        self.user.save()

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.login_data = {'username': 'johndoe', 'password': 'johnpassword'}

        self.response = self.client.post(
            '/api/v1.0.0/users/login',
            self.login_data, format="json")

        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_api_can_get_user_list(self):
        """Test the api can get a given userlist."""

        u = self.response.json()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + u.get('data').get('access_token'))
        response = self.client.get(
            '/api/v1.0.0/users/', format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
