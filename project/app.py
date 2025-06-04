from flask import Flask, request, jsonify, redirect, render_template,session
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
import bcrypt
import os

app = Flask(__name__)
CORS(app,supports_credentials=True)


app.config.from_pyfile('config.py')
app.config['MONGO_URI'] = 'mongodb+srv://oshaikh2705:oweish27@aihealthcare.r2e4n.mongodb.net/aihealthcare?retryWrites=true&w=majority&tlsAllowInvalidCertificates=true'

client = MongoClient(app.config['MONGO_URI'])
db = client.get_database('aihealthcare') 
users_collection = db.users


def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed)


@app.route('/')
def index():
    return render_template('login.html')

# Signup Endpoint

@app.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.json
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')

        if not name or not email or not password:
            return jsonify({"message": "All fields are required"}), 400
        
        existing_user = users_collection.find_one({"email": email})
        if existing_user:
            return jsonify({"message": "Email already exists"}), 400
        
        hashed_password = hash_password(password)
        
        user = {
            "name": name,
            "email": email,
            "password": hashed_password
        }
        result = users_collection.insert_one(user)
        
        return jsonify({
            "message": "Signup successful",
            "user_id": str(result.inserted_id)
        }), 201
        
    except Exception as e:
        print(f"Error: {str(e)}")  # Log it for debugging
        return jsonify({"message": "Something went wrong. Please try again."}), 500

# Login Endpoint

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({"message": "All fields are required"}), 400
        
        user = users_collection.find_one({"email": email})
        if not user:
            return jsonify({"message": "Invalid email or password"}), 401
        
        if not check_password(password, user['password']):
            return jsonify({"message": "Invalid email or password"}), 401
        
        session['user_id'] = str(user['_id'])
        session['user_name'] = user['name']
        
        return jsonify({
            "message": "Login successful",
            "user": {"id": str(user['_id']), "name": user['name']}
        }), 200

    except Exception as e:
        print(f"Error: {str(e)}")  # Log it for debugging
        return jsonify({"message": "Something went wrong. Please try again."}), 500
 
    
@app.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({"message": "Email is required"}), 400

    # Example: Send email logic here (implement with SMTP or service like SendGrid)
    print(f"Sending reset link to {email}")

    return jsonify({"message": "Password reset link sent!"}), 200



@app.route('/profile', methods=['GET'])
def profile():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"message": "Unauthorized"}), 401
    
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    user_profile = {
        "id": str(user['_id']),
        "name": user['name'],
        "email": user['email']
    }
    
    return jsonify(user_profile), 200



@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"message": "Logged out successfully"}), 200


@app.route('/api/patient/<id>', methods=['GET'])
def get_patient(id):
    try:
        patient = db.patients.find_one({"patientId": id})
        if not patient:
            return jsonify({"error": "Patient not found"}), 404
        patient['_id'] = str(patient['_id'])  # Convert ObjectId to string
        return jsonify(patient), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal server error"}), 500


@app.route('/api/patient/<patient_id>', methods=['GET'])
def get_patient_profile(patient_id):
    try:
        user = users_collection.find_one({"_id": ObjectId(patient_id)})
        if not user:
            return jsonify({"message": "User not found"}), 404

        user_profile = {
            "id": str(user['_id']),
            "name": user['name'],
            "email": user['email'],
        }
        return jsonify(user_profile), 200
    except Exception as e:
        print(f"Error fetching patient profile: {str(e)}")
        return jsonify({"message": "Something went wrong"}), 500


# Run Flask App


if __name__ == '__main__':
    app.run(debug=True, port=5001)
