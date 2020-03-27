from app import app
from unittest import TestCase
from models import db, Post, User


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class FlaskTests(TestCase):
    '''Testing General Flask'''

    def setUp(self):

        User.query.delete()
        Post.query.delete()

        max = User(first_name='Max', last_name='Jung', image_url="https://kottke.org/plus/misc/images/ai-faces-01.jpg")
        db.session.add(max)
        db.session.commit()

        max_post = Post(title='hello world', content='its me', user_id=1)
        db.session.add(max_post)
        db.session.commit()
        # breakpoint()

    def tearDown(self):

        # db.session.rollback()
        # breakpoint()
        db.drop_all()
        db.create_all()

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
    
    def test_display_post(self):
        " page for post displays correctly "

        with app.test_client() as client:
            resp = client.get('/posts/1')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status, '200 OK')
            self.assertIn('hello world', html)
    
    def test_edit_post(self):
        " test that edit post page loads correctly "

        with app.test_client() as client:
            resp = client.get('/posts/1/edit')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status, '200 OK')
            self.assertIn('Edit Post', html)

    def test_store_post(self):
        " create post for DB and confirm redirect"

        with app.test_client() as client:
            resp = client.post('/users/1/posts/new', data={'title': 'Unit Test Post', 'content': 'if you are seeing this the test was successful'})
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status, '302 FOUND')
            self.assertEqual(resp.location, 'http://localhost/users/1')

    def test_delete_post(self):
        " delete the post made in previous test "

        with app.test_client() as client:
            resp = client.post(f'/posts/1/delete')
            self.assertEqual(resp.status, '302 FOUND')
            self.assertEqual(resp.location, 'http://localhost/users/1')