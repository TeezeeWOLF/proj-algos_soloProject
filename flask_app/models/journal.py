
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
import re
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models import user
import random

class Journal:
    db = "cheerupbuttercup" #which database are you using for this project
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.journal_content = data['journal_content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.creator = None
        # What changes need to be made above for this project?
        #What needs to be added here for class association?



    # Create Journal Models

    @classmethod
    def create_journal(cls, data):
        query = """
            INSERT INTO journals(title,journal_content, user_id)
            VALUES(%(title)s, %(journal_content)s, %(user_id)s)
            ;"""
        journal_id = connectToMySQL(cls.db).query_db(query, data) 
        return journal_id

    # Read Journal Models
    @classmethod
    def get_all_journal_entries(cls):
        query = """
            SELECT * FROM journals
            ;"""
        results = connectToMySQL(cls.db).query_db(query)
        print(results)
        return results
    
    @classmethod 
    def get_journal_by_id(cls,id):
        data = {'id' : id}
        query = """
            SELECT * 
            FROM journals
            WHERE id = %(id)s
            ;"""
        result = connectToMySQL(cls.db).query_db(query, data)
        return result[0]
    

    @classmethod
    def get_users_journal_entries(cls, id):
        data = {'id' : id}
        query = """
            SELECT * FROM journals
            JOIN users ON journals.user_id = users.id
            WHERE users.id = %(id)s
            ;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        entries = []
        for result in results:
            entries.append(cls(result))
        return entries
    
    @classmethod
    def get_all_prompts_for_journal(cls):
        query = """
            SELECT * FROM prompts;
            ;"""
        results = connectToMySQL(cls.db).query_db(query)
        return random.choice(results)


    @classmethod
    def get_all_affirmations(cls):
        query = """
            SELECT * FROM affirmations;
            ;"""
        results = connectToMySQL(cls.db).query_db(query)
        return random.choice(results)


    # Update Journal Models
    @classmethod
    def edit_entry(cls,data):
        query = """
            UPDATE journals
            SET 
                title = %(title)s,
                journal_content = %(journal_content)s
            WHERE id = %(id)s
            ;"""
        return connectToMySQL(cls.db).query_db(query,data)
        


    # Delete Journal Models
        
    @classmethod
    def delete_entry(cls,id):
        data = {'id' : id}
        query = """
            DELETE 
            FROM journals
            WHERE id = %(id)s
            ;"""
        connectToMySQL(cls.db).query_db(query,data)
        return


    # Validations
        
    @classmethod
    def journal_validations(cls,data):
        is_valid = True
        if len(data['title']) < 1:
            is_valid = False
            flash("Title must not be empty, and be less than 45 characters long")
        return is_valid
