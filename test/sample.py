# vim: set fileencoding=utf-8 :
import numpy as np
import cv2

def linear(x, cols):
    return -8*x + cols

def robot_arms(image, size):
    cv2.line(image, (0, 0), (360, 360), (0, 255, 0), 5)
    cv2.line(image, (len(image[0]), 0), (200,200), (0, 0, 255), 3)
    return image

def put_rectangles(rows, cols, images):
    cv2.rectangle(image,(int(cols*0.6),int(rows*0.7)),((int(cols*0.6)+40), rows),(0,255,0),cv2.cv.CV_FILLED)
    cv2.rectangle(image,(int(cols*0.6),int(rows*0.3)),((int(cols*0.6)+40), int(rows*0.4)),(0,255,0),cv2.cv.CV_FILLED)

if __name__ == "__main__":
    cols = 1024
    rows = 800

    image = np.zeros((rows, cols, 3), np.uint8)

    image = robot_arms(image, 20)
    image = put_rectangles(rows, cols, image)

    # 表示して[ESC]が押されるまで待つ
    #cv2.imshow("image", image)
    #while cv2.waitKey(33) != 27:
      #pass
