import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_register_and_login():
    client = APIClient()
    reg_payload = {"username": "alice", "email": "alice@example.com", "password": "StrongPass123", "password2": "StrongPass123"}
    r = client.post('/api/auth/register/', reg_payload, format='json')
    assert r.status_code == 201, r.content

    login_payload = {"username": "alice", "password": "StrongPass123"}
    # SimpleJWT default expects username field 'username' or 'email' depending on configuration; here username
    token_resp = client.post('/api/auth/login/', login_payload, format='json')
    assert token_resp.status_code == 200, token_resp.content
    assert 'access' in token_resp.data
    assert 'refresh' in token_resp.data


@pytest.mark.django_db
def test_profile_update():
    user = User.objects.create_user(username='bob', email='bob@example.com', password='StrongPass123')
    client = APIClient()
    token_resp = client.post('/api/auth/login/', {"username": "bob", "password": "StrongPass123"}, format='json')
    access = token_resp.data['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')
    patch_resp = client.patch('/api/auth/me/', {"first_name": "Bobby"}, format='json')
    assert patch_resp.status_code == 200
    assert patch_resp.data['first_name'] == 'Bobby'
