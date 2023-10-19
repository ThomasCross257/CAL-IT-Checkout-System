from flask import Blueprint, render_template, redirect, url_for, request, session, url_for, flash
import bcrypt
from models.db_model import CheckedOut, db, Laptop, Admin
from app import app
import os

adminBP = Blueprint('admin', __name__, template_folder='templates')

@adminBP.route('/admin-dashboard')
def dashboard():
    if 'admin' not in session:
        return redirect(url_for('admin.login'))
    else:
        return render_template('dashboard.html', laptops=Laptop.query.all())
    
@adminBP.route('/admin-createAdmin', methods=['GET', 'POST'])
def createAdmin():
    if request.method == 'POST':
        password = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
        admin = Admin(username='admin', password=password)
        db.session.add(admin)
        db.session.commit()
        return redirect(url_for('admin.login'))
    else:
        return render_template('createAdmin.html')

@adminBP.route('/admin-login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        adminUser = Admin.query.filter_by(username=request.form['username']).first()
        if adminUser and bcrypt.checkpw(request.form['password'].encode('utf-8'), adminUser.password):
            session['admin'] = True
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid username or password', 'danger')
            return redirect(url_for('admin.login', messages='Invalid username or password'))
    if 'admin' in session:
        return redirect(url_for('admin.dashboard'))
    elif Admin.query.all() == []:
        return redirect(url_for('admin.createAdmin'))
    else:
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
        file = request.files['image']
        year = request.form['year']
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        device = Laptop(tag=tag, serial=serial, name=name, make=make, model=model, image=filename, year=year)
        db.session.add(device)
        db.session.commit()
        return redirect(url_for('admin.dashboard'))
    else:
        return render_template('add_laptop.html')
    
@adminBP.route('/checkoutHistory/<id>')
def checkoutHistory(id):
    laptopHistory = CheckedOut.query.filter_by(laptop_id=id).all()
    return render_template('laptopHistory.html', history = laptopHistory)

@adminBP.route('/delete/<id>', methods=['GET', 'POST'])
def deleteEntry(id):
    # Delete the laptop from the Laptop table
    entry = Laptop.query.get(id)
    db.session.delete(entry)

    # Delete all entries of the laptop from the CheckedOut table
    checked_out_entries = CheckedOut.query.filter(CheckedOut.laptop_id == id).all()
    for checked_out_entry in checked_out_entries:
        db.session.delete(checked_out_entry)

    db.session.commit()
    return redirect(url_for('admin.dashboard'))
