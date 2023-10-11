from flask import Blueprint, render_template, redirect, url_for, request, session, url_for, flash
from models.db_model import CheckedOut, db, Laptop
from app import app

adminBP = Blueprint('admin', __name__, template_folder='templates')

@adminBP.route('/admin-dashboard')
def dashboard():
    if 'admin' not in session:
        return redirect(url_for('admin.login'))
    else:
        return render_template('dashboard.html', laptops=Laptop.query.all())

@adminBP.route('/admin-login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == app.config['ADMIN_USER'] and request.form['password'] == app.config['ADMIN_PASS']:
            session['admin'] = True
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid username or password', 'danger')
            return redirect(url_for('admin.login'))
    return render_template('login.html')

@adminBP.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('admin.login'))

@adminBP.route('/add_laptop', methods=['GET', 'POST'])
def add_laptop():
    if request.method == 'POST':
        tag = request.form['tag']
        serial = request.form['serial']
        name = request.form['name']
        make = request.form['make']
        model = request.form['model']
        image = request.form['image']
        device = Laptop(tag=tag, serial=serial, name=name, make=make, model=model, image=image)
        db.session.add(device)
        db.session.commit()
        return redirect(url_for('admin.dashboard'))
    else:
        return render_template('add_laptop.html')
    
@adminBP.route('/checkoutHistory/<id>')
def checkoutHistory(id):
    laptopHistory = CheckedOut.query.filter_by(laptop_id=id).all()
    return render_template('laptopHistory.html', history = laptopHistory)