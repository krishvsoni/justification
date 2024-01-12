from flask import Flask,request
import requests

def sendOtp(phoneNumber):
    headers = {
        "Content-Type":"application/json",
        "ApiKey":"6be2dd73-cc5c-4a03-a42a-3638d687ffc5"
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

password = "xUSx9r8DZpmURiNe"

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
    
if __name__ == '__main__':
    app.run(debug=True)