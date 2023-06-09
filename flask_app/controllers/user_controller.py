from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.user_model import User
from flask_app.models.ticket_model import Ticket
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    return render_template('/new_user.html')


@app.route('/register', methods=['POST'])
def register():
    if not User.validate_register(request.form):
        return redirect('/')
    data ={
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.save(data)
    session['user_id'] = id
    return redirect('/main')


@app.route('/login',methods=['POST'])
def login():
    user = User.get_by_email(request.form)
    if not user:
        flash("Invalid Email","login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password","login")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/main')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/main')
def display_main():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    return render_template('main_page.html', user = User.get_by_id (data))


@app.route('/user/profile/<int:id>')
def show_user_profile(id):
    return render_template('/show_user_profile.html', user = User.get_by_id ({'id':id}))


@app.route('/user/edit/<int:id>')
def show_edit_user(id):
    return render_template('/show_edit_user.html', user = User.get_by_id ({'id':id}))


@app.route('/user/update', methods=['POST'])
def update():
    User.update(request.form)
    return redirect('/user/profile/<int:id>')