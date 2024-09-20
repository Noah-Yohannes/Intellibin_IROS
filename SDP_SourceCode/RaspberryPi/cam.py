import cv2

def main3():
    cam0 = cv2.VideoCapture(0)
    cam1 = cv2.VideoCapture(2)

    assert cam0.isOpened(), "failed to grab frame0"
    assert cam1.isOpened(), "failed to grab frame1"

    cam0.set(3,224)
    cam0.set(4,224)
    cam1.set(3,224)
    cam1.set(4,224)

    # cam0.set(3,1000)
    # cam0.set(4,1000)
    # cam1.set(3,1000)
    # cam1.set(4,1000)
    
    cv2.namedWindow("0")
    cv2.namedWindow("1")

    while True:
        _, frame0 = cam0.read() 
        _, frame1 = cam1.read()
        
        frame0 = cv2.resize(frame0,(224,224))
        frame1 = cv2.resize(frame1,(224,224))
        
        cv2.imshow("0", frame0)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        cv2.imshow("1", frame1)
 
    cam0.release()
    cam1.release()
    cv2.destroyAllWindows()

main3()