from django.test import TestCase

# Create your tests here.
from checkout.forms import OrderCreateForm
from checkout.models import Order
from forum.models import Forum
from products.models import Categoria, Prodotti
from user_manage.models import User, Cliente, Owner


class CheckoutFormTest(TestCase):
    #evito di inserire i dati con setUpTestData

    @classmethod
    def setUpTestData(cls):
            cls.user1 = User.objects.create(username='cliente3', password='prova1234', is_client=True)
            cls.user2 = User.objects.create(username='fornitore3', password='prova1234', is_owner=True)
            cls.cl1 = Cliente.objects.create(user=cls.user1)
            cls.fo1 = Owner.objects.create(user=cls.user2)
            cls.forum = Forum.objects.create(fornitore=cls.fo1,user=cls.cl1,titolo='prova',descrizione='prova',contenuto='prova')
            cls.cat = Categoria.objects.create(nome='Buste', image='media/products/36958002/36958002.jpg')
            cls.cat2 = Categoria.objects.create(nome='Cartone', image='media/products/36958002/36958002.jpg')
            cls.prod = Prodotti.objects.create(owner=cls.fo1, categoria=cls.cat, name='Sacchetto Naturale',
                                               dimensione='30x10cm', tipo_materiale='plastica', price='0.70€',
                                               image='media/products/36958002/36958002.jpg')

    def test_ProductForm_invalid(self):
        self.client.force_login(user=self.user1)
        dati= {
            'firs_name': 'Tom',
            'last_name': 'Bonisoli',
            'email': 'rimangoio@gmail.com',
            'address': 'via morlaso',
            'postal_code': '89800',
            'city ': 'Venezia',
        }
        form = OrderCreateForm(dati)
        self.assertFalse(form.is_valid())
