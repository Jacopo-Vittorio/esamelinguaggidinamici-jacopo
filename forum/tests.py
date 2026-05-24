from django.test import TestCase

# Create your tests here.
from forum.forms import ForumForm
from forum.models import Forum
from products.models import Categoria, Prodotti
from user_manage.models import User, Cliente, Owner


class ForumViewTest(TestCase):
    #evito di inserire i dati con setUpTestData

    @classmethod
    def setUpTestData(cls):
            cls.user1 = User.objects.create(username='cliente3', password='prova1234', is_client=True)
            cls.user2 = User.objects.create(username='fornitore3', password='prova1234', is_owner=True)
            cls.cl1 = Cliente.objects.create(user=cls.user1)
            cls.fo1 = Owner.objects.create(user=cls.user2)
            cls.forum = Forum.objects.create(fornitore=cls.fo1,user=cls.cl1,titolo='prova',descrizione='prova',contenuto='prova')

    def test_ThreadCreateView(self):
        Forum.objects.create(fornitore=self.fo1,user=self.cl1,titolo='prova',descrizione='prova',contenuto='prova')
        self.client.force_login(user=self.user1)
        dati = {
            'fornitore':self.fo1,
            'user': self.cl1,
            'titolo':'prova',
            'descrizione':'prova',
            'contenuto':'prova'
        }
        response = self.client.post(f'/forum/create', data=dati)
        self.assertEqual(response.status_code, 200)

    def test_RispostaList_DetailView(self):
        response = self.client.get(f'/forum/forum/{self.forum.pk}/discussione/')
        self.assertEqual(response.status_code, 200)

    def test_AddCommentView(self):
        Forum.objects.create(fornitore=self.fo1, user=self.cl1, titolo='prova', descrizione='prova', contenuto='prova')

class ForumFormTest(TestCase):
    #evito di inserire i dati con setUpTestData

    @classmethod
    def setUpTestData(cls):
            cls.user1 = User.objects.create(username='cliente3', password='prova1234', is_client=True)
            cls.user2 = User.objects.create(username='fornitore3', password='prova1234', is_owner=True)
            cls.cl1 = Cliente.objects.create(user=cls.user1)
            cls.fo1 = Owner.objects.create(user=cls.user2)
            cls.forum = Forum.objects.create(fornitore=cls.fo1,user=cls.cl1,titolo='prova',descrizione='prova',contenuto='prova')

    def ForumForm_valid(self):
        self.client.force_login(user=self.user1)
        dati = {
            'fornitore': self.fo1,
            'titolo': 'prova',
            'descrizione': 'prova',
            'contenuto': 'prova',
            }
        form = ForumForm(dati)
        self.assertTrue(form.is_valid())

    def ForumForm_not_valid(self):
        self.client.force_login(user=self.user1)
        dati = {
            'fornitore': self.fo1,
            'descrizione': 'prova',
            'contenuto': 'prova',
            }
        form = ForumForm(dati)
        self.assertTrue(form.is_valid())