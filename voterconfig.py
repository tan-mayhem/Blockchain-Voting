import pyrebase

def create_firebase_user(auth):
    #prompt user to provide credentials
    print "Register your voter account"
    voterId = raw_input('Enter your voter ID: ')
    voterPassword = raw_input('Enter your voter password: ')
    #return firebase user
    return auth.create_user_with_email_and_password(voterId, voterPassword)

def login_to_firebase(auth):
    #prompt user to login on frontend
    print "Login to your voter account"
    voterId = raw_input('Enter your voter ID: ')
    voterPassword = raw_input('Enter your voter password: ')
    #return firebase user
    return auth.sign_in_with_email_and_password(voterId, voterPassword)

def authenticate_user(auth):
    choice = raw_input('Enter \"1\" to register new voter or enter \"2\" to login: ')
    if choice == '1':
        return create_firebase_user(auth)
    else:
        return login_to_firebase(auth)
