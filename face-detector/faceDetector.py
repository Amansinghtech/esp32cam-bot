import cv2
import requests
from mtcnn import MTCNN
import imutils

faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

detector = MTCNN()
# set headers for stream
# requests.get('http://192.168.4.1/control?var=framesize&val=7') # set to 6 for 640x480
# requests.get('http://192.168.4.1/control?var=special_effect&val=2') # set to 2 for grayscale
# requests.get('http://192.168.4.1/control?var=vflip&val=1') # set to 1 for vertical flip
# requests.get('http://192.168.4.1/control?var=led&val=1')
# video_capture = cv2.VideoCapture('http://192.168.4.1:81/stream')
video_capture = cv2.VideoCapture(0)
# video_capture.set(cv2.CAP_PROP_BUFFERSIZE, 1)
# video_capture.set(3,640) # set Width
# video_capture.set(4,480) # set Height

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    # without mtcnn method 1
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # faces = faceCascade.detectMultiScale(
    #     gray,
    #     scaleFactor=1.1,
    #     minNeighbors=5,
    #     minSize=(30, 30),
    #     flags=cv2.CASCADE_SCALE_IMAGE
    # )

    # # Draw a rectangle around the faces
    # for (x, y, w, h) in faces:
    #     print('detected face x, v, w, h:', x, y, w, h)
    #     cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # # with mtcnn method 2
    video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
    if ret == False:
        print('no frame')
        break;
    else:
        result = detector.detect_faces(frame)
        print(result)

        if len(result) > 0:
            bounding_box = result[0]['box']
            
            cv2.rectangle(frame, 
                          (bounding_box[0], bounding_box[1]),
                          (bounding_box[0]+bounding_box[2], bounding_box[1]+bounding_box[3]), 
                          (0, 255, 0), 
                          2)
        
        # Display the resulting frame
        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord(' '):
            requests.get('http://192.168.4.1/control?var=led&val=1')            
            break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()