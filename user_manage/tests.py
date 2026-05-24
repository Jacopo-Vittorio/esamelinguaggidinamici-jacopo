from django.test import TestCase

from .forms import ClienteSignUpForm
from .models import User,Cliente,Owner
# Create your tests here.

class UserManageViewForm(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create(username='cliente3', password='prova1234', is_client=True)
        cls.user2 = User.objects.create(username='fornitore3', password='prova1234', is_owner=True)
        cls.cl1 = Cliente.objects.create(user=cls.user1)
        cls.fo1 = Owner.objects.create(user=cls.user2)

    def test_client(self):
        c = self.cl1
        self.assertTrue(isinstance(c, Cliente))
        self.assertEqual(c.__str__(), c.user.username)

    def test_owner(self):
        self.assertTrue(isinstance(self.fo1, Owner))
        self.assertEqual(self.fo1.__str__(), self.fo1.user.username)

    def test_ClientCreate(self):
        response = self.client.get(f'/user_manage/registration/client')
        self.assertEqual(response.status_code, 200)

    def test_OwnerCreate(self):
        response = self.client.get(f'/user_manage/registration/owne')
        self.assertEqual(response.status_code, 200)

    def test_create_user_invalid(self):
        response = self.client.post('/user_manage/registration/client',
                                    {'username': 'cliente3', 'password':'prova1234'})
        self.assertFormError(response, 'form', field='username',
                             errors='A user with that username already exists.')

    def test_create_fornit_invalid(self):
        response = self.client.post('/user_manage/registration/owne',
                                    {'username': 'fornitore3', 'password': 'prova1234'})
        self.assertFormError(response, 'form', field='username',
                             errors='A user with that username already exists.')