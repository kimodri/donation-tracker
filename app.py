from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return '<h2>Welcome to DONEate!</h2><br><a href="/thank-you">Make a Donation</a>'

@app.route('/thank-you')
def thank_you():
    return render_template('thankyou.html')

if __name__ == '__main__':
    from werkzeug.serving import run_simple
    run_simple('localhost', 5000, app, use_debugger=True, use_reloader=False)
