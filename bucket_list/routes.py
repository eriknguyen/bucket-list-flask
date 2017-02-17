from bucket_list import app
from bucket_list.models import db, User
from flask import render_template, json, request, redirect, url_for
from werkzeug import generate_password_hash, check_password_hash

# define the basic route and corresponding request handler


@app.route("/")
@app.route("/home")
def main():
    return render_template('index.jinja.html')


@app.route('/testdb')
def testdb():
    if db.session.query("1").from_statement("SELECT 1").all():
        return "DB workds"
    else:
        return "DB not connected"


@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.jinja.html', error=False)


@app.route('/showSignIn')
def showSignIn():
    return render_template('signin.jinja.html')

# routing for user signup


@app.route('/signUp', methods=['POST'])
def signUp():
    # function for creating user
    # read posted values from UI
    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']
    print("formdata = ", _name, _email, _password)

    check_user = User.query.filter_by(email=_email).all()
    print("check_user = ", check_user)
    if (len(check_user) > 0):
        print("there is some user inside")
        return redirect(url_for('showSignUp', error=True))
    else:
        new_user = User(_name, _email, _password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('main'))


@app.route('/validateLogin', methods=['POST'])
def validateLogin():
    try:
        _username = request.form['inputEmail']
        _password = request.form['inputPassword']

        check_user = User.query.filter_by(email=_username).first()
        if check_user:
            if check_user.check_password(_password):
                return redirect('/userHome')
            else:
                return render_template('error.jinja.html', error='Wrong Email address or password')
        else:
            return render_template('error.jinja.html', error='Wrong email address or password')

    except Exception as e:
        return render_template('error.jinja.html', error=str(e))


@app.route('/userHome')
def userHome():
    return render_template('userHome.jinja.html')

# check if the executed file is the main program and run the bucket_list
if __name__ == "__main__":
    app.run()
