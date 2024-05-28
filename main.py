# Import necessary modules from Flask
from flask import Flask, redirect, url_for, request, render_template, abort
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask application
app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookings.db'
db = SQLAlchemy(app)

# Define Booking model
class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    service = db.Column(db.String(100), nullable=False)

# Define routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/booking')
def booking():
    return render_template('booking.html')

@app.route('/edit_booking/<int:booking_id>', methods=['GET'])
def edit_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    return render_template('edit_booking.html', booking=booking)

@app.route('/save_booking', methods=['POST'])
def save_booking():
    booking_id = request.form.get('booking_id')
    booking = Booking.query.get_or_404(booking_id)
    booking.name = request.form.get('name')
    booking.service = request.form.get('service')
    db.session.commit()
    return redirect(url_for('bookings'))

@app.route('/book', methods=['POST'])
def book():
    name = request.form.get('name')
    service = request.form.get('service')

    booking = Booking(name=name, service=service)
    db.session.add(booking)
    db.session.commit()
    return redirect(url_for('bookings'))

@app.route('/bookings')
def bookings():
    all_books = Booking.query.all()
    return render_template('bookings.html', bookings=all_books)

@app.route('/delete_booking', methods=['POST'])
def delete_booking():
    booking_id = request.form.get('booking_id')
    booking = Booking.query.get(booking_id)
    if booking:
        db.session.delete(booking)
        db.session.commit()
    return redirect(url_for('bookings'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables before running the app
    app.run(debug=True)
