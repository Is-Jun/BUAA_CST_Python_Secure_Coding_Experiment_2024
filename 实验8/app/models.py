from werkzeug.security import generate_password_hash, check_password_hash
from . import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    real_name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, default=30)
    gender = db.Column(db.String(10), default='Male')
    phone = db.Column(db.String(20), default='')
    email = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), default='')

    def is_active(self):
        return True

    def is_admin(self):
        return self.role == 'admin'

    def get_id(self):
        return str(self.id)

    @property
    def is_authenticated(self):
        return True  # 或者根据你的业务逻辑返回一个适当的值

    def __repr__(self):
        return f"User('{self.username}', '{self.role}', '{self.real_name}', '{self.email}')"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
