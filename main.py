from app import app
from flask import redirect, url_for, render_template, session

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/checkout")
def checkout():
    return render_template('checkout.html')

if __name__ == "__main__":

    app.run(debug=True)