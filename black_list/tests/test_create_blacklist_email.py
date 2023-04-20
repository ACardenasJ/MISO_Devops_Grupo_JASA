
import sys
import os
os.environ['DATABASE_URL'] = 'sqlite:///test.db'
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

def fake_str(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str.upper()

class TestVistaHealthCheck(unittest.TestCase):
    rand_email = fake_str(3) + '@' + fake_str(3) + '.com'
    rand_app_uuid = fake_str(10)
    rand_blocked_reason = fake_str(50)
    rand_ip = fake_str(10)

    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
        self.token_ = ''

    def test_health_check(self):
        response = self.client.get('/blacklists/ping')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'"pong"\n')
    
    def test_create_offer(self):
        data_create = {
            "email": self.rand_email,
            "app_uuid": self.rand_app_uuid,
            "blocked_reason": self.rand_blocked_reason,
            "ipSolicitud": self.rand_ip,
        }  

        response = self.client.post('/blacklists',
                                    data=json.dumps(data_create), 
                                    content_type='application/json',
                                    headers={'Authorization': 'Bearer 1234321234321'})
        self.assertEqual(response.status_code, 201)
        response_data = json.loads(response.get_data(as_text=True))
        self.assertIn("id", response_data)
        self.assertIn("email", response_data)
        self.assertIn("createdAt", response_data)
    
    def test_create_offer_error(self):
        data_create = {
            "email": self.rand_email,
            "app_uuid": self.rand_app_uuid,
            "blocked_reason": self.rand_blocked_reason,
        }  

        response = self.client.post('/blacklists',
                                    data=json.dumps(data_create), 
                                    content_type='application/json',
                                    headers={'Authorization': 'Bearer 1234321234321'})
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.get_data(as_text=True))
        self.assertIn("error", response_data)
