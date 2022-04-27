import gardeneye
import os
import pyrebase
import configfile

firebase = pyrebase.initialize_app(configfile.firebaseConfig)
db = firebase.database()

auth = firebase.auth()
if __name__ == '__main__':
    #email = input('Email: ')
    #password = input('Password: ')
    email = 'paulmcd3@gmail.com'
    password = 'test123'
    #user = auth.sign_in_with_email_and_password(email, password)
    #items = db.child("PiDevices/").get()
    #print(len(items.key()))
    #print(len(items.val()))
    #print(items.key())
    #print(items.val())
   # print(f"Number of devices: {len(items.val())}")
    os.environ['Device'] = '0'#input('Enter Device number:')
    print(os.environ['Device'])
    os.environ['usingBackupData'] = 'false'
    gardeneye.main()
