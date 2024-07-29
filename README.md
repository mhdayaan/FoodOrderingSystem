Food Ordering System
This is a simple food ordering system implemented using Flask, a web framework for Python. The system allows users to sign up, log in, select a restaurant, choose menu items, and place an order. It also includes a confirmation page and a page for entering delivery address information.

Table of Contents
Requirements
Installation
Configuration
Usage
File Structure
Dependencies

Requirements
Python 3.x
PostgreSQL database
Flask
Flask-WTF
Psycopg2

Install dependencies:
pip install -r requirements.txt

Configuration
Set up a PostgreSQL database and update the connection details in the connect_to_database function in app.py.


Usage
Run the Flask application:
python app.py
Visit http://localhost:5000 in your web browser.

File Structure
app.py: The main Flask application file.
static/: Folder containing static files such as stylesheets and images.
templates/: Folder containing HTML templates.
requirements.txt: List of Python dependencies.

Dependencies
Flask: Web framework for Python.
Flask-WTF: Flask integration with WTForms.
Psycopg2: PostgreSQL adapter for Python.