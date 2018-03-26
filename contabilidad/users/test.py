# -*- coding: utf-8 -*-
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile
from rest_framework.test import APIClient
import json


class UserTestCase(TestCase):
    user_one = None
    user_one_email = "user_1@testing.com"
    user_one_password = "Prueba10"
    user_one_data = {
        "email": user_one_email,
        "password1": user_one_password,
        "password2": user_one_password,
        "first_name": "User One",
        "last_name": "Testing",
        "country_phone_code": "+52",
        "mobile_number": "9999999999"
    }

    def test_login(self):
        self.assertEqual("HOLA", "hola".upper())

    def test_registration_past(self):
        client = APIClient()
        response = client.post('/rest-auth/registration/', self.user_one_data, format='json')

        self.assertEqual(response.status_code, 201)

        self.user_one = User.objects.filter(email=self.user_one_email).first()

        self.assertNotEqual(self.user_one, None)

        email_address = self.user_one.emailaddress_set.all().first()

        self.assertNotEqual(email_address, None)

        email_address.verified = True
        email_address.save()

    def test_registration_password_mismatch(self):
        client = APIClient()
        data = {
            "email": "user_2@testing.com",
            "password1": "Prueba10",
            "password2": "Prueba01",
            "first_name": "User Two",
            "last_name": "Testing",
            "country_phone_code": "+52",
            "mobile_number": "9999999999"
        }
        response = client.post('/rest-auth/registration/', data, format='json')

        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.content)
        error_msg = response_data.get('non_field_errors', None)
        self.assertNotEqual(error_msg, None)
        self.assertIn('Los dos campos de contraseñas no coinciden entre si.', error_msg)

    def test_registration_missing_payload(self):
        client = APIClient()
        data = {
            "email": "user_2@testing.com",
            "password1": "Prueba10",
        }
        response = client.post('/rest-auth/registration/', data, format='json')

        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.content)

        expected_response = {
            'password2': ['Este campo es requerido.'],
            'first_name': ['Este campo es requerido.'],
            'last_name': ['Este campo es requerido.'],
            'country_phone_code': ['Este campo es requerido.'],
            'mobile_number': ['Este campo es requerido.']
        }

        self.assertEqual(response_data, expected_response)

    def test_login_success(self):
        client = APIClient()
        data = {
            "email": self.user_one_email,
            "password": self.user_one_password,
        }

        response = client.post('/rest-auth/login/', data, format='json')

        self.assertEqual(response.status_code, 200)



