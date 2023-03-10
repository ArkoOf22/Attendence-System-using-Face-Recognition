
import cv2  
import numpy as np
import face_recognition
import os
from datetime import datetime
path = 'Training_images'
images=[]
className=[]
myList=os.listdir(path)
print(myList)
for cl in myList:
    curImg=cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    className.append(os.path.splitext(cl)[0])
print(className)
def faceEncodings(images):
    encodeList = []
    for img in images:
        img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode=face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

encodeListKnown = faceEncodings(images)
print('Encoding Complete')

def attendance(name,dStr):

    with open('attendance.csv','r+') as f:
        myDataList =f.readlines()
        nameList=[]
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])

        if name and dStr not in nameList:
            time_now =datetime.now()
            tStr= time_now.strftime('%d/%b/%Y')
            f.writelines(f'\n{name},\t{dStr},\t{tStr}')
           

cap=cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    imgS=cv2.resize(img,(0,0),None,0.25,0.25)
    imgS =cv2.cvtColor(imgS,cv2.COLOR_BGR2RGB)
    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame=face_recognition.face_encodings(imgS,facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame,facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
        faceDis =face_recognition.face_distance(encodeListKnown,encodeFace)
        print(faceDis)
        matchIndex =np.argmin(faceDis)

        if matches[matchIndex]:
            name=className[matchIndex].upper()

            time_now =datetime.now()#
            dStr = time_now.strftime('%H:%M:%S')
            
            
            y1,x2,y2,x1 = faceLoc
            y1,x2,y2,x1 =y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
            cv2.putText(img, name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)
            attendance(name,dStr)
    cv2.imshow("Camera", img)
    if cv2.waitKey(0) == 13:
        break

cap.release()
cv2.destroyAllWindows()