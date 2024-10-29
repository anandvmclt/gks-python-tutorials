
from flask import Flask, render_template, request, redirect, url_for, flash,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length

# Initialize Flask app and configure database
app = Flask(__name__)
app.config['SECRET_KEY'] = 'gksinfotech'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contact.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Contact model
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    message = db.Column(db.String(500), nullable=True)


# Define the Contact form using Flask-WTF
class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=50)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=100)])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(max=20)])
    message = TextAreaField('Message', validators=[DataRequired(), Length(max=500)])
    submit = SubmitField('Submit')


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



# Initialize database
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)