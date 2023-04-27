
import sys
import os
os.environ['DATABASE_URL'] = 'sqlite:///test.db'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import patch
from application import application
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

class myProxyHack(object):

    def __init__(self, application):
        self.application = application

    def __call__(self, environ, start_response):
        environ['REMOTE_ADDR'] = environ.get('REMOTE_ADDR', '127.0.0.1')
        return self.application(environ, start_response)

class TestBlackList(unittest.TestCase):
    rand_email = fake_str(3) + '@' + fake_str(3) + '.com'
    rand_app_uuid = fake_str(10)
    rand_blocked_reason = fake_str(50)
    rand_ip = fake_str(10)

    def setUp(self):
        self.application = application
        self.application.wsgi_app = myProxyHack(application.wsgi_app)
        self.client = self.application.test_client()
        self.token_ = ''
    
    def test_health(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

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
                                    headers={'Authorization': 'Bearer 1234321234321'},
                                    environ_base={'REMOTE_ADDR': '127.0.0.1'})

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
        #print(response.data)
        self.assertEqual(response.status_code, 412)
        response_data = json.loads(response.get_data(as_text=True))
        self.assertIn("error", response_data)
    
    def test_create_offer_error_2(self):
        data_create = {
            "email": self.rand_email,
            "blocked_reason": self.rand_blocked_reason,
        }  

        response = self.client.post('/blacklists',
                                    data=json.dumps(data_create), 
                                    content_type='application/json',
                                    headers={'Authorization': 'Bearer 1234321234321'})
        #print(response.data)
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.get_data(as_text=True))
        self.assertIn("error", response_data)

    def test_get_email_from_blackList(self):

        data_create = {
            "email": 'acj8991@gmail.com',
            "app_uuid": self.rand_app_uuid,
            "blocked_reason": self.rand_blocked_reason,
            "ipSolicitud": self.rand_ip,
        }  
        
        response = self.client.post('/blacklists',
                                    data=json.dumps(data_create), 
                                    content_type='application/json',
                                    headers={'Authorization': 'Bearer 1234321234321'},
                                    environ_base={'REMOTE_ADDR': '127.0.0.1'})
        email = 'acj8991@gmail.com'
        endPoint = '/blacklists/{}'.format(email)
        response = self.client.get(endPoint,
                                    content_type='application/json',
                                    headers={'Authorization': 'Bearer 1234321234321'},
                                    environ_base={'REMOTE_ADDR': '127.0.0.1'})
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.get_data(as_text=True))
        self.assertIn("id", response_data)
        self.assertIn("email", response_data)

    def test_get_email_not_found_from_blackList(self):
        email = "andres-8991@yahhoo.com"
        endPoint = '/blacklists/{}'.format(email)
        response = self.client.get(endPoint,
                                    content_type='application/json',
                                    headers={'Authorization': 'Bearer 1234321234321'},
                                    environ_base={'REMOTE_ADDR': '127.0.0.1'})
        self.assertEqual(response.status_code, 401)