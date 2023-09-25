from flask import Blueprint, render_template, redirect, url_for, request, session, url_for, flash

from app import app

adminBP = Blueprint('admin', __name__, url_prefix='/admin')

@adminBP.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@adminBP.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == app.config['ADMIN_USERNAME'] and request.form['password'] == app.config['ADMIN_PASSWORD']:
            session['admin'] = True
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid username or password', 'danger')
            return redirect(url_for('admin.login'))
    return render_template('login.html')