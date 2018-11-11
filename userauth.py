#!/usr/bin/python
import base64
import getpass
from firebase_admin import db
import pyrebase

"""
def create():

    config = {
      'apiKey': 'AIzaSyBXQCdlBopceWbLcXV5lMAvoB1zoO8aOmg',
      'authDomain': 'blockchain-voting-79bf6.firebaseapp.com',
      'databaseURL': 'https://blockchain-voting-79bf6.firebaseio.com',
      'storageBucket': 'blockchain-voting-79bf6.appspot.com',
      'serviceAccount': 'blockchain-voting-79bf6-firebase-adminsdk-c8jef-ce8ee634ad.json'
    }

    firebase = pyrebase.initialize_app(config)
    db = firebase.database()
    ref = db.reference()

    voters_ref = ref.child('voters')
    voters_ref.push({
        'voter1': {
            'voter ID': '123',
            'password': '123'
        },
        'voter2': {
            'voter ID': '456',
            'password': '456'
        }
    })
"""

def enter(voterId, voterPassword, bc):
    encodedPassword = base64.encodestring(voterPassword)
    # Verify count
    count = 0
    for i in range(len(bc)):
        if bc[i][1] == voterId:
            if count >= 1:
                return False
            else:
							count += 1

    config = {
      'apiKey': 'AIzaSyBXQCdlBopceWbLcXV5lMAvoB1zoO8aOmg',
      'authDomain': 'blockchain-voting-79bf6.firebaseapp.com',
      'databaseURL': 'https://blockchain-voting-79bf6.firebaseio.com',
      'storageBucket': 'blockchain-voting-79bf6.appspot.com',
      'serviceAccount': 'blockchain-voting-79bf6-firebase-adminsdk-c8jef-ce8ee634ad.json'
    }

    firebase = pyrebase.initialize_app(config)
    db = firebase.database()

    all_voters = db.child("voters").get()
    for voter in all_voters.each():
        vId = str(voter.val()['voterid'])
        vPs = str(voter.val()['password'])
        if voterId == vId and voterPassword == vPs:
            k = 1
            break
        else:
            k = 0

    if k == 1:
        return True
    else:
        return False
