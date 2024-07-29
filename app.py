from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from psycopg import connect
from decimal import Decimal

app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = 'your_secret_key'

def connect_to_database():
    conn = connect("dbname=Final_Project port=5431 user=postgres password=minu")
    cursor = conn.cursor()
    return conn, cursor

class SignupForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(min=4, max=25)])
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired(), Length(min=6, max=40)])
    phone = StringField('phone', validators=[DataRequired(), Length(min=10, max=15)])
    submit = SubmitField('sign Up')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

def get_menu_items():
    return {
        '1': {'name': 'Item 1', 'price': 10},
        '2': {'name': 'Item 2', 'price': 15},
        '3': {'name': 'Item 3', 'price': 20},
    }

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/logout', methods=['POST'])
def logout():
    # Clear the session data
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        phone = form.phone.data
        conn, cursor = connect_to_database()

        try:
            cursor.execute('INSERT INTO users (username, email, password, phone) VALUES (%s, %s, %s, %s)',
                           (username, email, password, phone))
            conn.commit()

            session['username'] = username
            flash('Account created successfully. Please log in.', 'success')
            return redirect(url_for('select_restaurant'))
        except Exception as e:
            print(f"Error creating account: {str(e)}")
            flash(f'Error creating account: {str(e)}', 'danger')
        finally:
            cursor.close()
            conn.close()

    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session['username'] = form.username.data
        flash('Login successful.', 'success')
        return redirect(url_for('select_restaurant'))

    return render_template('login.html', form=form)

@app.route('/select-restaurant', methods=['GET', 'POST'])
def select_restaurant():
    conn, cursor = None, None  # Initialize variables

    try:
        conn, cursor = connect_to_database()

        if request.method == 'POST':
            # Handle form submission here
            selected_restaurant_id = request.form.get('restaurant')
            flash(f'Selected restaurant ID: {selected_restaurant_id}', 'success')
            return redirect(url_for('menus', restaurant=selected_restaurant_id))

        # Fetch the list of restaurants
        cursor.execute('SELECT id, name FROM restaurants limit 1000')
        restaurants = cursor.fetchall()

    except Exception as e:
        print(f"Error: {str(e)}")
        flash(f'Error: {str(e)}', 'danger')
        restaurants = []  # Assign an empty list in case of an error

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return render_template('select_restaurant.html', restaurants=restaurants)

@app.route('/ratings')
def ratings():
    conn, cursor = connect_to_database()

    try:
        # Fetch ratings for all restaurants
        cursor.execute('SELECT name, ratings FROM ratings')
        restaurant_ratings = cursor.fetchall()

        return render_template('ratings.html', restaurant_ratings=restaurant_ratings)

    except Exception as e:
        print(f"Error fetching ratings: {str(e)}")
        flash(f'Error fetching ratings: {str(e)}', 'danger')

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return render_template('error.html')

def get_user_id(username):
    conn, cursor = connect_to_database()

    try:
        cursor.execute('SELECT user_id FROM users WHERE username = %s', (username,))
        user_id = cursor.fetchone()

        if user_id is not None:
            return user_id[0]
        else:
            return None

    except Exception as e:
        print(f"Error getting user ID: {str(e)}")
        flash(f'Error getting user ID: {str(e)}', 'danger')
        return None

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def get_last_order_id():
    conn, cursor = connect_to_database()

    try:
        cursor.execute('SELECT MAX(id) FROM menu_items')
        last_order_id = cursor.fetchone()[0]
        return last_order_id if last_order_id is not None else 0

    except Exception as e:
        print(f"Error getting last order ID: {str(e)}")
        flash(f'Error getting last order ID: {str(e)}', 'danger')
        return None

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route('/menus', methods=['GET', 'POST'])
def menus():
    if request.method == 'POST':
        # Handle form submission for selected menu items here
        username = session.get('username')
        selected_items = request.form.getlist('item[]')
        quantities = request.form.getlist('quantity[]')
        prices = request.form.getlist('price[]')

        user_id = get_user_id(username)

        if user_id is not None:
            last_order_id = get_last_order_id()

            if last_order_id is not None:
                order_id = last_order_id + 1
            else:
                order_id = 1

            conn, cursor = connect_to_database()

            try:
                import re
                for i in range(len(selected_items)):
                    # Use regular expression to extract item name and price
                    match = re.match(r'^(.+) - \$([0-9.]+)$', selected_items[i])

                    if match:
                        item_name = match.group(1)
                        price = float(match.group(2))
                    else:
                        # Handle the case where the regular expression doesn't match
                        print(f"Error extracting item name and price for: {selected_items[i]}")
                        continue
                    # Extract quantity
                    quantity = quantities[i]

                   
                    # Insert into the database
                    cursor.execute('INSERT INTO menu_items (id, item_name, qty, price, user_id) VALUES (%s, %s, %s, %s, %s)',
                                (order_id, item_name, quantity, price, user_id))
                # Commit the changes
                conn.commit()
                flash(f'Selected menu items added to your order with ID: {order_id}.', 'success')
                return redirect(url_for('confirmation', order_id=order_id))

            except Exception as e:
                print(f"Error: {str(e)}")
                flash(f'Error: {str(e)}', 'danger')

            finally:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()
        else:
            flash('User not found.', 'danger')

    else:
        # This is the GET request to display the menu items
        restaurant_id = request.args.get('restaurant')
        conn, cursor = connect_to_database()

        try:
            # Fetch the menu items for the selected restaurant
            cursor.execute('SELECT id, name, price FROM menus WHERE restaurant_id = %s', (restaurant_id,))
            menu_items = cursor.fetchall()

            return render_template('menus.html', menu_items=menu_items, restaurant_id=restaurant_id)

        except Exception as e:
            print(f"Error: {str(e)}")
            flash(f'Error: {str(e)}', 'danger')

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    return render_template('error.html')

@app.route('/confirmation/<int:order_id>')
def confirmation(order_id):
    conn, cursor = connect_to_database()

    try:
        # Fetch the selected menu items and their details for the given order_id
        cursor.execute('SELECT item_name, qty, price, user_id FROM menu_items WHERE id = %s', (order_id,))
        order_details = cursor.fetchall()

        # Calculate the total price
        total_price = sum(item[1] * item[2] for item in order_details)
        user_id = next((item[3] for item in order_details), None)
        
        # Insert into the 'orders' table
        cursor.execute('INSERT INTO orders (user_id,order_total,order_id) VALUES (%s, %s, %s)',
                (user_id, total_price, order_id))

        conn.commit()

        if request.method == 'POST':
            # Redirect to the address page
            return redirect(url_for('address', order_id=order_id))

        return render_template('confirmation.html', order_id=order_id, order_details=order_details, total_price=total_price, user_id=user_id)

    except Exception as e:
        print(f"Error fetching order details: {str(e)}")
        flash(f'Error fetching order details: {str(e)}', 'danger')

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return render_template('error.html')

@app.route('/address', methods=['GET', 'POST'])
def address():
    # Handle the form submission for the address information
    if request.method == 'POST':
        # Extract address information from the form data
        address = request.form.get('address')
        pincode = request.form.get('pincode')
        # Get other address-related fields as needed

        # Assuming user is logged in, get user_id from session
        username = session.get('username')
        user_id = get_user_id(username)

        if user_id is not None:
            conn, cursor = connect_to_database()

            try:
                # Insert the address information into the 'address' table
                cursor.execute('INSERT INTO address (user_id, street, pincode) VALUES (%s, %s, %s)',
                               (user_id, address, pincode))
                conn.commit()

                flash('Address information saved successfully.', 'success')
                return redirect(url_for('thank_you'))

            except Exception as e:
                print(f"Error inserting address: {str(e)}")
                flash(f'Error inserting address: {str(e)}', 'danger')

            finally:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()

    return render_template('address.html')

# Add a route for the thank you page
@app.route('/thank-you')
def thank_you():
    return render_template('thank_you.html')



if __name__ == '__main__':
    app.run(debug=True)
