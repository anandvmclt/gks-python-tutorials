
from flask import Flask, render_template, request, redirect, url_for, flash,session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms.validators import DataRequired, Email, Length
from models import User, Contact
from forms import ContactForm, RegistrationForm, LoginForm
from db import db  # Import db from db.py

# Initialize Flask app and configure database
app = Flask(__name__)
app.config['SECRET_KEY'] = 'gksinfotech'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contact.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the db with app context
db.init_app(app)

# Route to list all contacts
@app.route('/')
def index():
    contacts = Contact.query.all()
    return render_template('index.html', contacts=contacts)

# Route to view a contact
# Route to create a new contact
@app.route('/create', methods=['GET', 'POST'])
def create():
    form = ContactForm()
    if form.validate_on_submit():
        new_contact = Contact(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            message=form.message.data
        )
        db.session.add(new_contact)
        db.session.commit()
        flash('Contact created successfully!', 'success')
        return redirect(url_for('index'))
    else:
        # Flash validation errors if form submission fails
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{field}: {error}", 'danger')
    return render_template('create.html', form=form)

# Route to view a contact
@app.route('/view/<int:id>')
def view(id):
    contact = Contact.query.get_or_404(id)
    return render_template('view.html', contact=contact)


# Route to edit a contact
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    contact = Contact.query.get_or_404(id)
    form = ContactForm(obj=contact)
    if form.validate_on_submit():
        contact.name = form.name.data
        contact.email = form.email.data
        contact.phone = form.phone.data
        contact.message = form.message.data
        db.session.commit()
        flash('Contact updated successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('edit.html', form=form, contact=contact)


# Route to delete a contact
@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    contact = Contact.query.get_or_404(id)
    db.session.delete(contact)
    db.session.commit()
    flash('Contact deleted successfully!', 'success')
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful. You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # if user is not None:
        if user and check_password_hash(user.password, form.password.data):
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        flash('Login unsuccessful. Check email and password.', 'danger')
    return render_template('login.html', form=form)


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please log in to access this page.', 'danger')
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session.get('username'))

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


# Initialize database
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)