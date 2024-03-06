from flask import Flask
import os
import dotenv

from routes.main import main

dotenv.load_dotenv()

app =  Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


app.register_blueprint(main)





if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)