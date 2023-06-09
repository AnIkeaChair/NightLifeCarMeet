from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.ticket_model import Ticket
from flask_app.controllers.user_controller import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/ticket/new')
def index_ticket():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    return render_template('/create_new_ticket.html', user = User.get_by_id(data))


@app.route('/ticket/show/<int:id>')
def index_one_ticket(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    return render_template('/show_one_ticket.html', ticket = Ticket.get_by_id({'id':id}), user = User.get_by_id(data))


@app.route('/ticket/edit/<int:id>')
def show_edit_ticket(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    return render_template('/edit_ticket.html', ticket = Ticket.get_by_id({'id':id}), user = User.get_by_id(data))


@app.route('/ticket/destroy/<int:id>')
def delete(id):
    data ={
        'id':id
    }
    Ticket.destroy(data)
    return redirect('/tickets')


@app.route('/register/ticket/<int:id>', methods=['POST'])
def register_ticket(id):
    print(request.form)
    if not Ticket.validate_ticket(request.form):
        return redirect(f"/ticket/new")
    data ={
        "user_id": request.form['user_id'],
        "title": request.form['title'],
        "description": request.form['description']
    }
    Ticket.save(data)
    return redirect('/tickets')

@app.route('/update/ticket/<int:id>', methods=['POST'])
def update_ticket(id):
    print(request.form)
    if not Ticket.validate_update_ticket(request.form):
        return redirect(f"/ticket/edit/{id}")
    data ={
        "user_id": request.form['user_id'],
        "title": request.form['title'],
        "description": request.form['description'],
        "id": {id}
    }
    Ticket.update(data)
    return redirect('/tickets')

@app.route('/tickets')
def tickets():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    return render_template('show_tickets.html', user = User.get_by_id(data) , tickets = Ticket.get_all())