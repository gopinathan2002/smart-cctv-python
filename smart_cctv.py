
from imutils.video import VideoStream
 
import datetime
import imutils
import time
import cv2
import way2sms
cam =cv2.VideoCapture(0)
ret,init=cam.read()

cv2.imwrite("ffrm.jpg",init)
cam.release()

vs = cv2.VideoCapture(0)
#mobno=input("Entert your Mobile no:")
#print(mobno)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
v = cv2.VideoWriter('suspects.avi',fourcc, 25.0, (640,480))
# initialize the first frame in the video stream
firstFrame = cv2.imread("ffrm.jpg")
firstFrame = imutils.resize(firstFrame, width=500)
firstFrame = cv2.cvtColor(firstFrame, cv2.COLOR_BGR2GRAY)
firstFrame = cv2.GaussianBlur(firstFrame, (21, 21), 0)
s=0
# loop over the frames of the video
while True:
    
    ret,frame = vs.read()
    
    vid=frame
    text = "Unoccupied"

    
    

    # resize the frame, convert it to grayscale, and blur it
    frame = imutils.resize(frame, width=500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    z=0

    # compute the absolute difference between the current frame and
    # first frame
    frameDelta = cv2.absdiff(firstFrame, gray)
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

    # dilate the thresholded image to fill in holes, then find contours
    # on thresholded image
    thresh = cv2.dilate(thresh, None, iterations=2)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] 

    # loop over the contours
    for c in cnts:
        # if the contour is too small, ignore it
        if cv2.contourArea(c) > 1000:
            continue

        # compute the bounding box for the contour, draw it on the frame,
        # and update the text
        z=z+1
        (x, y, w, h) = cv2.boundingRect(c)
        s=s+1
        #print(s)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        if(s%10==0 and s<500):
            #print("s=1")
            #print("in if")
            cv2.imwrite("suspect"+str(s)+".jpg",frame)
            #q=way2sms.Sms(1234567890,'*****')
            #j=0
            #j=q.send(mobno,'Someone is there in ur house')
            # print(j)
            #j=q.logout()
        else:
            text="Occupied"
            cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
            (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
            if(z==1):
                v.write(vid)
                #print(z)
 
            
        
        #out.write(frame)
        #cv2.imshow('frame',vid)
        

    # draw the text and timestamp on the frame
    
        
    
    cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
        (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

    # show the frame and record if the user presses a key
    #cv2.imshow("Frame Delta", frameDelta)
    cv2.imshow("Security Feed", frame)
    #cv2.imshow("Thresh", thresh)
    firstFrame=gray
    key = cv2.waitKey(2) & 0xFF
    #v.write(vid)

    # if the `q` key is pressed, break from the loop
    if key == ord("q"):
        v.release()
        break

# cleanup the camera and close any open windows
#
vs.release()
cv2.destroyAllWindows()
