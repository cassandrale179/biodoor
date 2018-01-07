#!/usr/bin/python

import cv2

cam = cv2.VideoCapture(0)
cv2.namedWindow("test")

ret, frame = cam.read()
cv2.imshow("test", frame)
while True:
    ret, frame = cam.read()
    cv2.imshow("test", frame)
    # if not ret:
    #     break
    # k = cv2.waitKey(1)
    img_counter = 0
    while img_counter < 10:
    # if k%256 == 27:
        # ESC pressed
        # print("Escape hit, closing...")
        # break
    # elif k%256 == 32:
        # SPACE pressed
        img_name = "opencv_frame_{}.png".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        img_counter += 1
    break
cam.release()
cv2.destroyAllWindows()