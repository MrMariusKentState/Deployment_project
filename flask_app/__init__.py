from flask import Flask
app = Flask(__name__)
app.secret_key = 'Login!' # set a secret key for security purposes