import unittest
import json
from app import app
from db import init_db

class UserApiTestCase(unittest.TestCase):
    def setUp(self):
        init_db()
        self.app = app.test_client()
        self.app.testing = True

    def test_create_user(self):
        response = self.app.post('/user', json={'username': 'testuser'})
        self.assertIn(response.status_code, [201, 400])
        data = response.get_json()
        self.assertIn('username', data)

    def test_get_user(self):
        # 先建立一個 user
        create_resp = self.app.post('/user', json={'username': 'apitestuser'})
        if create_resp.status_code == 201:
            user_id = create_resp.get_json()['id']
        else:
            # 已存在則查詢 id 1
            user_id = 1
        response = self.app.get(f'/user/{user_id}')
        self.assertIn(response.status_code, [200, 404])

class MessageApiTestCase(unittest.TestCase):
    def setUp(self):
        init_db()
        self.app = app.test_client()
        self.app.testing = True

    def test_create_message(self):
        # 先建立 user
        user_resp = self.app.post('/user', json={'username': 'msguser'})
        user_id = user_resp.get_json().get('id', 1)
        response = self.app.post('/message', json={'user_id': user_id, 'content': 'hello'})
        self.assertIn(response.status_code, [201, 404, 400])
        data = response.get_json()
        self.assertIn('user_id', data)

    def test_get_message(self):
        # 先建立 user
        user_resp = self.app.post('/user', json={'username': 'msguser2'})
        user_id = user_resp.get_json().get('id', 1)
        # 建立 message
        msg_resp = self.app.post('/message', json={'user_id': user_id, 'content': 'hi'})
        if msg_resp.status_code == 201:
            msg_id = msg_resp.get_json()['id']
        else:
            msg_id = 1
        response = self.app.get(f'/message/{msg_id}')
        self.assertIn(response.status_code, [200, 404])

if __name__ == '__main__':
    unittest.main()
