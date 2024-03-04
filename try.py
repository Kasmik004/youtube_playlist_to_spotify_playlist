from flask import Flask, render_template
import os




app =  Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(64)

@app.route('/')
def main():
    try:
        return render_template('hero.html')
    except:
        return render_template('success.html')






if __name__ == '__main__':
    app.run(debug=True)