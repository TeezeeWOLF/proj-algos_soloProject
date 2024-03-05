
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session,request
import re
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
# The above is used when we do login registration, flask-bcrypt should already be in your env check the pipfile

# Remember 'fat models, skinny controllers' more logic should go in here rather than in your controller. Your controller should be able to just call a function from the model for what it needs, ideally.

class User:
    db = "cheerupbuttercup" #which database are you using for this project
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        # What changes need to be made above for this project?
        #What needs to be added here for class association?



    # Create Users Models
    @classmethod
    def create_users(cls, user_data):
        if not cls.validate_user_data(user_data): return False
        user_data = user_data.copy()
        user_data = { 
            "first_name" : request
        }
        user_data['password'] = bcrypt.generate_password_hash(user_data['password'])
        query = """
        INSERT INTO users(first_name,last_name,email, password)
        VALUES (%(first_name)s,%(last_name)s,%(email)s, %(password)s)
        """
        user_id = connectToMySQL(cls.db).query_db(query, user_data)
        session['user_id'] = user_id
        session['user_name'] = f'{user_data["first_name"]} {user_data["last_name"]}'
        return user_id
        


    # Read Users Models

    @classmethod
    def get_user_by_id(cls,id):
        data = {"id" : id}
        query = """ 
            SELECT * FROM users
            WHERE id = %(id)s
            ;"""
        result = connectToMySQL(cls.db).query_db(query, data)
        return cls(result[0])
    
    @classmethod
    def get_all_users(cls):
        query = """
            SELECT * FROM users
            ;"""
        results = connectToMySQL(cls.db).query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
        return users
        



    @classmethod
    def get_user_by_email(cls, email):
        data = {'email' : email}
        query = """
            SELECT * FROM users
            WHERE email = %(email)s
            ;"""
        user_email = connectToMySQL(cls.db).query_db(query, data)
        if user_email:
            return cls(user_email[0])
        return False

    # Update Users Models



    # Delete Users Models


    #login
    @classmethod
    def login(cls, data):
        this_user = cls.get_user_by_email(data['email'])
        if this_user:
            if bcrypt.check_password_hash(this_user.password, data['password']):
                session['user_id'] = this_user.id
                session['user_name'] = f'{this_user.first_name} {this_user.last_name}'
                return True
        flash("Your login information was incorrect.")
        return False
    # Validations

    @classmethod
    def validate_user_data(cls, data):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        is_valid = True
        if len(data['first_name']) < 1: 
            is_valid = False
            flash("Name field cannot be empty")
        if len(data['last_name']) < 1:
            is_valid = False
            flash("Last name cannot be empty")
        if len(data['password']) < 8:
            is_valid = False
            flash('Your password must be at least 8 characters long')
        if data['password'] != data['confirm_password']:
            is_valid = False
            flash('Passwords do not match')
        if not EMAIL_REGEX.match(data['email']):
            is_valid = False
            flash('Please use valid email.')
        if cls.get_user_by_email(data['email']):
            is_valid = False
            flash('email already in use.')
        return is_valid       
