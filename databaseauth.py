import pyrebase
from voterconfig import *

config = {
  'apiKey': 'AIzaSyBXQCdlBopceWbLcXV5lMAvoB1zoO8aOmg',
  'authDomain': 'blockchain-voting-79bf6.firebaseapp.com',
  'databaseURL': 'https://blockchain-voting-79bf6.firebaseio.com',
  'storageBucket': 'blockchain-voting-79bf6.appspot.com'
}

fb = pyrebase.initialize_app(config)
result = fb.get('blockchain-voting-79bf6')
auth = fb.auth()
db = fb.database()
voter = authenticate_user(auth)

# data to save
data = {
    'metadata': {'voterId': '123', 'voterPassword': 'password123'},
}

# Pass the user's idToken to the push method
# results = db.child("users").push(data, user['idToken'])
metadata_store = db.child("voter").child(voter['localId']).push(data, voter['idToken'])

"""
fb = firebase.FirebaseApplication('https://blockchain-voting-79bf6.firebaseio.com', None)

name = input('Enter a name: ')

result = fb.post('/voter', name)
print(result)
"""
