from typing import NoReturn
from flask_app.config.MySQLconnect import MySQLConnection
from flask import flash



class Recipe:
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.minutes = data['30_minutes']
        self.instructions = data['instructions']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    @staticmethod
    def validate_recipe(data):
            is_valid = True
            if len(data['rname']) < 1:
                flash("The recipe name cannot be left blank.")
                is_valid = False
            if len(data['rname']) >= 1 and len(data['rname'])<= 2:
                flash("The recipe name must be at least 3 characters in length.")
                is_valid = False
            if len(data['description']) < 1:
                flash("The description field cannot be left blank.")
                is_valid = False
            if len(data['description']) >= 1 and len(data['description'])<= 2:
                flash("The description must be at least 3 characters in length.")
                is_valid = False
            if len(data['instructions']) < 1:
                flash("The instructions field cannot be left blank.")
                is_valid = False
            if len(data['instructions']) >= 1 and len(data['instructions'])<= 2:
                flash("The instructions field must be at least 3 characters in length.")
                is_valid = False
            return is_valid


    @classmethod
    def add_recipe(cls, data ):
        query = "INSERT INTO recipes (name, description, instructions, created_at, updated_at, user_id, 30_minutes ) VALUES ( %(name)s, %(description)s, %(instructions)s , %(created_at)s , NOW(), %(user_id)s, %(30minutes)s );"
        return MySQLConnection('user').query_db( query, data )

    @classmethod
    def get_all_recipe_names(cls):
        query = "SELECT * FROM recipes";
        results = MySQLConnection('user').query_db( query)
        recipes = []
        for item in results:
            recipes.append(cls(item))
        return recipes

    @classmethod
    def get_recipe(cls, data):
        query = "SELECT * FROM recipes WHERE id = %(id)s";
        result = MySQLConnection('user').query_db(query,data)
        return cls(result[0])


    @classmethod
    def edit_recipe(cls, data):
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, 30_minutes = %(30minutes)s, created_at = %(created_at)s WHERE id = %(id)s";
        print("hope this is successful!")
        return MySQLConnection('user').query_db(query,data)
    

    @classmethod
    def delete_recipe(cls, data):
        query = "DELETE FROM recipes WHERE id = %(id)s";
        return MySQLConnection('user').query_db( query, data )
    
