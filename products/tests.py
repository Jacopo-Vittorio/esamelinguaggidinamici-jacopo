from django.test import TestCase

from .forms import SearchForm, ProdottiForm, ReviewForm
from checkout.models import Order, OrderItem
from products.recommendations import get_suggested_products
from .models import Prodotti, Review, Categoria, SearchHistory
from user_manage.models import User,Owner,Cliente

class ProdottiViewTest(TestCase):
    #evito di inserire ogni volta i dati con setUpTestData

    @classmethod
    def setUpTestData(cls):
        Prodotti.objects.filter(
            name__in=['Pacchetto standard', 'Imballaggio a base fungina']
        ).delete()

        cls.user1= User.objects.create(username='cliente3',password='prova1234', is_client=True)
        cls.user2= User.objects.create(username='fornitore3',password='prova1234', is_owner=True)
        cls.cl1 = Cliente.objects.create(user=cls.user1)
        cls.fo1 = Owner.objects.create(user=cls.user2)
        cls.cat = Categoria.objects.create(nome='Buste',image='media/products/36958002/36958002.jpg')
        cls.cat2 = Categoria.objects.create(nome='Cartone',image='media/products/36958002/36958002.jpg')
        cls.prod = Prodotti.objects.create(owner=cls.fo1,categoria=cls.cat,name='Sacchetto Naturale',dimensione='30x10cm',tipo_materiale='plastica',price='0.70',image='media/products/36958002/36958002.jpg')

       # cls.rew = Review.objects.create(prodotto=cls.prod,comment_name='OTTIMO',comment_body='Davvero speciale',rating_fornitore='5',rating_prodotto='5')


    def test_Product_create(self):
        Prodotti.objects.create(owner=self.fo1,categoria=self.cat2,name='Cartone patatine', dimensione='10x10cm',tipo_materiale='cartone',price='0.50',image='media/products/36958002/36958002.jpg')
        self.client.force_login(user=self.user2)
        dati = {
            'name': 'Cartone patatine',
            'dimensione': '10x10cm',
            'tipo_materiale': 'cartone',
            'price': '0.50',
            'image': 'media/products/36958002/36958002.jpg'
        }
        response = self.client.post(f'/products/products/create',data=dati)
        self.assertEqual(response.status_code,200)

    def test_Product_detail(self):
        response = self.client.get(f'/products/products/{self.prod.pk}/detail')
        self.assertEqual(response.status_code,200)

    def test_Product_list_cart_button_route(self):
        response = self.client.get(f'/products/products/{self.prod.pk}/list')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f'/cart/add/{self.prod.pk}/')

    def test_Category_owner_action_routes(self):
        self.client.force_login(user=self.user2)
        response = self.client.get(f'/products/categoria/?category={self.cat.nome}')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f'/products/products/{self.prod.pk}/update')
        self.assertContains(response, f'/products/products/{self.prod.pk}/delete')

    def test_Product_delete(self):
        Prodotti.objects.create(owner=self.fo1, categoria=self.cat2, name='Cartone patatine', dimensione='10x10cm',
                                tipo_materiale='cartone', price='0.50', image='media/products/36958002/36958002.jpg')
        self.client.force_login(user=self.user2)
        response = self.client.get(f'/products/products/{self.prod.pk}/delete')
        self.assertEqual(response.status_code,200)

    def test_Search(self):
        response = self.client.get(f'/products/')
        self.assertEqual(response.status_code,200)
        self.assertNotContains(response, 'href="/forum/list/ "')

    def test_Search_saves_history_for_logged_user(self):
        self.client.force_login(user=self.user1)
        response = self.client.get('/products/?nome=Sacchetto&material=plastica')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            SearchHistory.objects.filter(
                user=self.user1,
                query='Sacchetto',
                material='plastica',
            ).exists()
        )

    def test_suggested_products_use_bought_categories(self):
        suggested_product = Prodotti.objects.create(
            owner=self.fo1,
            categoria=self.cat,
            name='Sacchetto Avana',
            dimensione='20x10cm',
            tipo_materiale='plastica',
            price='1.20',
            image='media/products/36958002/36958002.jpg',
        )
        order = Order.objects.create(
            user=self.user1,
            firs_name='Tom',
            last_name='Test',
            email='tom@example.com',
            address='Via Roma',
            postal_code='00100',
            city='Roma',
        )
        OrderItem.objects.create(
            order=order,
            product=self.prod,
            price=self.prod.price,
            quantity=1,
        )

        suggestions = list(get_suggested_products(self.user1))

        self.assertIn(suggested_product, suggestions)
        self.assertNotIn(self.prod, suggestions)

    def test_suggested_products_fallback_to_three_random_products_without_orders(self):
        products = [
            self.prod,
            Prodotti.objects.create(
                owner=self.fo1,
                categoria=self.cat,
                name='Sacchetto Avana',
                dimensione='20x10cm',
                tipo_materiale='carta',
                price='1.20',
                image='media/products/36958002/36958002.jpg',
            ),
            Prodotti.objects.create(
                owner=self.fo1,
                categoria=self.cat2,
                name='Cartone Ondulato',
                dimensione='40x30cm',
                tipo_materiale='cartone',
                price='2.10',
                image='media/products/36958002/36958002.jpg',
            ),
        ]

        suggestions = list(get_suggested_products(self.user1))

        self.assertEqual(len(suggestions), 3)
        self.assertCountEqual(suggestions, products)

    def test_homepage_shows_random_suggestions_for_logged_user_without_orders(self):
        products = [
            self.prod,
            Prodotti.objects.create(
                owner=self.fo1,
                categoria=self.cat,
                name='Sacchetto Avana',
                dimensione='20x10cm',
                tipo_materiale='carta',
                price='1.20',
                image='media/products/36958002/36958002.jpg',
            ),
            Prodotti.objects.create(
                owner=self.fo1,
                categoria=self.cat2,
                name='Cartone Ondulato',
                dimensione='40x30cm',
                tipo_materiale='cartone',
                price='2.10',
                image='media/products/36958002/36958002.jpg',
            ),
        ]
        self.client.force_login(user=self.user1)

        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'homeSuggestedCarousel')
        self.assertContains(response, 'Prodotti suggeriti')
        self.assertContains(response, 'data-interval="10000"')
        for product in products:
            self.assertContains(response, product.name)
            self.assertContains(response, f'/products/products/{product.pk}/detail')

    def test_homepage_shows_suggestions_carousel_for_logged_user(self):
        suggested_product = Prodotti.objects.create(
            owner=self.fo1,
            categoria=self.cat,
            name='Sacchetto Avana',
            dimensione='20x10cm',
            tipo_materiale='plastica',
            price='1.20',
            image='media/products/36958002/36958002.jpg',
        )
        SearchHistory.objects.create(user=self.user1, query='Avana')
        self.client.force_login(user=self.user1)

        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'homeSuggestedCarousel')
        self.assertContains(response, 'Prodotti suggeriti')
        self.assertContains(response, suggested_product.name)

    def test_search_page_shows_suggestions_carousel_for_logged_user(self):
        suggested_product = Prodotti.objects.create(
            owner=self.fo1,
            categoria=self.cat,
            name='Sacchetto Avana',
            dimensione='20x10cm',
            tipo_materiale='plastica',
            price='1.20',
            image='media/products/36958002/36958002.jpg',
        )
        SearchHistory.objects.create(user=self.user1, query='Avana')
        self.client.force_login(user=self.user1)

        response = self.client.get('/products/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'searchSuggestedCarousel')
        self.assertContains(response, 'Prodotti suggeriti')
        self.assertContains(response, suggested_product.name)

    def test_cart_page_shows_suggestions_carousel_for_logged_user(self):
        suggested_product = Prodotti.objects.create(
            owner=self.fo1,
            categoria=self.cat,
            name='Sacchetto Avana',
            dimensione='20x10cm',
            tipo_materiale='plastica',
            price='1.20',
            image='media/products/36958002/36958002.jpg',
        )
        SearchHistory.objects.create(user=self.user1, query='Avana')
        self.client.force_login(user=self.user1)

        response = self.client.get('/cart/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'cartSuggestedCarousel')
        self.assertContains(response, 'Prodotti suggeriti')
        self.assertContains(response, suggested_product.name)

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
        cls.prod = Prodotti.objects.create(owner=cls.fo1, categoria=cls.cat, name='Sacchetto Naturale',dimensione='30x10cm', tipo_materiale='plastica', price='0.70',image='media/products/36958002/36958002.jpg')

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
            'price': '2.00',
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
            'price': '2.00',
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
