
from app import create_app
from app.extensions import db
from flask import request, jsonify
from app.blueprints import Customer

app = create_app()

with app.app_context():
    # db.drop_all()
    db.create_all()
    app.run(debug=True)

# --- Signup route for registering new customers ---
@app.route('/auth/signup', methods=['POST'])
def signup():
    data = request.get_json()
    email = data.get('email')
    if not email or not data.get('password'):
        return jsonify({'message': 'Email and password required'}), 400
    if Customer.query.filter_by(email=email).first():
        return jsonify({'message': 'Email already registered'}), 400
    customer = Customer(
        first_name=data.get('first_name', ''),
        last_name=data.get('last_name', ''),
        email=email,
        phone=data.get('phone', ''),
        password=data.get('password'),
        address=data.get('address', ''),
        dob=data.get('dob')
    )
    db.session.add(customer)
    db.session.commit()
    return jsonify({'message': 'Customer registered successfully', 'id': customer.id}), 201

if __name__ == "__main__":
    app.run(debug=True)