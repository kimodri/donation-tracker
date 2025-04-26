from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process', methods = ['POST'])
def process():
    email = request.form.get('email')
    password = request.form.get('password')
    role = request.form.get('role')


@app.route('/thank-you')
def thank_you():
    return render_template('thankyou.html')

