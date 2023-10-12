from app import app
from flask import redirect, url_for, render_template, session, request, send_from_directory, flash
from admin.admin import adminBP
from models.db_model import db, CheckedOut, Laptop
from dotenv import load_dotenv
import os
from datetime import datetime
from sqlalchemy import not_

load_dotenv()

app.register_blueprint(adminBP)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///laptop.db'
db.init_app(app)
app.config['ADMIN_PASS'] = os.getenv('ADMIN_PASS')
app.config['ADMIN_USER'] = os.getenv('ADMIN_USER')
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER')
app.secret_key = os.getenv('SECRET_KEY')
TessPath = os.getenv('TESSPATH')

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
        laptops = Laptop.query.outerjoin(CheckedOut).filter(not_(CheckedOut.id.isnot(None))).all()
        return render_template('laptopList.html', laptops=laptops)
    
@app.route("/laptops/<int:id>")
def laptop(id):
    if 'admin' in session:
        return redirect(url_for('admin.dashboard'))
    else:
        laptop = Laptop.query.get(id)
        return render_template('laptop.html', laptop=laptop)
    
@app.route("/returnLaptop", methods=['GET', 'POST'])
def returnLaptop():
    if request.method == 'POST':
        tagNum = int(request.form['tag'])
        laptop = Laptop.query.filter_by(tag=tagNum).first()
        if laptop:
            inUse = CheckedOut.query.filter_by(laptop_id=laptop.id).first()
            if inUse:
                if inUse.returned == True:
                    return render_template('returnpage.html', error="Laptop is not checked out")
                else:
                    inUse.returned = True
                    db.session.commit()
                    flash('Laptop returned successfully', 'success')
                    return redirect(url_for('returnLaptop', returned=True))
            else:
                return render_template('returnpage.html', error="Laptop is not checked out")
        else:
            return render_template('returnpage.html', error="Laptop does not exist")


    return render_template('returnpage.html')


@app.route("/checkout/<id>" , methods=['GET', 'POST'])
def checkout(id):
    laptop = Laptop.query.get(id)
    if request.method == 'POST':
        user_fname = request.form['user_fname']
        user_lname = request.form['user_lname']
        user_coyoteID = request.form['user_coyoteID']
        returned = request.form['return_date']
        checkedOut = CheckedOut(user_fname=user_fname, 
                                user_lname=user_lname, 
                                user_coyoteID=user_coyoteID, 
                                laptop_id=laptop.id,
                                returned = False,
                                return_date=datetime.strptime(returned, '%Y-%m-%d')
        )
        db.session.add(checkedOut)
        db.session.commit()
        return redirect(url_for('success', returnDate=returned))
    return render_template('checkoutForm.html', laptop=laptop)

@app.route("/success")
def success():
    return render_template('success.html')

@app.route("/uploads/<filename>", methods=['GET', 'POST'])
def uploads(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)