from random import randint
from flask import Flask, render_template, redirect, session, request
app = Flask(__name__)
app.secret_key = 'super secret'

@app.route('/')
def hello_world():

    return render_template('index.html')


@app.route('/destroy_session', methods=['POST'])
def destroy_session():
    session.clear()
    return redirect('/')

if __name__=="__main__":
    app.run(debug=True)