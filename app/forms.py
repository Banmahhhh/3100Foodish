from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FloatField, DateTimeField, IntegerField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class DishForm(FlaskForm):
    dishName = StringField('Dish name', validators=[DataRequired()])
    dishPrice = FloatField('Dish price', validators=[DataRequired()])
    dishPhoto = StringField('Dish photo link', validators=[DataRequired()])
    dishDeliveryTime = DateTimeField('Delivery time', validators=[DataRequired()])
    dishExpectedOrderNumber = IntegerField('Expected order number', validators=[DataRequired()])
    dishFlavour=StringField('Dish flavour', validators=[DataRequired()])
    dishTaboo=StringField('Potential taboo', validators=[DataRequired()])
    dishDescription = TextAreaField('Dish description', validators=[Length(min=1, max=200)])
    dishPickUpLocation = TextAreaField('Dish pick up location', validators=[Length(min=1, max=140)])
    submit = SubmitField('Submit')

class OrderForm(FlaskForm):
    quantity = IntegerField('The quantity you want to order:', validators=[DataRequired()])
    contact = StringField('Your contact number:', validators=[DataRequired()])
    submit = SubmitField('Submit')

class SearchBox(FlaskForm):
    content = StringField('Search by food tags:', validators=[DataRequired()])
    submit = SubmitField('Search')

class EditProfileForm(FlaskForm):
    username = StringField('Username:', validators=[DataRequired()])
    head_portrait = StringField('image link of your head portrait:')
    self_introduction = TextAreaField('self introduction:', validators=[Length(min=0, max=400)])
    submit = SubmitField('Submit')

