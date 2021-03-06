from flask import render_template, flash, redirect
from app import app, db
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user
from app.models import User, Dish, Order
from flask_login import login_required
from flask import request, url_for
from werkzeug.urls import url_parse
from app.forms import RegistrationForm, DishForm, OrderForm, SearchBox, EditProfileForm, CommentForm
from datetime import datetime
from app.forms import MessageForm
from app.models import Message, Notification, Image
from flask import jsonify
import json
import random
from datetime import datetime
from flask import Response


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    dishes=Dish.query.paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('index', page=dishes.next_num) \
        if dishes.has_next else None
    prev_url = url_for('index', page=dishes.prev_num) \
        if dishes.has_prev else None
    form=SearchBox()
    if form.validate_on_submit():
        results = Dish.query.filter(Dish.dish_name.like("%"+form.content.data+"%")).all()
        if results == []:
            flash('No results match.')
        else:
            return render_template('search.html', title='Home', results=results)
    return render_template('index.html', title='Home', dishes=dishes.items, form=form, next_url=next_url,
                           prev_url=prev_url)

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
        flavour=form.dishFlavour.data, 
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
        status="ongoing", dish=dish, buyer=current_user)
        dish.current_order_number+=1
        db.session.add(order)
        notice="Dear chef %s, you have a new order made by user %s for your dish %s." % (dish.seller.username, current_user.username, dish.dish_name)
        msg=Message(author=None, recipient=dish.seller, body=notice)
        db.session.add(msg)
        dish.seller.add_notification('unread_message_count', dish.seller.new_messages())
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

@app.route('/view_order/<order_id>', methods=['GET','POST'])
@login_required
def view_order(order_id):
    order = Order.query.filter_by(id=int(order_id)).first()
    form = CommentForm()
    if (order.dish.deliveryTime-datetime.now()).seconds > 86400:
        can_cancel=True
    else:
        can_cancel=False
    if form.validate_on_submit():
        order.comment=form.content.data
        db.session.commit()
        flash('Your comment has been saved.')
    return render_template('order_info.html', user=user, order=order, form=form, can_cancel=can_cancel)

@app.route('/cancel_by_customer/<order_id>', methods=['GET','POST'])
@login_required
def cancel_by_customer(order_id):
    order = Order.query.filter_by(id=int(order_id)).first()
    if request.method == 'POST':
        if request.form['submit_button'] == 'Yes':
            db.session.delete(order)
            db.session.commit()
            flash("You have deleted this order.")
        return redirect(url_for('user',username=current_user.username))
    return render_template('confirm_cancel.html')

@app.route('/cancel_by_chef/<dish_id>', methods=['GET','POST'])
@login_required
def cancel_by_chef(dish_id):
    dish = Dish.query.filter_by(id=int(dish_id)).first()
    orders = Order.query.filter_by(dish=dish).all()
    if request.method == 'POST':
        if request.form['submit_button'] == 'Yes':
            for order in orders:
                notice="Dear user %s, your order for dish %s has been cancelled by the chef. Please contact the chef for further information." % (order.buyer.username, dish.dish_name)
                msg=Message(author=None, recipient=order.buyer, body=notice)
                db.session.add(msg)
                order.buyer.add_notification('unread_message_count', order.buyer.new_messages())
                db.session.delete(order)   
            db.session.delete(dish)
            db.session.commit()
            flash("You have deleted this dish.")
        return redirect(url_for('user',username=current_user.username))
    return render_template('confirm_cancel.html')

@app.route('/send_message/<recipient>', methods=['GET', 'POST'])
@login_required
def send_message(recipient):
    user = User.query.filter_by(username=recipient).first_or_404()
    form = MessageForm()
    if form.validate_on_submit():
        msg = Message(author=current_user, recipient=user,
                      body=form.message.data)
        db.session.add(msg)
        user.add_notification('unread_message_count', user.new_messages())
        db.session.commit()
        flash('Your message has been sent.')
        return redirect(url_for('user', username=recipient))
    return render_template('send_message.html', title='Send Message',
                           form=form, recipient=recipient)

@app.route('/messages')
@login_required
def messages():
    current_user.last_message_read_time = datetime.utcnow()
    current_user.add_notification('unread_message_count', 0)
    db.session.commit()
    page = request.args.get('page', 1, type=int)
    messages = current_user.messages_received.order_by(
        Message.timestamp.desc()).paginate(
            page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('messages', page=messages.next_num) \
        if messages.has_next else None
    prev_url = url_for('messages', page=messages.prev_num) \
        if messages.has_prev else None
    return render_template('messages.html', messages=messages.items,
                           next_url=next_url, prev_url=prev_url)

@app.route('/notifications')
@login_required
def notifications():
    since = request.args.get('since', 0.0, type=float)
    notifications = current_user.notifications.filter(
        Notification.timestamp > since).order_by(Notification.timestamp.asc())
    return jsonify([{
        'name': n.name,
        'data': n.get_data(),
        'timestamp': n.timestamp
    } for n in notifications])

@app.route('/rating/<order_id>', methods=['POST'])
@login_required
def rating(order_id):
    order=Order.query.filter_by(id=order_id).first()
    order.order_rating=int(request.form['rating_button'])
    db.session.commit()
    orders=Order.query.filter_by(dish=order.dish).all()
    ratings=0
    cnt=0
    for o in orders:
        if o.order_rating is not None:
            ratings+=o.order_rating
            cnt+=1
    if cnt!=0:
        order.dish.rating=ratings/cnt
    db.session.commit()

    chef=order.dish.seller
    dishes=Dish.query.filter_by(seller=chef).all()
    ratings=0
    cnt=0
    for d in dishes:
        if d.rating is not None:
            ratings+=d.rating
            cnt+=1
    if cnt!=0:
        chef.rating=ratings/cnt
    db.session.commit()
    return redirect(url_for('view_order',order_id=order_id))


@app.route('/api/userregister/', methods=['POST'])
def userregister():
    data = request.data
    data = json.loads(data)
    username=data['username']
    password=data['password']
    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return Response(status=201)


@app.route('/logintoken/', methods=['POST'])
def logintoken():
    data={"token":'abc'}
    return jsonify(data)


@app.route('/api/users/<id>/', methods=['GET','PATCH'])
def users(id):
    user = User.query.filter_by(id=int(id)).first()
    if request.method == 'PATCH':
        data = request.data
        data = json.loads(data)
        last_name= data.get('last_name')
        image_url= data.get('image_url')
        if last_name is not None:
            user.username=last_name
        if image_url is not None:
            user.image_url=image_url
        db.session.commit()
    else:
        data=user.encode_partial()
    response = Response(json.dumps(data), mimetype='application/json')
    return response

@app.route('/api/users/', methods=['GET'])
def list_users():
    username=request.args.get("username")
    users = User.query.filter_by(username=username).all()
    data=[]
    for user in users:
        data.append(user.encode_all())
    response = Response(json.dumps(data), mimetype='application/json')
    return response

@app.route('/api/books/', methods=['GET','POST'])
def books():
    if request.method == 'POST':
        data = request.data
        data = json.loads(data)
        dish_id = data['food']
        user_id = data['user']
        buyer = User.query.filter_by(id=int(user_id)).first()
        dish = Dish.query.filter_by(id=int(dish_id)).first()
        order = Order(quantity=0,
        status="ongoing", dish=dish, buyer=buyer)
        dish.current_order_number+=1
        db.session.add(order)
        db.session.commit()
    else:
        user_id=request.args.get('user')
        data=[]
        buyer = User.query.filter_by(id=int(user_id)).first()
        orders = Order.query.filter_by(buyer=buyer).all()
        for order in orders:
            data.append(order.encode_book())
    response = Response(json.dumps(data), mimetype='application/json')
    return response
    

@app.route('/api/books/<id>/', methods=['DELETE'])
def delete_books(id):
    data=request.data
    order = Order.query.filter_by(id=int(id)).first()
    db.session.delete(order)
    db.session.commit()
    response = Response(data, mimetype='application/json')
    return response

@app.route('/api/foods/', methods=['GET', 'POST'])
def post_foods():
    if request.method == 'POST':
        data = request.data
        data = json.loads(data)
        image_url=data['image_url']
        name=data['name']
        price=data['price']
        place=data['place']
        date=data['date']
        max_book=data['max_book']
        content=data['content']
        book_now=data['book_now']
        diet=data['diet']
        style=data['style']
        author=data['author']

        chef = User.query.filter_by(id = int(author)).first()
        dish = Dish(dish_name=name, 
        price=float(price),
        photo=image_url, 
        expected_order_number=int(max_book),
        deliveryTime=date,
        current_order_number=int(book_now),
        flavour=style, 
        potential_taboo=diet, 
        description=content,
        pick_up_location=place, 
        seller=chef)
        db.session.add(dish)
        db.session.commit()
    else:
        dataDict = request.data
        dataDict = json.loads(dataDict)
        chef_id = dataDict['author']
        chef = User.query.filter_by(id=int(chef_id)).first()
        data=[]
        dishes = Dish.query.filter_by(seller=chef).all()
        for dish in dishes:
            data.append(dish.encode())
    response = Response(json.dumps(data), mimetype='application/json')
    return response
    
@app.route('/api/foods/<id>/', methods=['GET','PUT'])
def foods(id):
    dish = Dish.query.filter_by(id = int(id)).first()
    if request.method == 'PUT':
        data = request.data
        data = json.loads(data)
        db.session.delete(dish)
        db.session.commit()
    else:
        data=dish.encode()
    response = Response(json.dumps(data), mimetype='application/json')
    return response





@app.route('/api/comments/', methods=['GET', 'POST'])
def comments():
    if request.method == 'POST':
        data = request.data
        data = json.loads(data)
        description=data['description']
        score=data['score']
        auther=data['auther']
        food=data['food']
        dish = Dish.query.filter_by(id = int(food)).first()
        user = User.query.filter_by(id = int(auther)).first()
        order = Order.query.filter_by(dish=dish, buyer=user).first()
        order.comment=description
        order.rating=int(score)
        db.session.commit()
    else:
        food=request.args.get('food')
        dish = Dish.query.filter_by(id = int(food)).first()
        orders = Order.query.filter_by(dish=dish).all()
        data=[]
        for order in orders:
            data.append(order.encode_comment())
    response = Response(json.dumps(data), mimetype='application/json')
    return response

@app.route('/<name>', methods=['GET'])
def get_img(name):
    img = Image.query.filter_by(image_name= name).first()
    data= img.image_data
    response = Response(data, mimetype='application/octet-stream')
    return response

@app.route('/upload/image/', methods=['POST'])
def images():
    f = request.files['img']
    image_data=request.data
    name=f.filename
    image = Image(image_name = name, image_data=image_data)
    db.session.add(image)
    db.session.commit()
    data = {'url': name}
    response = Response(json.dumps(data), mimetype='application/json', status=201)
    return response

@app.route('/api/recommend/', methods=['GET', 'POST'])
def recommend():
    dishes=Dish.query.all()
    dishes=random.choices(dishes)
    data=[]
    for dish in dishes:
        data.append(dish.encode())
    response = Response(json.dumps(data), mimetype='application/json')
    return response






    
    
   
    
    
    
    
