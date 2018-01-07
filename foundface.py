import numpy
import cv2
import matplotlib.pyplot as plt


#------------- READ AND DISPLAY AN IMAGE ------------
imagePath = 'C:\Users\lengu\Desktop\cognizer\\face.jpg'
cascPath = 'C:\Users\lengu\Desktop\cognizer\\haarcascade_frontalface_default.xml'
faceCascade = cv2.CascadeClassifier(cascPath)
image = cv2.imread(imagePath)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


# Detect faces in the image
# detectMultiScale function detects general objects
# scaleFactor: some faces may be closer to the camera
# minNeighbors defines how many objects are detected near the current one before it declares the face found
# faces: a list of rectangles where it believes it found a face
faces = faceCascade.detectMultiScale(
    gray,
    scaleFactor=1.1,
    minNeighbors=5,
    minSize=(30, 30),
    flags = cv2.CASCADE_SCALE_IMAGE
)


print "Found {0} faces!".format(len(faces))

# Draw a rectangle around the faces
for (x, y, w, h) in faces:
    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

cv2.imshow('Faces found', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
#img = cv2.imread(imgPath, cv2.IMREAD_GRAYSCALE)

'''
Plot the image
plt.imshow(img, cmap='gray', interpolation='bicubic')
plt.show()
'''
