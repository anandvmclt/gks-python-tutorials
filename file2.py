from flask import Flask,jsonify, render_template
import json

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/home")
def home():
    data = {'name': 'John', 'age': 30, 'city': 'New York'}
    return render_template('index.html',data=data)


app.run(debug=True)

# if __name__ == "__main__":
#     app.run(debug=True)