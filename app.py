from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os 
import secrets

load_dotenv()

MONGO_URI=os.getenv('MONGO_URI')

uri = MONGO_URI

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

db=client.cloud_resume #Database name is cloud_resume

contacts_collection = db['contact']  # Collection name or Table Name

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


app = Flask(__name__)

app.secret_key = secrets.token_hex(16)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/resume')
def resume():
    return render_template('resume.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/submit_form', methods=['POST'])
def submit_form():
    if request.method == 'POST':
        # Retrieve form data
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        message = request.form['message']

        # Save to MongoDB
        contact_entry = {'name': name, 'email': email, 'phone':phone, 'message': message}
        contacts_collection.insert_one(contact_entry)

        # Debugging print statement
        print("Flashing message: Your message has been saved successfully!")

        flash("Your message has been saved successfully!", "success")

        # print(session)

        return redirect(url_for('contact'))
    
@app.route('/view_contacts')
def view_contacts():
    contacts = list(contacts_collection.find())  # Retrieve all documents from MongoDB
    return render_template('view_contacts.html', contacts=contacts)

@app.route('/projects')
def projects():
    return render_template('projects.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404

if __name__ == '__main__':
    app.run(port=5000, debug=True)