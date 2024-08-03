# Food Ordering System

This repository contains a simple food ordering system implemented using Flask, a web framework for Python. The system allows users to sign up, log in, select a restaurant, choose menu items, and place an order. It also includes a confirmation page and a page for entering delivery address information.

## Table of Contents

1. [Requirements](#requirements)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Usage](#usage)
5. [File Structure](#file-structure)
6. [Dependencies](#dependencies)
7. [Libraries Used](#libraries-used)
8. [Contributing](#contributing)

## Requirements

- Python 3.x
- PostgreSQL database
- Flask
- Flask-WTF
- Psycopg2

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/mhdayaan/DBMS
   cd DBMS
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. Set up a PostgreSQL database.
2. Update the connection details in the `connect_to_database` function within `app.py`.

## Usage

1. Run the Flask application:
   ```bash
   python app.py
   ```

2. Open your web browser and visit [http://localhost:5000](http://localhost:5000) to access the application.

## File Structure

- `app.py`: The main Flask application file.
- `static/`: Folder containing static files such as stylesheets and images.
- `templates/`: Folder containing HTML templates.
- `requirements.txt`: List of Python dependencies.
- `Data Files/`: Directory for storing data files.
- `Log/`: Directory for application logs.
- `Pg_dump Files/`: Directory for PostgreSQL dump files.
- `README.md`: This file.

## Dependencies

- **Flask**: Web framework for Python.
- **Flask-WTF**: Flask integration with WTForms.
- **Psycopg2**: PostgreSQL adapter for Python.

## Libraries Used

This project utilizes several Python libraries to provide functionality for the food ordering system. Below are the libraries used along with their roles:

- **Flask**: 
  - **Purpose**: Web framework for building the application.
  - **Usage**: Manages routing, request handling, and response generation.
  - **Documentation**: [Flask Documentation](https://flask.palletsprojects.com/)

- **Flask-WTF**:
  - **Purpose**: Integration of WTForms with Flask for form handling and validation.
  - **Usage**: Provides form classes and validation methods to handle user inputs.
  - **Documentation**: [Flask-WTF Documentation](https://flask-wtf.readthedocs.io/)

- **WTForms**:
  - **Purpose**: Library for form handling and validation.
  - **Usage**: Defines form fields and validators to manage and validate user input.
  - **Documentation**: [WTForms Documentation](https://wtforms.readthedocs.io/)

- **Psycopg2**:
  - **Purpose**: PostgreSQL adapter for Python.
  - **Usage**: Connects to and interacts with PostgreSQL databases.
  - **Documentation**: [Psycopg2 Documentation](https://www.psycopg.org/docs/)

- **Decimal**:
  - **Purpose**: Provides support for fast correctly-rounded decimal floating point arithmetic.
  - **Usage**: Handles precise monetary calculations and avoids floating-point inaccuracies.
  - **Documentation**: [Decimal Documentation](https://docs.python.org/3/library/decimal.html)

## Contributing

Contributions are welcome! Please open an issue or submit a pull request with your changes.
