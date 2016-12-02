from bucket_list import app
from bucket_list.models import db, User
from flask import render_template, json, request

# define the basic route and corresponding request handler
@app.route("/")
@app.route("/main")
def main():
    return render_template('index.html')

@app.route('/testdb')
def testdb():
    if db.session.query("1").from_statement("SELECT 1").all():
        return "DB workds"
    else:
        return "DB not connected"


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

    new_user = User(_name, _email, _password)
    db.session.add(new_user)
    db.session.commit()

    # validate received values
    if _name and _email and _password:
        return json.dumps({
            'html': '<span>All fields good !!</span>'
        })
    else:
        return json.dumps({
            'html': '<span>Enter the required fields !!</span>'
        })

# check if the executed file is the main program and run the bucket_list
if __name__ == "__main__":
    app.run()
