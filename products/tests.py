from django.test import TestCase

from .forms import SearchForm, ProdottiForm, ReviewForm
from .models import Prodotti, Review,Categoria
from user_manage.models import User,Owner,Cliente

class ProdottiViewTest(TestCase):
    #evito di inserire ogni volta i dati con setUpTestData

    @classmethod
    def setUpTestData(cls):
        cls.user1= User.objects.create(username='cliente3',password='prova1234', is_client=True)
        cls.user2= User.objects.create(username='fornitore3',password='prova1234', is_owner=True)
        cls.cl1 = Cliente.objects.create(user=cls.user1)
        cls.fo1 = Owner.objects.create(user=cls.user2)
        cls.cat = Categoria.objects.create(nome='Buste',image='media/products/36958002/36958002.jpg')
        cls.cat2 = Categoria.objects.create(nome='Cartone',image='media/products/36958002/36958002.jpg')
        cls.prod = Prodotti.objects.create(owner=cls.fo1,categoria=cls.cat,name='Sacchetto Naturale',dimensione='30x10cm',tipo_materiale='plastica',price='0.70€',image='media/products/36958002/36958002.jpg')

       # cls.rew = Review.objects.create(prodotto=cls.prod,comment_name='OTTIMO',comment_body='Davvero speciale',rating_fornitore='5',rating_prodotto='5')


    def test_Product_create(self):
        Prodotti.objects.create(owner=self.fo1,categoria=self.cat2,name='Cartone patatine', dimensione='10x10cm',tipo_materiale='cartone',price='0.50€',image='media/products/36958002/36958002.jpg')
        self.client.force_login(user=self.user2)
        dati = {
            'name': 'Cartone patatine',
            'dimensione': '10x10cm',
            'tipo_materiale': 'cartone',
            'price': '0.50€',
            'image': 'media/products/36958002/36958002.jpg'
        }
        response = self.client.post(f'/products/products/create',data=dati)
        self.assertEqual(response.status_code,200)

    def test_Product_detail(self):
        response = self.client.get(f'/products/products/{self.prod.pk}/detail')
        self.assertEqual(response.status_code,200)

    def test_Product_delete(self):
        Prodotti.objects.create(owner=self.fo1, categoria=self.cat2, name='Cartone patatine', dimensione='10x10cm',
                                tipo_materiale='cartone', price='0.50€', image='media/products/36958002/36958002.jpg')
        self.client.force_login(user=self.user2)
        response = self.client.get(f'/products/products/{self.prod.pk}/delete')
        self.assertEqual(response.status_code,200)

    def test_Search(self):
        response = self.client.get(f'/products/')
        self.assertEqual(response.status_code,200)

    def test_Add_review(self):
        self.client.force_login(user=self.user1)
        response = self.client.get(f'/products/product/{self.prod.pk}/recensioni')
        self.assertEqual(response.status_code,200)


class FormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create(username='cliente3', password='prova1234', is_client=True)
        cls.user2 = User.objects.create(username='fornitore3', password='prova1234', is_owner=True)
        cls.cl1 = Cliente.objects.create(user=cls.user1)
        cls.fo1 = Owner.objects.create(user=cls.user2)
        cls.cat = Categoria.objects.create(nome='Buste', image='media/products/36958002/36958002.jpg')
        cls.cat2 = Categoria.objects.create(nome='Cartone', image='media/products/36958002/36958002.jpg')
        cls.prod = Prodotti.objects.create(owner=cls.fo1, categoria=cls.cat, name='Sacchetto Naturale',dimensione='30x10cm', tipo_materiale='plastica', price='0.70€',image='media/products/36958002/36958002.jpg')

    def test_SearchForm(self):
        dati = {
            'nome': 'Sacchetto Naturale',
            'material': 'plastica',
            'min_price': '1',
            'max_price':'5'
        }
        form = SearchForm(dati)
        self.assertTrue(form.is_valid())

    def test_ProductForm_valid(self):
        self.client.force_login(user=self.user2)
        dati= {
            'owner': self.user2,
            'categoria': self.cat2,
            'name': 'Buste',
            'dimensione': '2x3cm',
            'tipo_materiale': 'carta',
            'price': '2€',
            'image': 'media/products/36958002/36958002.jpg'
        }
        form = ProdottiForm(dati)
        self.assertTrue(form.is_valid())

    def test_ProductForm_not_valid(self):
        self.client.force_login(user=self.user2)
        dati = {
            'name': 'Buste',
            'dimensione': '2x3cm',
            'tipo_materiale': 'carta',
            'price': '2€',
            'image': 'media/products/36958002/36958002.jpg'
        }
        form = ProdottiForm(dati)
        self.assertFalse(form.is_valid())

    def test_ReviewForm_valid(self):
        self.client.force_login(user=self.user1)
        dati = {
            'prodotto': self.prod.pk,
            'comment_name': 'OTTIMO',
            'comment_body': 'Grandioso prodotto e fornitore affidabile',
            'rating_fornitore': '5',
            'rating_prodotto': '5'
        }
        form = ReviewForm(dati)
        self.assertTrue(form.is_valid())

    def test_ReviewForm_not_valid(self):
        self.client.force_login(user=self.user1)
        dati = {
            'prodotto': self.prod.pk,
            'comment_name': 'OTTIMO',
            'comment_body': 'Grandioso prodotto e fornitore affidabile',
            'rating_fornitore': '6',
            'rating_prodotto': '5'
        }
        form = ReviewForm(dati)
        self.assertFalse(form.is_valid())