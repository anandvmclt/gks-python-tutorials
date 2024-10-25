from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contact.db'  # Path to SQLite DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the Contact model
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False,unique=True)
    message = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Contact {self.name}'
    
# Create the database (Run this only once to create the table)
@app.before_first_request
def create_tables():
    db.create_all()

# Create a database connection
def get_db_connection():
    conn = sqlite3.connect('contact.db')  # Database file inside 'instance' folder
    conn.row_factory = sqlite3.Row
    return conn

# Initialize the database (only run this once, or when needed)
def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS contact (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"   

# Route for displaying the contact form
@app.route('/contact', methods=['GET', 'POST'])
def contacts():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        
        print(" Form data :", name, email, message)
        # Store the form data into the SQLite database
        conn = get_db_connection()
        conn.execute('INSERT INTO contact (name, email, message) VALUES (?, ?, ?)',
                     (name, email, message))
        conn.commit()
        conn.close()
        
        # Redirect to a success page
        return render_template('success.html')
        # return redirect(url_for('success'))
    
    return render_template('contact.html')

# List users in Table from databse
@app.route('/view-users', methods=['GET'])
def view_users():
    # Connect to the database
    conn = get_db_connection()
    # Fetch data from the database
    # users = conn.execute('SELECT * FROM contact').fetchall()
    users = Contact.query.all()  
    print("Users : ", users)
    conn.close()
    # Send the data to the template
    return render_template('view-users.html', users=users)






if __name__ == '__main__':
    init_db()  # Initialize the database
    app.run(debug=True)
