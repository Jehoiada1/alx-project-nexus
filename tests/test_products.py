import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from catalog.models import Category, Product


@pytest.mark.django_db
def test_create_and_filter_products():
    user = User.objects.create_user(username='maker', password='StrongPass123')
    client = APIClient()
    token_resp = client.post('/api/auth/login/', {"username": "maker", "password": "StrongPass123"}, format='json')
    access = token_resp.data['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')

    cat_resp = client.post('/api/categories/', {"name": "Shoes", "description": "Footwear"}, format='json')
    assert cat_resp.status_code == 201, cat_resp.content
    cat_id = cat_resp.data['id']

    prod_payload = {"name": "Running Shoe", "description": "Lightweight", "price": "79.99", "stock": 10, "category": cat_id}
    p_resp = client.post('/api/products/', prod_payload, format='json')
    assert p_resp.status_code == 201, p_resp.content

    list_resp = client.get('/api/products/?min_price=50&max_price=100&search=running&ordering=price')
    assert list_resp.status_code == 200
    assert list_resp.data['results'][0]['name'] == 'Running Shoe'
