import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import unittest
from unittest.mock import patch
from app import app
import json
import random
import string
from flask_restful import Api
from flask import Flask
from flask_restful import Resource

os.environ['DATABASE_URL'] = 'sqlite:///userm.db'


def generate_random_credentials():
    username = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    email = username + '@example.com'
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    return username, email, password

class TestVistaHealthCheck(unittest.TestCase):
    random_username, random_email, random_password = generate_random_credentials()

    def setUp(self):
        self.app = app
        #self.api = Api(self.app)
        #self.api.add_resource(VistaHealthCheck, '/health')
        self.client = self.app.test_client()
        self.token_ = ''

    def test_health_check(self):
        response = self.client.get('/users/ping')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'"pong"\n')

    def test_create_user(self):     
        data_create = {
            "username": self.random_username,
            "email": self.random_email,
            "password": self.random_password
        }   
        response = self.client.post('/users/', data=json.dumps(data_create), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        response_data = json.loads(response.get_data(as_text=True))
        self.assertIn("id", response_data)
        self.assertIn("createdAt", response_data)
    
    def test_get_token(self):
        data_get_token = {
            "username": self.random_username,
            "password": self.random_password
        } 
        response = self.client.post('/users/auth', data=json.dumps(data_get_token), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.get_data(as_text=True))
        self.assertIn("id", response_data)
        self.assertIn("token", response_data)
        self.assertIn("expireAt", response_data)
        # get token from response_data
        self.token_ = response_data["token"]
        # print(self.token_)
        print("Test Users/me: -----------------")
        response = self.client.get('/users/me', headers={'Authorization': 'Bearer ' + self.token_})
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.get_data(as_text=True))
        self.assertIn("id", response_data)
        self.assertIn("username", response_data)
        self.assertIn("email", response_data) 

if __name__ == '__main__':
    unittest.main()