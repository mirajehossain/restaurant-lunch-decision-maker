from django.test import TestCase
from user.models import User


class UserTest(TestCase):
    """ Test module for user model """

    def setUp(self):
        first_name = 'John'
        last_name = 'Doe'
        username = 'johndoe'
        password = '12345'

        user = User(
            username=username,
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        user.save()

    def test_user_fullname(self):
        user = User.objects.get(username='johndoe')
        self.assertEqual(
            user.get_fullnamme(), "John Doe")
