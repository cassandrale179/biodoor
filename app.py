#----------------------- IMPORT A BUNCH OF STUFF -----------------------------
from flask import Flask, render_template, request, json, url_for, flash, jsonify
import pyrebase
import numpy
import os
import cv2
import time
import test
app = Flask(__name__)

owner = ""


#-------------------- INITIALIZE FIREBASE -------------------
config = {
    "apiKey": "AIzaSyBiBNGannX7FelsOzvJMuqAmkqhVykrxIc",
    "authDomain": "cognizer-7f557.firebaseapp.com",
    "databaseURL": "https://cognizer-7f557.firebaseio.com",
    "projectId": "cognizer-7f557",
    "storageBucket": "cognizer-7f557.appspot.com",
    "messagingSenderId": "311655476959"
}
firebase = pyrebase.initialize_app(config)



#-------------------- MAIN PAGE ------------------
@app.route("/")
def main():
    auth = firebase.auth()
    db = firebase.database()
    print(db)
    return render_template('index.html')

#------------------- GET THE VARIABLES ------------
@app.route("/send", methods=['POST','GET'])
def send():
    global owner
    #------------- IF YOU CLICK SEND BUTTON ------
    if request.method == 'POST':
        name = request.form['name']
        owner = name

        #------ THE CODE TO OPEN THE WEBCAM ------
        cam = cv2.VideoCapture(0)
        cv2.namedWindow("test")
        img_counter = 0
        ret, frame = cam.read()
        cv2.imshow("test", frame)
        t0 = time.clock()
        wait_time = 0
        while wait_time < 3:
            wait_time = time.clock()-t0
        while True:
            ret, frame = cam.read()
            cv2.imshow("test", frame)
            while img_counter < 10:
                img_name = "opencv_frame_{}.png".format(img_counter)
                cv2.imwrite("data/s1/" + img_name, frame)
                print("{} written!".format(img_name))
                img_counter += 1
            break
        cam.release()
        cv2.destroyAllWindows()
        return render_template('age.html', name=name)
    else:
        return render_template('index.html')

@app.route("/letmein", methods=['POST', 'GET'])
def letmein():
    global owner
    # ------------- IF YOU CLICK LET ME IN BUTTON ------
    if request.method == 'POST':

        #-------- SECRETLY TAKE ONE PICTURE ----------------
        cam = cv2.VideoCapture(0)
        cv2.namedWindow("test")
        img_counter = 0
        ret, frame = cam.read()
        cv2.imshow("test", frame)
        t0 = time.clock()
        wait_time = 0
        while wait_time < 3:
            wait_time = time.clock()-t0
        ret, frame = cam.read()
        cv2.imshow("test", frame)
        img_name = "pic.png"
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        cam.release()
        cv2.destroyAllWindows()

        #-----------  CALL THE TEST MAIN FUNCTION AGAIN ----------------
        test.testmain(owner)
        return render_template('index.html')

#---------------- RUN THE APP -----------------
if __name__ == "__main__":
    app.run()
