import numpy as np
import cv2

def getImage():
    cam = cv2.VideoCapture(0)
    count = 0
    while (count != 1):
        ret, img = cam.read()
        cv2.imshow("Press Space Button To Take A Photo", img)
        if not ret:
            break
        k = cv2.waitKey(1)

        if k % 256 == 27:
            print("close")
            break

        if k % 256 == 32:
            print("Image saved")
            cv2.imwrite('../Images/image.jpg', img)
            count += 1

    cam.release()
    cv2.destroyAllWindows()

getImage()
