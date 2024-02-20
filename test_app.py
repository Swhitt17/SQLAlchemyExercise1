from unittest import TestCase

from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///test_blogly'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

context = app.app_context()
context.push()

db.drop_all()
db.create_all()


class UserViewsTestCase(TestCase):
    """Tests for views for User."""

    def setUp(self):
        """Add sample user."""

        User.query.delete()

        user = User(first_name='Betsy', last_name='Martin', image_url='https://www.flaticon.com/free-icon/user_219969')
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_list_users(self):
       with app.test_client() as client:
          res = client.get('/users')
          html = res.get_data(as_text=True)

          self.assertEqual(res.status_code, 200)
          self.assertIn('Betsy Martin',html)

    def test_show_user(self):
        with app.test_client() as client:
          res = client.get(f'/{self.user_id}')
          html = res.get_data(as_text=True)

          self.assertEqual(res.status_code, 200)
          self.assertIn('<h1>Betsy Martin</h1>',html)

    def test_create_user(self):
        with app.test_client() as client:
          d={'first_name': 'Tyson', 'last_name':'Mays', 'image_url': 'https://www.freepik.com/icon/profile_3135715#fromView=keyword&term=User&page=1&position=4&uuid=b54ae4ab-f32f-4a13-bd70-d8219a2fa9b7'}
          res = client.get('/users/new',data=d, follow_redirects=True)
          html = res.get_data(as_text=True)

          self.assertEqual(res.status_code, 200)
          self.assertIn('<h1>Tyson Mays</h1>',html)

    def test_edit_user(self):
        with app.test_client() as client:
          d={'first_name': 'Mike', 'last_name':'Mays', 'image_url': 'https://www.freepik.com/icon/profile_3135715#fromView=keyword&term=User&page=1&position=4&uuid=b54ae4ab-f32f-4a13-bd70-d8219a2fa9b7'}
          res = client.get('/users/new',data=d, follow_redirects=True)
          html = res.get_data(as_text=True)

          self.assertEqual(res.status_code, 200)
          self.assertIn('<h1>Mike Mays</h1>',html)
