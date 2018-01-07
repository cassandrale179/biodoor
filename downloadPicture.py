import pyrebase
config = {
    "apiKey": "AIzaSyBiBNGannX7FelsOzvJMuqAmkqhVykrxIc",
    "authDomain": "cognizer-7f557.firebaseapp.com",
    "databaseURL": "https://cognizer-7f557.firebaseio.com",
    "projectId": "cognizer-7f557",
    "storageBucket": "cognizer-7f557.appspot.com",
    "messagingSenderId": "311655476959"
}
firebase = pyrebase.initialize_app(config)

storage = firebase.storage()
db  = firebase.database()

def downloadPic():
    storage.child("images/image0.jpg").download("demoImage.jpg")
