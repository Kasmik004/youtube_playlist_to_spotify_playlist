from flask import Flask
import os

from routes.main import main


app =  Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SECRET_KEY'] = os.urandom(64)


app.register_blueprint(main)





if __name__ == '__main__':
    app.run(debug=True)