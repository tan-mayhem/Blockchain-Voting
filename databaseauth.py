import pyrebase

config = {
  "apiKey": "AIzaSyBXQCdlBopceWbLcXV5lMAvoB1zoO8aOmg",
  "authDomain": "blockchain-voting-79bf6.firebaseapp.com",
  "databaseURL": "https://blockchain-voting-79bf6.firebaseio.com/",
  "storageBucket": "blockchain-voting-79bf6.appspot.com"
}

firebase = pyrebase.initialize_app(config)

# Get a reference to the auth service
auth = firebase.auth()

# Log the user in
# user = auth.sign_in_with_email_and_password(email, password)

# Get a reference to the database service
db = firebase.database()



# data to save
data = {
    'voterId': '123'
    'voterPassword': 'password123'
},
{
    'voterId': '456'
    'voterPassword': 'password456'
},
{
    'voterId': '789'
    'voterPassword': 'password789'
}

# Pass the user's idToken to the push method
# results = db.child("users").push(data, user['idToken'])
db.child("voter").child(user['localId']).push(data, user['idToken'])
