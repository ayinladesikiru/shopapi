from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Category, Product


class CatalogTestData(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.phones = Category.objects.create(name='Phones', slug='phones')
        cls.laptops = Category.objects.create(name='Laptops', slug='laptops')

        cls.phone_a = Product.objects.create(
            category=cls.phones, title='Phone A', price='199.99', sku='PH-A',
        )
        cls.phone_b = Product.objects.create(
            category=cls.phones, title='Phone B', price='299.99', sku='PH-B',
        )
        cls.old_phone = Product.objects.create(
            category=cls.phones, title='Old Phone', price='49.99', sku='PH-OLD', is_active=False,
        )
        cls.laptop = Product.objects.create(
            category=cls.laptops, title='Laptop X', price='999.00', sku='LP-X',
        )


class ProductListViewTests(CatalogTestData):
    url = reverse('product_list')

    def test_list_is_public(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_only_active_products_returned(self):
        response = self.client.get(self.url)

        titles = {item['title'] for item in response.data}
        self.assertEqual(titles, {'Phone A', 'Phone B', 'Laptop X'})
        self.assertNotIn('Old Phone', titles)

    def test_product_fields(self):
        response = self.client.get(self.url)

        for item in response.data:
            self.assertEqual(set(item.keys()), {'title', 'price', 'description', 'sku'})

    def test_empty_list_when_no_products(self):
        Product.objects.all().delete()

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])


class CategoryProductsViewTests(CatalogTestData):
    def get_url(self, slug):
        return reverse('product_list_by_category', args=[slug])

    def test_category_is_public(self):
        response = self.client.get(self.get_url('phones'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_returns_category_details(self):
        response = self.client.get(self.get_url('phones'))

        self.assertEqual(response.data['id'], self.phones.id)
        self.assertEqual(response.data['name'], 'Phones')
        self.assertIsInstance(response.data['products'], list)

    def test_only_products_from_category_returned(self):
        response = self.client.get(self.get_url('phones'))

        titles = {item['title'] for item in response.data['products']}
        self.assertIn('Phone A', titles)
        self.assertIn('Phone B', titles)
        self.assertNotIn('Laptop X', titles)

    def test_unknown_slug_returns_404(self):
        response = self.client.get(self.get_url('does-not-exist'))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
