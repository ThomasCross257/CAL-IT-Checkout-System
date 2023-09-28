from app import app
from flask import redirect, url_for, render_template, session, request
from admin.admin import adminBP
from models.db_model import db, CheckedOut, Admin
from dotenv import load_dotenv
import os

load_dotenv()

app.register_blueprint(adminBP)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///laptop.db'
db.init_app(app)
app.config['ADMIN_PASS'] = os.getenv('ADMIN_PASS')

print(os.getenv('ADMIN_PASS'))

with app.app_context():
    if not Admin.query.filter_by(username='admin').first():
        admin = Admin(username='admin')
        admin.set_password(os.getenv('ADMIN_PASSWORD'))
        db.session.add(admin)
        db.session.commit()
    else:
        pass

@app.route("/")
def home():
    if 'admin' in session:
        return redirect(url_for('admin.dashboard'))
    else:
        return render_template('index.html')

@app.route("/laptops")
def laptops():
    if 'admin' in session:
        return redirect(url_for('admin.dashboard'))
    else:
        return render_template('laptopList.html')

@app.route("/checkout" , methods=['GET', 'POST'])
def checkout(checkedOut):
    if request.method == 'POST':
        user_fname = request.form['user_fname']
        user_lname = request.form['user_lname']
        user_coyoteID = request.form['user_coyoteID']
        user_address = request.form['user_address']
        checkedOut = CheckedOut(user_fname=user_fname, 
                                user_lname=user_lname, 
                                user_coyoteID=user_coyoteID, 
                                user_address=user_address)
        db.session.add(checkedOut)
        db.session.commit()
        return redirect(url_for('success'))
    return render_template('checkout.html')

@app.route("/success")
def success():
    return render_template('success.html')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)