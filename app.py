from flask import Flask, render_template, json, request
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/bucketlist'
db = SQLAlchemy(app)

# define the basic route and corresponding request handler
@app.route("/")
def main():
    return render_template('index.html')


@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')


# routing for user signup
@app.route('/signUp', methods=['POST'])
def signUp():
    # function for creating user
    # read posted values from UI
    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']

    # validate received values
    if _name and _email and _password:
        return json.dumps({
            'html': '<span>All fields good !!</span>'
        })
    else:
        return json.dumps({
            'html': '<span>Enter the required fields !!</span>'
        })

# check if the executed file is the main program and run the app
if __name__ == "__main__":
    app.run()

