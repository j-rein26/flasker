from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import os
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from datetime import datetime



#create a flask instance
app = Flask(__name__)

#add database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blogusers.db'

#load dotenv
load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
app.config['SECRET_KEY'] = SECRET_KEY

#initialize Database
db = SQLAlchemy(app)


# Create Model
class BlogUsers(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(200), nullable=False)
	email = db.Column(db.String(120), nullable=False, unique=True)
	date_added = db.Column(db.DateTime, default=datetime.utcnow)

	#Create a string
	def __repr__(self):
		return '<Name %r>' % self.name


with app.app_context():
	db.create_all()


#create a Form Class for Blogusers
class UserForm(FlaskForm):
	name = StringField("Name", validators=[DataRequired()])
	email = StringField("Email", validators=[DataRequired()])
	submit = SubmitField("Submit")

#create a Form Class
class NameForm(FlaskForm):
	name = StringField("What's Your Name", validators=[DataRequired()])
	submit = SubmitField("Submit")

#create a decorate/routes

@app.route("/user/add", methods=['GET', 'POST'])
def add_user():
	name = None
	form = UserForm()
	#validate form
	if form.validate_on_submit():
		user = BlogUsers.query.filter_by(email=form.email.data).first()
		if user is None:
			user = BlogUsers(name=form.name.data, email=form.email.data)
			db.session.add(user)
			db.session.commit()
		name = form.name.data
		form.name.data = ''
		form.email.data = ''
		flash('User Added Successfully')
	our_users = BlogUsers.query.order_by(BlogUsers.date_added)
	return render_template('add_user.html', form=form, name=name, our_users=our_users)

@app.route("/")
def index():
	first_name = "James"
	favorite_pizza= ['pepperoni', 'sauagsage', 'cheese']
	return render_template('index.html', 
		first_name=first_name,
		favorite_pizza=favorite_pizza)


@app.route("/user/<name>")
def user(name):
	return render_template('user.html', user_name=name)

#create custom error pages

#invalid url error page
@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

#internal server error
@app.errorhandler(500)
def internal_server_error(e):
	return render_template('500.html'), 500


#create route to name page
@app.route("/name", methods=['GET', 'POST'])
def name():
	name = None
	form = NameForm()
	#validate form
	if form.validate_on_submit():
		name = form.name.data 
		form.name.data = ''
		flash('Form Submitted Successfully')
	return render_template('name.html', name=name, form=form)


if __name__ == '__main__':
	app.run(debug=True)




    

