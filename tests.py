import unittest
from app import app, db
from app.models import User, Dish, Order

class UserModelCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_chef_dish(self):
        u1 = User(username='A')
        u2 = User(username='B')
        d1 = Dish(dish_name='rice')
        d2 = Dish(dish_name='noodles')
        d3 = Dish(dish_name='beef')
        d4 = Dish(dish_name='pork')
        d1.seller=u1
        d2.seller=u1
        d3.seller=u2
        d4.seller=u2
        db.session.add(u1)
        db.session.add(u2)
        db.session.add(d1)
        db.session.add(d2)
        db.session.add(d3)
        db.session.add(d4)
        db.session.commit()
        
        chef1=User.query.filter_by(username='A').first()
        chef2=User.query.filter_by(username='B').first()
        dish1=Dish.query.filter_by(dish_name='rice').first()
        dish2=Dish.query.filter_by(dish_name='noodles').first()
        dish3=Dish.query.filter_by(dish_name='beef').first()
        dish4=Dish.query.filter_by(dish_name='pork').first()
        self.assertEqual(chef1.sales_history.all(), [dish1,dish2])
        self.assertEqual(chef2.sales_history.all(), [dish3,dish4])

    def test_customer_order(self):
        u1 = User(username='A')
        u2 = User(username='B')
        d1 = Dish(dish_name='rice')
        d2 = Dish(dish_name='noodles')
        d3 = Dish(dish_name='beef')
        d4 = Dish(dish_name='pork')
        d1.seller=u1
        d2.seller=u1
        d3.seller=u2
        d4.seller=u2
        db.session.add(u1)
        db.session.add(u2)
        db.session.add(d1)
        db.session.add(d2)
        db.session.add(d3)
        db.session.add(d4)
        db.session.commit()

        u3 = User(username='a')
        u4 = User(username='b')
        o1 = Order(dish=d2,buyer=u3)
        o2 = Order(dish=d3,buyer=u3)
        o3 = Order(dish=d3,buyer=u4)
        o4 = Order(dish=d4,buyer=u4)
        db.session.add(u3)
        db.session.add(u4)
        db.session.add(o1)
        db.session.add(o2)
        db.session.add(o3)
        db.session.add(o4)
        db.session.commit()

        self.assertEqual(u3.purchasing_history.all(), [o1,o2])
        self.assertEqual(u4.purchasing_history.all(), [o3,o4])
        self.assertEqual(d1.order_lists.all(), [])
        self.assertEqual(d2.order_lists.all(), [o1])
        self.assertEqual(d3.order_lists.all(), [o2,o3])
        self.assertEqual(d4.order_lists.all(), [o4])

        
if __name__ == '__main__':
    unittest.main(verbosity=2)