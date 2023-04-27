from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from .user_model import User


class Ticket:
    db = "NightLifeCarMeetDB"
    def __init__(self,data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.title = data['title']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None

    @classmethod
    def save(cls, data):
        query = "INSERT INTO tickets (user_id, title, description) VALUES (%(user_id)s , %(title)s , %(description)s);"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def update(cls, data):
        query = "UPDATE tickets SET user_id=%(user_id)s , title=%(title)s , description=%(description)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM tickets WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM tickets LEFT JOIN users ON tickets.user_id = users.id WHERE tickets.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        ticket = cls(results[0])
        for t in results:
            u = {
                'id': t['users.id'],
                'first_name': t['first_name'],
                'last_name': t['last_name'],
                'email': t['email'],
                'password': t['password'],
                'created_at': t['users.created_at'],
                'updated_at': t['users.updated_at'],
            }
            ticket.creator = User(u)
        return ticket

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM tickets LEFT JOIN users ON tickets.user_id = users.id;"
        results = connectToMySQL(cls.db).query_db(query)
        tickets = []
        for t in results:
            ticket = cls(t)
            u = {
                'id': t['users.id'],
                'first_name': t['first_name'],
                'last_name': t['last_name'],
                'email': t['email'],
                'password': t['password'],
                'created_at': t['users.created_at'],
                'updated_at': t['users.updated_at'],
            }
            ticket.creator = User(u)
            tickets.append(ticket)
        return tickets

    @staticmethod
    def validate_ticket(recipe):
        is_valid = True
        query = "SELECT * FROM tickets WHERE title = %(title)s;"
        results = connectToMySQL(Ticket.db).query_db(query,recipe)
        if len(results) >0:
            flash("This ticket has already been registered.","register ticket")
            is_valid = False
        if len(recipe['title']) < 3:
            flash("Title must be at least 3 characters.","register ticket")
            is_valid = False
        if len(recipe['description']) < 3:
            flash("Description must be at least 3 characters.","register ticket")
            is_valid = False
        return is_valid

    @staticmethod
    def validate_update_ticket(recipe):
        is_valid = True
        query = "SELECT * FROM tickets WHERE title = %(title)s;"
        results = connectToMySQL(Ticket.db).query_db(query,recipe)
        if len(recipe['title']) < 3:
            flash("Name must be at least 3 characters.","update ticket")
            is_valid = False
        if len(recipe['description']) < 3:
            flash("Description must be at least 3 characters.","update ticket")
            is_valid = False
        return is_valid