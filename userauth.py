#!/usr/bin/python
import base64
import getpass
from firebase_admin import db
import pyrebase

def enter(voterId, voterPassword):
    encodedPassword = base64.encodestring(voterPassword)

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
        vId = voter.val()['voterid']
        vPs = voter.val()['password']
        if voterId == vId and voterPassword == encodedvPs:
            return True
        else:
            return False
