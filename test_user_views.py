import unittest
from app import app, db
from models import User


class NoUserTestCase(unittest.TestCase):
    def setUp(self):
        app.config[
            'SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/test_warbler_db'
        app.config['WTF_CSRF_ENABLED'] = False

        db.create_all()
        user1 = User(
            username='jason',
            image_url='https://via.placeholder.com/250x250',
            header_image_url='https://via.placeholder.com/1000x200',
            bio='hi this is my bio',
            location='sf',
            email='mary@rithm.com',
            password=User.hash_password('123456'))
        db.session.add(user1)
        db.session.commit()
        self.client = app.test_client()

    def tearDown(self):
        db.drop_all()

    def test_home_view(self):
        result = self.client.get('/', follow_redirects=True)
        self.assertIn(b'<h4>New to Warbler?', result.data)

    def test_signup_view(self):
        result = self.client.get('/signup')
        self.assertIn(b'Join Warbler today.</h2>', result.data)

    def test_login_view(self):
        result = self.client.get('/login')
        self.assertIn(b'message">Welcome back.', result.data)

    def test_users_index_view(self):
        result = self.client.get('/users')
        self.assertIn(b'<div class="col-lg-4 col-md-6 col-12">', result.data)

    def test_users_index_search_nouser_found_view(self):
        result = self.client.get('/users?q=jdhfsdjhf')
        self.assertIn(b'<h3>Sorry, no users found</h3>', result.data)

    def test_users_index_search_user_found_view(self):
        result = self.client.get('/users?q=jason')
        self.assertIn(b'@jason', result.data)

    def test_user_login(self):
        result = self.client.post(
            '/login', data={
                'username': 'jason',
                'password': '123456'
            })
        # print(result.data)
        self.assertEqual(result.status_code, 302)
        self.assertEqual(result.location, "http://localhost/")

    def test_user_login_fails(self):
        result = self.client.post(
            '/login', data={
                'username': 'jason',
                'password': '12345lll'
            })
        # print(result.data)
        self.assertIn(b'Invalid credentials.', result.data)

    def test_user_create(self):
        result = self.client.post(
            '/signup',
            data={
                'username': 'juan',
                'email': 'juan@yahoo.com',
                'password': '123457'
            })
        self.assertEqual(result.status_code, 302)

    def test_user_create_fail(self):
        result = self.client.post(
            '/signup',
            data={
                'username': 'jason',
                'email': 'juan@yahoo.com',
                'password': '123457'
            })
        self.assertIn(b"Username already taken", result.data)

    def test_user_show(self):
        result = self.client.get('/users/1')
        self.assertNotIn(b'value="Delete', result.data)


class UserLoggedInTestCase(unittest.TestCase):
    def setUp(self):
        app.config[
            'SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/test_warbler_db'
        app.config['WTF_CSRF_ENABLED'] = False

        db.create_all()
        user1 = User(
            username='jason',
            image_url='https://via.placeholder.com/250x250',
            header_image_url='https://via.placeholder.com/1000x200',
            bio='hi this is my bio',
            location='sf',
            email='mary@rithm.com',
            password=User.hash_password('123456'))
        user2 = User(
            username='juan',
            image_url='https://via.placeholder.com/250x250',
            header_image_url='https://via.placeholder.com/1000x200',
            bio='hi this is my ',
            location='pn',
            email='juan@rithm.com',
            password=User.hash_password('123457'))
        user3 = User(
            username='mary',
            image_url='https://via.placeholder.com/250x250',
            header_image_url='https://via.placeholder.com/1000x200',
            bio='hi this is my ',
            location='sj',
            email='mary5@rithm.com',
            password=User.hash_password('123458'))

        db.session.add_all([user1, user2, user3])
        db.session.commit()
        self.client = app.test_client()
        self.client.post(
            '/login', data={
                'username': 'jason',
                'password': '123456'
            })

    def tearDown(self):
        db.drop_all()

    def test_user_logout(self):
        result = self.client.get('/logout', follow_redirects=True)
        self.assertIn(b"You have successfully logged out.", result.data)

    def test_followers_create(self):
        result = self.client.post('users/2/followers')
        self.assertEqual(result.status_code, 302)
        result = self.client.get('/users/2/followers')
        self.assertIn(b'@jason', result.data)
        result = self.client.get('/users/1/following')
        self.assertIn(b'@juan', result.data)

    def test_followers_delete(self):
        result = self.client.post('users/2/followers')
        self.assertEqual(result.status_code, 302)
        result = self.client.post('/users/2/followers?_method=delete')
        self.assertEqual(result.status_code, 302)
        result = self.client.get('/users/2/followers')
        self.assertNotIn(b'@jason', result.data)
        result = self.client.get('/users/1/following')
        self.assertNotIn(b'@juan', result.data)

    def test_user_show(self):
        result = self.client.get('/users/1')
        self.assertIn(b'value="Delete', result.data)


if __name__ == '__main__':
    unittest.main()
