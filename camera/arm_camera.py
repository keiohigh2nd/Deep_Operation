import cv2

if __name__=="__main__":

    capture1 = cv2.VideoCapture(0)
    capture2 = cv2.VideoCapture(1)
    capture = cv2.VideoCapture(2)
    
    if capture.isOpened() is False:
        raise("IO Error")

    cv2.namedWindow("Capture", cv2.WINDOW_AUTOSIZE)

    while True:
        #This line save the photos 
        ret, image = capture.read()
        if ret == False:
            continue
        cv2.imshow("Capture", image)
        if cv2.waitKey(33) >= 0:
            cv2.imwrite("image.png", image)
            break

    cv2.destroyAllWindows()
