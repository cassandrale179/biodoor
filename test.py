import numpy
import cv2
import os
import pyrebase
import downloadPicture
from twilio.rest import Client
# import win32com.client as wincl
import ttsTest
# speak = wincl.Dispatch("SAPI.SpVoice")


#------------------------ FIREBASE CONFIG ----------------
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


#------------------- TWILIO API ----------------------------
account_sid = "ACa25b9e68025c8db22bb5d85e4e930cc5"
auth_token = "b3914f78318a81ab0603b02b2256ff93"
client = Client(account_sid, auth_token)

#--------------------GET CURRENT DIRECTORY PATH ---------------
cwd = os.getcwd()


#----------------------- DETECT IF A FACE EXIST ------------------
def detect_face(image):
    #----------------- GET THE HAARCASCADE FORMULA --------------
    # cascPath = 'C:\Users\lengu\Desktop\hackathons\cognizer\\haarcascade_frontalface_default.xml'
    cascPath = os.path.join(cwd, 'haarcascade_frontalface_default.xml')
    faceCascade = cv2.CascadeClassifier(cascPath)

    #----------------- TRAIN DATA --------------------
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags = cv2.CASCADE_SCALE_IMAGE
    );
    if (len(faces) == 0):
        return None, None
    (x, y, w, h) = faces[0]
    return gray[y:y+w, x:x+h], faces[0]


#----------- ACCESS FOLDER DATA AND RETURN A LIST OF FACES AND THEIR LABEL ------------------
def train_data(folderpath):
    dirs = os.listdir(folderpath)
    faces = []
    labels = []
    for folder in dirs:
        label = int(folder[1:])
        images = os.listdir(folderpath + "\\" + folder)
        for imagename in images:
            imagepath = folderpath + "\\" + folder + "\\" + imagename
            image = cv2.imread(imagepath)
            # cv2.imshow("Training on image...", image)
            # cv2.waitKey(100)
            face, rect = detect_face(image)
            if face is not None:
                faces.append(face)
                labels.append(label)
    cv2.destroyAllWindows()
    cv2.waitKey(1)
    cv2.destroyAllWindows()
    return faces, labels

#------------------- TRAIN FACE RECOGNIZER ----------------------
# folderPath = 'C:\Users\lengu\Desktop\hackathons\cognizer\data'
folderPath = os.path.join(cwd, 'data')
faces, labels = train_data(folderPath)
face_recognizer = cv2.createLBPHFaceRecognizer()
face_recognizer.train(faces, numpy.array(labels))


#------------------- DRAWING FUNCTION ---------------------
def draw_rectangle(img, rect):
    (x,y,w,h) = rect
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
def draw_text(img, text, x, y):
    cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)

#---------------------- FACE PREDICTION ------------------
def predict(testImage, owner):

    #---------------- GLOBAL VARIABLES TO BE USED ----------
    global face_recognizer
    global client
    global speak
    subjects = ["", owner]
    img = testImage.copy()
    face, rect = detect_face(img)
    print face
    label, confidence = face_recognizer.predict(face)

    #------------- IF IT'S A GOOD MATCH (THRESHOLD UNDER 100) ----------
    print("Confidence level", confidence)
    if (confidence < 130) and (confidence != 0):
        label_text = subjects[label]
        ttsTest.speakNow(owner)
        print("This picture is the owner")
        #Push the signal to firebase
        db.child('signal').update({
            'doorOpen': 1       # It's the OWNER
        })
        # str_speech = "Welcome home " + owner
        # speak.Speak(str_speech)

    #------------ IF IT'S NOT A GOOD MATCH -------------------
    else:
        ttsTest.intruder()
        # str_speech = "INTRUDER ALERT INTRUDER ALERT GET OUT OF MY F ing HOUSE!"
        # speak.Speak(str_speech)
        label_text = "Not sure who this is"
        print("This picture is not the owner")
        db.child('signal').update({
            'doorOpen': 2       # It's a THIEF
        })
        message = client.messages.create(
        to="+15512326269",
        from_="+15595408466 ",
        body="There's an INTRUDER!!!!!!")
        print(message.sid)

    #----------------- DISPLAY PICTURE OF PERSON AND LABEL THEM -----------
    draw_rectangle(img, rect)
    draw_text(img, label_text, rect[0], rect[1]-5)
    return img

#---------------------- INPUTTING IMAGE HERE FOR TESTING ------------
def testmain(owner):
    db.child('signal').update({
            'doorOpen': 0
    })
    print("Predicting images...")
    test_img1 = cv2.imread(os.path.join(cwd, "pic.png"))
    predicted_img1 = predict(test_img1, owner)
    print("Prediction complete")

    cv2.imshow('Image', cv2.resize(predicted_img1, (700, 500)))
    cv2.waitKey(0)
    cv2.destroyAllWindows()
