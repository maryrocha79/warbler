import unittest
from app import app, db
from models import User


class NoUserTestCase(unittest.TestCase):
    def setUp(self):
        app.config[
            'SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/test_warbler_db'

        db.create_all()
        self.user1 = User(
            username='mary',
            image_url='https://via.placeholder.com/250x250',
            header_image_url='https://via.placeholder.com/1000x200',
            bio='hi this is my bio',
            location='sf',
            email='mary@rithm.com',
            password=User.hash_password('123456'))
        db.session.add(self.user1)
        db.session.commit()

    def tearDown(self):
        db.session.close()
        db.drop_all()

    def test_user_added_to_db(self):
        self.assertNotEqual(self.user1.id, None)

    def test_password_hashed(self):
        self.assert_(self.user1.password.startswith("$2b"))

    def test_user_authenticates(self):
        auth = User.authenticate("mary", "123456")
        self.assertEqual(auth.username, "mary")

    def test_user_authenticate_fails(self):
        auth = User.authenticate("mary", "wrong-password")
        self.assertEqual(auth, False)


if __name__ == '__main__':
    unittest.main()

# email = db.Column(db.Text, unique=True)
# username = db.Column(db.Text, unique=True)
# image_url = db.Column(db.Text, default="/static/images/default-pic.png")
# header_image_url = db.Column(db.Text)
# bio = db.Column(db.Text)
# location = db.Column(db.Text)
# password = db.Column(db.Text)
# messages = db.relationship('Message', backref='user', lazy='dynamic')
# followers = db.relationship(
#     "User",
#     secondary=FollowersFollowee,
#     primaryjoin=(FollowersFollowee.c.follower_id == id),
#     secondaryjoin=(FollowersFollowee.c.followee_id == id),
#     backref=db.backref('following', lazy='dynamic'),
#     lazy='dynamic')
# liked_messages = db.relationship(
#     'Message',
#     secondary=LikesMessages,
#     backref=db.backref('user_likes', lazy='dynamic'),
#     lazy='dynamic')
