from bucket_list import *
from bucket_list.models import db, User
from flask import render_template, json, request, redirect, url_for, session
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

# Option 1: using user model & sqlalchemy
# @app.route('/signUp', methods=['POST'])
# def signUp():
#     # function for creating user
#     # read posted values from UI
#     _name = request.form['inputName']
#     _email = request.form['inputEmail']
#     _password = request.form['inputPassword']
#     print("formdata = ", _name, _email, _password)

#     check_user = User.query.filter_by(email=_email).all()
#     print("check_user = ", check_user)
#     if (len(check_user) > 0):
#         print("there is some user inside")
#         return redirect(url_for('showSignUp', error=True))
#     else:
#         new_user = User(_name, _email, _password)
#         db.session.add(new_user)
#         db.session.commit()
#         return redirect(url_for('main'))

# Option 2: using stored procedure and flask-mysql only
@app.route('/signUp', methods=['POST'])
def signUp():
    # function for creating user
    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']
    _hashed_password = generate_password_hash(_password)
    print("formdata = ", _name, _email, _password, _hashed_password)

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.callproc('sp_createUser', (_name, _email, _hashed_password))

    # if stored procedure is executed successfully, then commit the change and
    # return success message
    data = cursor.fetchall()
    if len(data) is 0:
        conn.commit()
        return json.dumps({'status': 'OK'})
    else:
        return json.dumps({
            'status': 'fail',
            'error': str(data[0])
        })


# to validate user login

# 1. using sqlalchemy and User model
# @app.route('/validateLogin', methods=['POST'])
# def validateLogin():
#     try:
#         _username = request.form['inputEmail']
#         _password = request.form['inputPassword']

#         check_user = User.query.filter_by(email=_username).first()
#         if check_user:
#             if check_user.check_password(_password):
#                 return redirect('/userHome')
#             else:
#                 return render_template('error.jinja.html', error='Wrong Email address or password')
#         else:
#             return render_template('error.jinja.html', error='Wrong email address or password')

#     except Exception as e:
#         return render_template('error.jinja.html', error=str(e))

# 2. using flask-mysql and stored procedure
@app.route('/validateLogin', methods=['POST'])
def validateLogin():
    try:
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        # connect to mysql
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.callproc('sp_validateLogin', (_email, ))
        data = cursor.fetchall()

        if len(data) > 0:
            for item in data:
                print(item)
            if check_password_hash(str(data[0][3]), _password):
                session['user'] = data[0][0]
                return redirect('/userHome')
            else:
                print("Error: ", "Password does not match")
                return render_template('error.jinja.html', error = 'Wrong email address')
        else:
            print("Error: ", "len(data) = 0")
            return render_template('error.jinja.html', error = 'Wrong email address')

    except Exception as e:
        print("Error = ", e)
        return render_template('error.jinja.html', error=str(e))
    finally:
        cursor.close()
        conn.close()


@app.route('/userHome')
def userHome():
    if session.get('user'):
        return render_template('userHome.jinja.html')
    else:
        return render_template('error.jinja.html', error = 'Unauthorized Access')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')


# check if the executed file is the main program and run the bucket_list
if __name__ == "__main__":
    app.run()
