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


@app.route('/showAddWish')
def show_add_wish():
    return render_template('addWish.jinja.html')


@app.route('/addWish', methods=['POST'])
def add_wish():
    try:
        if 'user' in session:
            print("user is in session")
            _title = request.form['inputTitle']
            _desc = request.form['inputDescription']
            _user = session.get('user')

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_addWish', (_title, _desc, _user))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return redirect('/userHome')
            else:
                return render_template('error.jinja.html', error = 'An error occured!')
        else:
            return render_template('error.jinja.html', error = 'Unauthorized user')
    except Exception as e:
        return render_template('error.jinja.html', error = str(e))
    finally:
        cursor.close()
        conn.close()


@app.route('/getWish')
def get_wish():
    try:
        if 'user' in session:
            _user = session.get('user')

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_getWishByUser', (_user, ))
            wishes = cursor.fetchall()

            if len(wishes) > 0:
                wishes_dict = []
                for wish in wishes:
                    wishes_dict.append({
                        'id': wish[0],
                        'title': wish[1],
                        'desc': wish[2],
                        'created': wish[4]
                        })
                return json.dumps(wishes_dict)
            else:
                return render_template('error.jinja.html', error = 'User has no wish at all')
        else:
            return render_template('error.jinja.html', error = 'Unauthorized user')
    except Exception as e:
        return render_template('error.jinja.html', error = str(e))
    finally:
        cursor.close()
        conn.close()


@app.route('/getWishById', methods=['POST'])
def get_wish_by_id():
    try:
        if 'user' in session:
            _user = session.get('user')
            _id = request.form['id']

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_getWishById', (_id, _user))
            result = cursor.fetchall()[0]
            print(result)

            wish = []
            wish.append({
                'id': result[0],
                'title': result[1],
                'desc': result[2],
                'created': result[4]
                })

            return json.dumps(wish)
        else:
            return render_template('error.jinja.html', error='Unauthorized user')
    except Exception as e:
        return render_template('error.jinja.html', error = str(e))
    finally:
        cursor.close()
        conn.close()


@app.route('/updateWish', methods=['POST'])
def update_wish():
    try:
        if 'user' in session:
            _user = session.get('user')
            _id = request.form['id']
            _title = request.form['title']
            _desc = request.form['description']

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_updateWish', (_id, _title, _desc, _user))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return json.dumps({'status': 'OK'})
            else:
                return json.dumps({'status': 'ERROR'})
        else:
            return render_template('error.jinja.html', error='Unauthorized user')
    except Exception as e:
        return render_template('error.jinja.html', error = 'Unauthorized access')
    finally:
        cursor.close()
        conn.close()


@app.route('/deleteWish', methods=['POST'])
def delete_wish():
    try:
        if 'user' in session:
            _user = session.get('user')
            _id = request.form['id']

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_deleteWish', (_id, _user))
            result = cursor.fetchall()

            if len(result) is 0:
                conn.commit()
                return json.dumps({'status': 'OK'})
            else:
                return json.dumps({'status': 'An error occured'})
        else:
            return render_template('error.jinja.html', error='Unauthorized access')
    except Exception as e:
        return json.dumps({'status': str(e)})
    finally:
        cursor.close()
        conn.close()


# check if the executed file is the main program and run the bucket_list
# if __name__ == "__main__":
#     app.run()
