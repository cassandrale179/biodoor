import pyrebase
# import picamera
from time import sleep

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


#x: how many times you want the camera to snap the picture
def capture(x):
    camera = picamera.PiCamera()
    camera.capture_sequence(['image%02d.jpg' % i for i in range(x)])
    print("finished taking picture!")

    #Upload image to Firebase Storage
    storage.child("images/image0.jpg").put("image0.jpg")

    #Push url to Firebase Database
    url = storage.child("images/image0.jpg").get_url(None)
    db.child("imageData").update({
        "imageURL": url
    })

# capture(1)
