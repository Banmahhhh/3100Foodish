from flask import render_template, flash, redirect
from app import app, db
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user
from app.models import User, Dish, Order
from flask_login import login_required
from flask import request, url_for
from werkzeug.urls import url_parse
from app.forms import RegistrationForm, DishForm, OrderForm, SearchBox, EditProfileForm


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    dishes=Dish.query.all()
    form=SearchBox()
    if form.validate_on_submit():
        results = Dish.query.filter(Dish.dish_name.like("%"+form.content.data+"%")).all()
        if results == []:
            flash('No results match.')
        else:
            return render_template('search.html', title='Home', results=results)
    return render_template('index.html', title='Home', dishes=dishes, form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/post_dish', methods=['GET', 'POST'])
@login_required
def post_dish():
    form = DishForm()
    if form.validate_on_submit():
        dish = Dish(dish_name=form.dishName.data, price=form.dishPrice.data,
        photo=form.dishPhoto.data, deliveryTime=form.dishDeliveryTime.data,
        expected_order_number=form.dishExpectedOrderNumber.data, current_order_number=0,
        rating=0, flavour=form.dishFlavour.data, 
        potential_taboo=form.dishTaboo.data, description=form.dishDescription.data,
        pick_up_location=form.dishPickUpLocation.data, seller=current_user)
        db.session.add(dish)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('post_dish.html', title='Post a dish', form=form)

@app.route('/dish_info/<dishname>')
@login_required
def dish_info(dishname):
    dish = Dish.query.filter_by(dish_name=dishname).first_or_404()
    return render_template('dish_info.html', dish=dish)

@app.route('/make_order/<dishname>', methods=['GET', 'POST'])
@login_required
def make_order(dishname):
    dish = Dish.query.filter_by(dish_name=dishname).first_or_404()
    form = OrderForm()
    if form.validate_on_submit():
        order = Order(quantity=form.quantity.data,
        status=1, dish=dish, buyer=current_user)
        dish.current_order_number+=1
        db.session.add(order)
        db.session.commit()
        flash('Your order is successful!')
        return redirect(url_for('index'))
    return render_template('order.html', dish=dish, form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)
    
@app.route('/user/chef_dishes/<username>')
@login_required
def chef_dishes(username):
    user = User.query.filter_by(username=username).first_or_404()
    chef_dishes = Dish.query.join(User).filter(User.username==username).all()
    return render_template('user.html', user=user, chef_dishes=chef_dishes)

@app.route('/user/customer_orders/<username>')
@login_required
def customer_orders(username):
    user = User.query.filter_by(username=username).first_or_404()
    orders = Order.query.join(User).filter(User.username==username).all()
    return render_template('user.html', user=user, orders=orders)
  
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.head_portrait = form.head_portrait.data
        current_user.self_introduction = form.self_introduction.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.head_portrait.data = current_user.head_portrait  
        form.self_introduction.data = current_user.self_introduction
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)
    
    
