from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
import json
from time import time

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    self_introduction = db.Column(db.Text)
    rating=db.Column(db.Integer)
    head_portrait = db.Column(db.String(200))
    sales_history=db.relationship('Dish', backref='seller', lazy='dynamic')
    purchasing_history=db.relationship('Order', backref='buyer', lazy='dynamic')
    messages_sent = db.relationship('Message',
                                    foreign_keys='Message.sender_id',
                                    backref='author', lazy='dynamic')
    messages_received = db.relationship('Message',
                                        foreign_keys='Message.recipient_id',
                                        backref='recipient', lazy='dynamic')
    last_message_read_time = db.Column(db.DateTime)
    notifications = db.relationship('Notification', backref='user',
                                    lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def new_messages(self):
        last_read_time = self.last_message_read_time or datetime(1900, 1, 1)
        return Message.query.filter_by(recipient=self).filter(
            Message.timestamp > last_read_time).count()

    def add_notification(self, name, data):
        self.notifications.filter_by(name=name).delete()
        n = Notification(name=name, payload_json=json.dumps(data), user=self)
        db.session.add(n)
        return n
    
    def encode_all(self):
        data={
        "id":self.id,
        "isStop": False,
        "username": self.username,
        "password": self.password_hash,
        "image_url": self.head_portrait #not sure!
        }
        return data
    
    def encode_partial(self):
        data={
        "id":self.id, 
        "last_name": self.username,
        "image_url": self.head_portrait #not sure!
        }
        return data


class Dish(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dish_name = db.Column(db.String(50))
    price = db.Column(db.Float)
    photo = db.Column(db.String(200))
    deliveryTime = db.Column(db.String(140))
    expected_order_number = db.Column(db.Integer)
    current_order_number = db.Column(db.Integer)
    rating = db.Column(db.Integer)
    flavour = db.Column(db.String(140))
    potential_taboo=db.Column(db.String(500))
    description = db.Column(db.Text)
    pick_up_location=db.Column(db.String(500))
    chef_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    order_lists=db.relationship('Order', backref='dish', lazy='dynamic')
    
    def __repr__(self):
        return '<Dish {}>'.format(self.dish_name)  
    
    def encode(self):

        data={
        "id":self.id,
        "name": self.dish_name,
        "price":self.price,
        "place":self.pick_up_location,
        'date':self.deliveryTime,
        'max_book':self.expected_order_number,
        'content':self.description,
        'book_now':self.current_order_number,
        'diet':self.potential_taboo,
        'style':self.flavour,
        'author':self.seller.username
        }
        return data
    
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity=db.Column(db.Integer)
    order_time=db.Column(db.DateTime, index=True, default=datetime.utcnow)
    status=db.Column(db.String(100))
    comment=db.Column(db.Text)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    dish_id = db.Column(db.Integer, db.ForeignKey('dish.id'))
    order_rating=db.Column(db.Integer)
    
    def __repr__(self):
        return '<Order {}>'.format(self.id)
    
    def encode_comment(self):
        data={
            "food_ave_score": self.dish.rating,
            "id": self.id, #not sure
            "auther": self.buyer.username,
            "description": self.comment,
            "food_detail_data": self.dish.description
        }
        return data

    def encode_book(self):
        if self.comment is not None:
            is_comment=True
        else:
            is_comment=False
        data={
            "book_now": self.dish.current_order_number,
            "food": self.dish.dish_name,
            'food_id': self.dish.id,
            "user": self.buyer.username,
            "is_comment": is_comment,
            "food_detail": self.dish.description
        }
        return data
    

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    body = db.Column(db.String(500))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Message {}>'.format(self.body)

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.Float, index=True, default=time)
    payload_json = db.Column(db.Text)

    def get_data(self):
        return json.loads(str(self.payload_json))

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_data = db.Column(db.LargeBinary)
    image_name = db.Column(db.String(1000), index=True)
    

    