from app import app
from unittest import TestCase
from models import connect_db

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
connect_db(app)

class FlaskTests(TestCase):
    '''Testing General Flask'''

    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG_TB_HOSTS'] = ['dont=show-debug-toolbar']

    def test_index_page(self):
        '''Test that calling index page will result: 
        1. 200 response 
        2. Form HTML elements test'''

        with app.test_client() as client:
            resp = client.get('/')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status, '302 FOUND')
            self.assertEqual(resp.location, 'http://localhost/users')
        
    def test_index_page_redirect(self):
        with app.test_client() as client:
            resp = client.get('/', follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status, '200 OK')
                
    
    def test_user_page(self):
        with app.test_client() as client:
            resp = client.get('/users/new')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status, '200 OK')
            self.assertIn('<button type="submit">Add</button>', html)

    def test_user_page_post(self):
        with app.test_client() as client:
            resp = client.post('/users/new', data={'first-name': 'Mary', 'last-name': 'Jane', 'image-url': 'None'})
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status, '302 FOUND')
            self.assertEqual(resp.location, 'http://localhost/users')
    
    # def test_delete_page(self):
    #     with app.test_client() as client:
    #         resp = client.get('/users/1/delete')
    #         html = resp.get_data(as_text=True)
    #         self.assertEqual(resp.status, '302 FOUND')
    #         self.assertEqual(resp.location, 'http://localhost/users')

    

