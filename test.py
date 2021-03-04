from app import app
import unittest
from unittest import TestCase
class TestSimpleRoutes(unittest.TestCase):
    def setUp(self):
        """Stuff to do before every test."""

        tester = app.test_client(self)
        app.config['TESTING'] = True

    def test_home_page(self):
        with tester:
            response = tester.get('/', content_type='html/text')
            self.assertIn(b'users', response.data.lower())
            self.assertEqual(response.status_code, 200)

    def test_new_user_form(self):
        with tester:
            response = tester.get('/users/new', content_type='html/text')
            self.assertIn(b'create a user', response.data.lower())
            self.assertEqual(response.status_code, 200)

    def test_show_user(self):
        with tester:
            response = tester.get('/users/<int:user_id>', content_type='html/text')
            self.assertIn(b'user information', response.data.lower())
            self.assertEqual(response.status_code, 200)

    def test_users_edit_page(self):
        with tester:
            response = tester.get('/users/<int:user_id>/edit', content_type='html/text')
            self.assertIn(b'edit a user', response.data.lower())
            self.assertEqual(response.status_code, 200)