from flask import Flask,  render_template, request, redirect, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
# from flask_wtf import FlaskForm
# from wtforms import StringField, TextAreaField, SubmitField
# from wtforms.validators import DataRequired, Email, Length

# Initialize the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'asdff'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contact.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy with the Flask app
db = SQLAlchemy(app)
                        
# Define the Contact model
class Contact(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False)
    message = Column(String(500), nullable=True)

# Define the ContactForm using Flask-WTF
""" 
class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=50)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=100)])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(max=20)])
    message = TextAreaField('Message', validators=[DataRequired(), Length(max=500)])
    submit = SubmitField('Submit')


# Route to display the contact form and handle form submission
@app.route('/', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        # Create a new Contact instance
        new_contact = Contact(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            message=form.message.data
        )
        # Add and commit the new contact to the database
        db.session.add(new_contact)
        db.session.commit()
        flash('Message sent successfully!', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html', form=form)

"""

# Route to create a new contact record
@app.route('/create-contact', methods=['POST', 'GET'])
def create_contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        phone = request.form['phone'],
        
        print(" Form data :", name, email, phone, message)
        # Store the form data into the SQLite database
        new_contact = Contact(name=name, email=email, phone=str(phone), message=message)
        db.session.add(new_contact)
        db.session.commit()
       # Redirect to a success page
        return render_template('success.html')
   # Route to display the contact form
    return render_template('contact.html')


@app.route('/contacts', methods=['GET'])
def get_contacts():
    contacts = Contact.query.all()
    return render_template('view-users.html', contacts=contacts)


# Initialize the database
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
