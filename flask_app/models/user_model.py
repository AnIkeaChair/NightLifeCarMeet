from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    db = "NightLifeCarMeetDB"
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s , %(last_name)s , %(email)s , %(password)s);"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def update(cls, data):
        query = "UPDATE users SET first_name=%(first_name)s, last_name=%(last_name)s , email=%(email)s, password=%(password)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls(results[0])

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db).query_db(query)
        users = []
        for u in results:
            users.append( cls(u) )
        return users


    @staticmethod
    def validate_register(user):
        is_valid = True
        uppers = []
        lowers = []
        numbers = []
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(User.db).query_db(query,user)
        if len(results) >= 1:
            flash("This email has already been taken.","register")
            is_valid=False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email.","register")
            is_valid=False
        if len(user['first_name']) < 3:
            flash("First name must be at least 2 characters.","register")
            is_valid= False
        if len(user['last_name']) < 3:
            flash("Last name must be at least 2 characters.","register")
            is_valid= False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters.","register")
            is_valid = False
        if len(user['confirm_password']) < 1:
            flash("You must confirm your password.","register")
            is_valid = False
        if user['password'] != user['confirm_password']:
            flash("Passwords don't match.","register")
            is_valid = False
        for i in range(len(user['password'])):
            if list(user['password'])[i].isupper() == True:
                uppers.append(list(user['password'])[i])
            if list(user['password'])[i].islower() == True:
                lowers.append(list(user['password'])[i])
            if list(user['password'])[i].isnumeric() == True:
                numbers.append(list(user['password'])[i])
        if len(uppers) < 1:
            flash("Password must contain at least 1 capital letter.","register")
            is_valid = False
        if len(lowers) < 1:
            flash("Password must contain at least 1 lowercase letter.","register")
            is_valid = False
        if len(numbers) < 1:
            flash("Password must contain at least 1 number.","register")
            is_valid = False
        return is_valid

    @staticmethod
    def validate_login(user):
        is_valid = True
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address!","login")
            is_valid = False
        return is_valid