from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

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

# Route for displaying the contact form
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        
        print(" Form data :", name, email, message)
        # Store the form data into the SQLite database
        conn = get_db_connection()
        conn.execute('INSERT INTO contact (name, email, message) VALUES (?, ?, ?)',
                     (name, email, message))
        # conn.commit()
        conn.close()
        
        # Redirect to a success page
        return render_template('success.html')
        # return redirect(url_for('success'))
    
    return render_template('contact.html')

# Route for success page
# @app.route('/success')
# def success():
#     return render_template('success.html')

if __name__ == '__main__':
    init_db()  # Initialize the database
    app.run(debug=True)
