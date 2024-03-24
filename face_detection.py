import cv2
import mediapipe as mp
import imutils
import os
from datetime import date
from datetime import datetime
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
import joblib 
import serial

# # Number of images to take for each user
nimgs = 10
# Saving Date today in 2 different formats
datetoday = date.today().strftime("%m_%d_%y")
# Initializing VideoCapture object to access WebCam
face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
# If these directories don't exist, create them
# if not os.path.isdir('Attendance'):
#     os.makedirs('Attendance')
# if not os.path.isdir('./face_recognition'):
#     os.makedirs('./face_recognition')
# if not os.path.isdir('./face_recognition/ph'):
#     os.makedirs('./face_recognition/ph')
# if f'Attendance-{datetoday}.csv' not in os.listdir('Attendance'):
#     with open(f'Attendance/Attendance-{datetoday}.csv', 'w') as f:
#         f.write('Name,Year,Roll,Time')
# get a number of total registered users

arduino = serial.Serial(port='COM3', baudrate=9600, timeout=.1)

identified_person = ""

def write_read(x):
    arduino.write(bytes(x,'utf-8'))
    # time.sleep(0.1)
    pass

write_read("0 0")

def totalreg():
    return len(os.listdir('static/faces'))
# extract the face from an image
def extract_faces(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_points = face_detector.detectMultiScale(
        gray, 1.3, 3, minSize=(30, 30))
    return face_points
# # Identify face using ML model
def identify_face(facearray):
    model = joblib.load(r".\face_recognition\face_recognition_model.pkl")
    return model.predict(facearray)
# A function which trains the model on all the faces available in faces folder
def train_model():
    faces = []
    labels = []
    userlist = os.listdir('face_recognition/ph/')
    for user in userlist:
        for imgname in os.listdir(f'face_recognition/ph/{user}'):
            img = cv2.imread(f'face_recognition/ph/{user}/{imgname}')
            resized_face = cv2.resize(img, (50, 50))
            faces.append(resized_face.ravel())
            labels.append(user)
    faces = np.array(faces)
    knn = KNeighborsClassifier(n_neighbors=5)
    knn.fit(faces, labels)
    joblib.dump(knn, './face_recognition/face_recognition_model.pkl')

    
# # Extract info from today's attendance file in attendance folder
def extract_attendance():
    df = pd.read_csv(f'Attendance/Attendance-{datetoday}.csv')
    names = df['Name']
    years = df['Year']
    rolls = df['Roll']
    times = df['Time']
    l = len(df)
    return names, years, rolls, times, l
# # Add Attendance of a specific user
def add_attendance(name):
    username = name.split('_')[0]
    userrole = name.split('_')[1]
    userid = name.split('_')[2]
    current_time = datetime.now().strftime("%H:%M:%S")
    df = pd.read_csv(f'Attendance/Attendance-{datetoday}.csv')
    if int(userid) not in list(df['Roll']):
        with open(f'Attendance/Attendance-{datetoday}.csv', 'a') as f:
            f.write(f'\n{username},{userrole},{userid},{current_time}')
# def home():
#     names, rolls, times, l = extract_attendance()
#     return render_template('home.html', names=names, rolls=rolls, times=times, l=l, totalreg=totalreg())
            
from mediapipe.framework.formats import location_data_pb2
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils


def detect_face():
    if 'face_recognition_model.pkl' not in os.listdir(r".\face_recognition"):
        print('There is no trained model in the static folder. Please add a new face to continue.')
    cap = cv2.VideoCapture(0)
    with mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.6) as face_detection:
        while cap.isOpened():
            success, image = cap.read()
            image = imutils.resize(image, width=1000)
            if not success:
                print("Ignoring empty camera frame.")
                continue

            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = face_detection.process(image)
            (h, w) = image.shape[:2] 
            cv2.circle(image, (w//2, h//2), 7, (255, 255, 255), -1)

            # Draw the face detection annotations on the image.
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)    
            # cv2.line(image,0,0,"red", 0.5)   

            if results.detections:
                for detection in results.detections:
                    mp_drawing.draw_detection(image, detection)
                    location_data = detection.location_data
                    if location_data.format == location_data_pb2.LocationData.RELATIVE_BOUNDING_BOX:
                        bb = location_data.relative_bounding_box
                        bb_box = [
                            bb.xmin, bb.ymin,
                            bb.width, bb.height,
                        ]


                        x, y, width, height = bb_box[0], bb_box[1], bb_box[2], bb_box[3]
                        # cv2.imshow(image[y:y+height, x:x+width])

                        # Calculate the center point
                        center_x = (x + width / 2)*w
                        center_y = (y + height / 2)*h
                        center = (int(center_x), int(center_y))
                        cv2.circle(image, (int(center_x), int(center_y)), 7, (255, 255, 255), -1)

                        cv2.line(image, (w//2,h//2), center, (0, 255, 0), 2)
                        deg_x = int(((w/2 - center[0])/(w/2))*30)
                        deg_y = int(((h/2 - center[1])/(w/2))*30)
                        # cv2.plot(image)
                        #print(deg_x,deg_y)
                        write_read(str(deg_x)+" "+str(deg_y))


                    bboxC = detection.location_data.relative_bounding_box
                    ih, iw, _ = image.shape
                    x, y, w, h = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)

                    x, y, w, h = max(0, x), max(0, y), max(0, w), max(0, h)
                    # cv2.rectangle(image, (x, y), (x+w, y+h), (86, 32, 251), 1)
                    # cv2.rectangle(image, (x, y), (x+w, y-40), (86, 32, 251), -1)

                    # Extract face region
                    face = cv2.resize(image[y:y+h, x:x+w], (50, 50))
                identified_person_label = identify_face(face.reshape(1, -1))[0]
                global identified_person
                identified_person= f'{identified_person_label}'
                # print(identified_person)
                cv2.putText(image, identified_person, (x+5, y-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.imshow('recognition', image)
            if cv2.waitKey(1) == 27:
                break
    write_read("0 0")
    write_read("0 0")
    write_read("0 0")
    write_read("0 0")
    arduino.close()
    cap.release()
    cv2.destroyAllWindows()
    return


def add_face():
    newusername = input("Enter the new user: ")
    newuserrole = input("Enter the working place/role of new year: ")
    newuserid = input("Enter the new user id: ")
    userimagefolder = './face_recognition/ph/'+newusername+'_'+newuserrole+'_'+str(newuserid)
    if not os.path.isdir(userimagefolder):
        os.makedirs(userimagefolder)
    i, j = 0, 0
    cap = cv2.VideoCapture(0)
    with mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.6) as face_detection:
        while cap.isOpened():
            success, image = cap.read()
            image = imutils.resize(image, width=1000)
            if not success:
                print("Ignoring empty camera frame.")
                continue

            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = face_detection.process(image)
            (h, w) = image.shape[:2] 

    
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)    
            if results.detections:
                for detection in results.detections:
                    bboxC = detection.location_data.relative_bounding_box
                    ih, iw, _ = image.shape
                    x, y, w, h = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)

                    x, y, w, h = max(0, x), max(0, y), max(0, w), max(0, h)

            cv2.putText(image, f'Images Captured: {i}/{nimgs}', (30, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 20), 2, cv2.LINE_AA)
            if j % 10 == 0:
                name = newusername+'_'+str(i)+'.jpg'
                cv2.imwrite(userimagefolder+'/'+name, image[y:y+h, x:x+w])
                i += 1
            j += 1
            if j == nimgs*10:
                break
            cv2.imshow('Adding new User', image)
            if cv2.waitKey(1) == 27:
                break
    cap.release()
    cv2.destroyAllWindows()
    print('Training Model')
    train_model()