from configs.database import db
from configs.config import SECRET_KEY
from passlib.apps import custom_app_context
from itsdangerous import TimedJSONWebSignatureSerializer, SignatureExpired, BadSignature


class User(db.Model):
    """
    the table of users
    """
    __talbename__ = 'user'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    username = db.Column(db.String(32), index=True, nullable=False)

    password_hash = db.Column(db.String(128), nullable=False)  # important! hash password

    email = db.Column(db.String(20), nullable=False)

    customization = db.Column(db.String(128), nullable=True)

    create_time = db.Column(db.DateTime, nullable=False)

    # db.relationship

    def hash_password(self, password):
        """
        save the hash password
        :param password:
        :return: password_hash
        """
        self.password_hash = custom_app_context.encrypt(password)

    def verify_password(self, password):
        """
        verify the hash password
        :param password:
        :return: True or False
        """
        return custom_app_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=600):
        """
        generate a new token
        :param expiration: duration
        :return: the signature
        """
        serializer = TimedJSONWebSignatureSerializer(SECRET_KEY, expiration)
        return serializer.dumps({"id":self.id}).decode("utf-8")

    @staticmethod
    def verify_token(token):
        """
        verify the token
        :param token:
        :return: the user information or error message
        """
        serializer = TimedJSONWebSignatureSerializer(SECRET_KEY)
        try:
            data = serializer.loads(bytes(token, encoding="utf-8"))
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = User.query.get(data["id"])
        return user
