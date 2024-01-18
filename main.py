from flask import Flask,request
import requests

def sendOtp(phoneNumber):
    headers = {
        "Content-Type":"application/json",
        "ApiKey":""
    }
    data = {
        "PhoneNumber":phoneNumber
    }
    res = requests.post("https://api.igniteauth.in/OTP/sendOTP",headers=headers,json=data)
    return res.text

def verifyOtp(phoneNumber,verificationCode,otp):
    headers = {
        "Content-Type":"application/json",
        "ApiKey":"6be2dd73-cc5c-4a03-a42a-3638d687ffc5"
    }
    data = {
        "PhoneNumber":phoneNumber,
        "VerificationCode":verificationCode,
        "OTP":otp
    }
    res = requests.post("https://api.igniteauth.in/OTP/verifyOTP",headers=headers,json=data)
    return res.text


app  = Flask(__name__)

@app.route('/')
def home():
    return "Hello FLASK"

@app.route('/login',methods =['POST'])
def login():
    postData =  request.json
    phoneNumber = postData.get("phoneNumber")
    otp = sendOtp(phoneNumber)
    print(otp)
    return otp

@app.route('/verify',methods =['POST'])
def verify():
    postData = request.json
    verificationCode = postData.get("verificationCode")
    phoneNumber = postData.get("phoneNumber")
    otp = postData.get("otp")
    res = verifyOtp(phoneNumber,verificationCode,otp)
    return res

users = [
    {"id": 1, "name": "John Doe"},
    {"id": 2, "name": "Jane Doe"}
]

# Route to get all users
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users)

# Route to get a specific user by ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = next((user for user in users if user['id'] == user_id), None)
    if user:
        return jsonify(user)
    else:
        return jsonify({"error": "User not found"}), 404

# Route to create a new user
@app.route('/users', methods=['POST'])
def create_user():
    new_user = request.json
    new_user['id'] = len(users) + 1
    users.append(new_user)
    return jsonify({"message": "User created successfully", "user": new_user}), 201

# Route to update a user by ID
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = next((user for user in users if user['id'] == user_id), None)
    if user:
        updated_data = request.json
        user.update(updated_data)
        return jsonify({"message": "User updated successfully", "user": user})
    else:
        return jsonify({"error": "User not found"}), 404

# Route to delete a user by ID
@app.route('/users/<int:user_id>', methods=['DELETE'])

def delete_user(user_id):
    global users
    users = [user for user in users if user['id'] != user_id]
    return jsonify({"message": "User deleted successfully"})
    
if __name__ == '__main__':
    app.run(debug=True)
