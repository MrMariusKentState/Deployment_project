from flask_app.config.MySQLconnect import MySQLConnection
from flask import flash
from flask_app.models.recipe import Recipe
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 


class Login:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.confirm_password = data['confirm_password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.recipes = []


    @staticmethod
    def register(user):
            is_valid = True
            if len(user['fname']) < 2:
                flash("Your first name must be at least 2 letters in length.")
                is_valid = False
            if len(user['lname']) < 2:
                flash("Your last name must be at least 2 letters in length.")
                is_valid = False
            if user['fname'].isalpha() == False:
                flash("Your first name must be comprised of letters only.")
                is_valid = False
            if user['lname'].isalpha() == False:
                flash("Your last name must be comprised of letters only.")
                is_valid = False
            if not EMAIL_REGEX.match(user['email']): 
                flash("The email address you have provided is invalid.")
                is_valid = False
            if len(user['password']) < 8:
                flash("Your password must be at least 8 characters in length.")
                is_valid = False
            query = "SELECT * From user WHERE email = %(email)s;"
            results = MySQLConnection('user').query_db( query, user )
            if len(results) > 0:
                flash("You must register with a different email address.");
                is_valid = False;
            query = "SELECT * From user WHERE password = %(password)s;"
            results = MySQLConnection('user').query_db( query, user )
            if len(results) > 0:
                flash("This password is not available.  Please choose a different password.");
                is_valid = False;
            if user['password'] != user['cpassword']:
                flash("Your password and password confirmation must match.")
                is_valid = False;
            return is_valid


    @classmethod
    def save(cls, data ):
            query = "INSERT INTO user (first_name, last_name, email, password, confirm_password, created_at, updated_at ) VALUES ( %(fname)s, %(lname)s, %(email)s , %(password)s, %(cpassword)s, NOW() , NOW() );"
            return MySQLConnection('user').query_db( query, data )


    @classmethod
    def get_by_email(cls,data):
            query = "SELECT * FROM user WHERE email = %(email)s;"
            result = MySQLConnection('user').query_db(query,data)
            # Didn't find a matching user
            if len(result) < 1:
                return False
            return cls(result[0])


    @classmethod
    def get_user(cls, data):
            query = "SELECT * FROM user WHERE id = %(id)s;"
            result = MySQLConnection('user').query_db(query,data)
            return cls(result[0])



    @classmethod
    def get_user_with_recipes(cls, data):
        query = "SELECT * FROM user LEFT JOIN recipes ON recipes.user_id = user.id WHERE user.id = %(id)s;"
        results = MySQLConnection('user').query_db(query,data)
        recipe = cls(results[0])
        for row in results:
            print(row)
            recipe_data = {
                "id": row['recipes.id'],
                "name": row['recipes.name'],
                "description": row['recipes.description'],
                "minutes": row['recipes.30_minutes'],
                "instructions": row['recipes.instructions'],
                "created_at": row['recipes.created_at'],
                "updated_at":row['recipes.updated_at'],
                "user_id": row['recipes.user_id']
            }
        recipe.recipes.append(recipe.Recipe(recipe_data))
        return recipe


      