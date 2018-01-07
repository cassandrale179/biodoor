# Servo Control
import time
import pyrebase
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(14, GPIO.OUT)
pwm = GPIO.PWM(14, 50)
pwm.start(0)

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

def setAngle(angle):
        duty = angle / 18 + 2
        GPIO.output(14, True)
        pwm.ChangeDutyCycle(duty)
        time.sleep(1)
        GPIO.output(14, False)
        pwm.ChangeDutyCycle(0)


def openDoor():
        setAngle(90)
        time.sleep(5)
        setAngle(0)

def lockDoor():
        setAngle(0)

signal_to_servo = db.child('signal').get().key()
while signal_to_servo == 0:
        signal_to_servo = db.child('signal').get().key()
        time.sleep(0.05)

if signal_to_servo == 1:
        openDoor()
else:
        lockDoor()




