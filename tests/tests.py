from flask import json
from unittest import TestCase
from web import create_app
from web.api.models import db, Request


class TestRequests(TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app.app_context().push()
        self.client = self.app.test_client()
        self.first_request = {
            'title': 'First Request',
            'description': 'First Description',
            'clientId': 1,
            'priority': 1,
            'productId': 1,
            'targetDate': 'May 30, 2019'
        }
        self.second_request = {
            'title': 'Second Request',
            'description': 'Second Description',
            'clientId': 1,
            'priority': 1,
            'productId': 1,
            'targetDate': 'May 30, 2019'
        }
        self.request_edit = {
            'title': 'First Request Edited',
            'description': 'First Description Edited',
            'clientId': 1,
            'priority': 1,
            'productId': 1,
            'targetDate': 'May 30, 2019'
        }

    def createFirstRequestForTesting(self):
        self.client.post('/create', data=self.first_request)

    def createSecondRequestForTesting(self):
        self.client.post('/create', data=self.second_request)

    def test_create_request(self):
        res = self.client.post('/create', data=self.first_request)
        self.assertEqual(res.status_code, 302)
        self.assertEqual(Request.query.count(), 1)
        self.assertEqual(Request.query.get(1).title, 'First Request')

    def test_get_all_requests(self):
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)
        self.assertTrue("no feature requests" in res.get_data(as_text=True))

    def test_get_specific_request(self):
        self.createFirstRequestForTesting()
        res = self.client.get('/1')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data["title"], 'First Request')
        self.assertEqual(data["clientId"], 1)
        self.assertEqual(data["priority"], 1)

    def test_priority_reorder_on_create(self):
        self.createFirstRequestForTesting()
        res = self.client.post('/create', data=self.second_request)
        self.assertEqual(res.status_code, 302)
        self.assertEqual(Request.query.count(), 2)
        self.assertEqual(Request.query.get(1).priority, 2)
        self.assertEqual(Request.query.get(2).priority, 1)

    def test_update_request(self):
        self.createFirstRequestForTesting()
        res = self.client.post('/update/1', data=self.request_edit)
        self.assertEqual(res.status_code, 302)
        data = Request.query.get(1)
        self.assertEqual(data.title, 'First Request Edited')
        self.assertEqual(data.description, 'First Description Edited')

    def test_priority_reorder_on_update(self):
        self.createFirstRequestForTesting()
        self.createSecondRequestForTesting()
        res = self.client.post('/update/1', data=self.request_edit)
        self.assertEqual(res.status_code, 302)
        self.assertEqual(Request.query.get(1).priority, 1)
        self.assertEqual(Request.query.get(2).priority, 2)

    def test_delete_request(self):
        self.createFirstRequestForTesting()
        self.createSecondRequestForTesting()
        res = self.client.get('/delete/1')
        self.assertEqual(res.status_code, 302)
        self.assertEqual(Request.query.count(), 1)
        self.assertEqual(Request.query.first().title, 'Second Request')

    def test_request_not_found_on_get(self):
        res = self.client.get('/1')
        self.assertEqual(res.status_code, 404)

    def test_request_not_found_on_update(self):
        res = self.client.post('/update/1', data=self.request_edit)
        self.assertEqual(res.status_code, 404)

    def test_request_not_found_on_delete(self):
        res = self.client.get('/delete/1')
        self.assertEqual(res.status_code, 404)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
