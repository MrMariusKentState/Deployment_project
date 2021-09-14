from flask import render_template, request, redirect, session, flash
from flask_app.models.user import Login
from flask_app.models.recipe import Recipe

from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/register/user', methods=['POST'])
def register():
    if not Login.register(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    # put the pw_hash into the data dictionary
    data = {
        "fname": request.form['fname'],
        "lname": request.form['lname'],
        "email": request.form['email'],
        "password" : pw_hash,
        "cpassword": pw_hash
    }
    # Call the save @classmethod on User
    user_id = Login.save(data)
    # store user id into session
    session['user_id'] = user_id
    flash("Your registration has been successful!  Please login to continue.")
    return render_template("index.html")



@app.route('/login', methods=['POST'])
def login():
    # see if the username provided exists in the database
    data = { "email" : request.form['loginemail'] }
    user_in_db = Login.get_by_email(data)
    # user is not registered in the db
    if not user_in_db:
        flash("Invalid Email/Password. Please try again.")
        return redirect('/next')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['loginpassword']):
        # if we get False after checking the password
        flash("Invalid Email/Password. Please try again.")
        return redirect('/next')
    # if the passwords matched, we set the user_id into session
    session['user_id'] = user_in_db.id
    # never render on a post!!!
    return redirect('/dashboard')


@app.route('/dashboard')
def dashboard():
    if "user_id" not in session:
        return redirect ('/')
    data = {
        "id": session["user_id"]
    }
    user = Login.get_user(data)
    recipes = Recipe.get_all_recipe_names()
    return render_template("dashboard.html", user = user, recipes = recipes)




#The dashboard page functions:

@app.route('/recipes/new')
def create():
    if "user_id" not in session:
        return redirect ('/')
    data = {
        "id": session["user_id"]
    }
    user = Login.get_user(data)
    return render_template("addrecipe.html", user = user)



@app.route('/logout')
def logout():
    session.clear()
    return redirect ('/')



@app.route('/create/recipe/<int:user_id>', methods = ['POST'])
def add_recipe(user_id):
    if "user_id" not in session:
        return redirect ('/')
    if not Recipe.validate_recipe(request.form):
        return redirect('/recipes/new')
    data = {
        "name": request.form['rname'],
        "description": request.form['description'],
        "instructions": request.form['instructions'],
        "user_id": user_id,
        "created_at": request.form['datemade'],
        "30minutes": request.form['radio']
    }
    Recipe.add_recipe(data)
    flash("Your recipe has been added!  It is now posted on the dashboard.")
    return redirect ('/recipes/new')



@app.route('/recipes/<int:item_id>')
def instructions(item_id):
    if "user_id" not in session:
        return redirect ('/')
    data = {
        "id": session["user_id"]
    }
    data2 = {
        "id": item_id
    }
    user = Login.get_user(data)
    recipe = Recipe.get_recipe(data2)
    return render_template("welcome.html", recipe = recipe, user = user)


@app.route('/recipes/edit/<int:item_id>')
def edit(item_id):
    if "user_id" not in session:
        return redirect ('/')
    data = {
        "id": session["user_id"]
    }
    data2 = {
        "id": item_id
    }
    user = Login.get_user(data)
    recipe = Recipe.get_recipe(data2)
    print(recipe.created_at)
    return render_template("editrecipe.html", recipe = recipe, user = user)


@app.route('/recipes/edit/submit/<int:recipe_id>', methods = ['POST'])
def submit_edits(recipe_id):
    data = {
        "name": request.form['rname'],
        "description": request.form['description'],
        "instructions": request.form['instructions'],
        "created_at": request.form['datemade'],
        "30minutes": request.form['radio'],
        "id": recipe_id
    }
    Recipe.edit_recipe(data)
    print("test again")
    return redirect('/dashboard')



@app.route('/recipes/delete/<int:item_id>')
def delete(item_id):
    if "user_id" not in session:
        return redirect ('/')
    data = {
        "id": item_id
    }
    Recipe.delete_recipe(data)
    return redirect ('/dashboard')




