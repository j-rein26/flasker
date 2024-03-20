from flask import Flask, render_template


#create a flask instance
app = Flask(__name__)


#create a decorater
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




if __name__ == '__main__':
    app.run(debug=True)

