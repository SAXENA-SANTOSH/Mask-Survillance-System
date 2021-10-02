import os
import cv2
import pickle
import cvlib as cv
from json import load
from keras_facenet import FaceNet
from tensorflow.keras.models import load_model
from Frame_prediction import Attendance_Frame_prediction, Mask_prediction

class Camera:

    def __init__(self):
        self.path = os.getcwd()
        self.facenet = FaceNet()
        self.ann_model = load_model(self.path+"/Training/AI_Models/Attendance_System_AI_Model.model")
        self.encoder = pickle.load(open(self.path + "/Training/AI_Models/Attendance_encoder.pickle","rb"))
        self.mask_model = load_model(self.path + "/Training/AI_Models/Mask.model")
        self.mask_encoder = pickle.load(open(self.path + "/Training/AI_Models/Mask_encoder.pickle","rb"))


    def package(self):
        vid = cv2.VideoCapture(0)
        while True:
            ret, frame = vid.read()
                
            if(ret):
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.flip(frame , 1)
                self.frame = frame
                face_detection = cv.detect_face(frame)
                timer = cv2.getTickCount()
                fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
                for box , confidence in zip(face_detection[0] , face_detection[1]):
                    if(confidence > 0.9):
                        x1 , y1  = box[0] , box[1]
                        x2 , y2 = box[2] , box[3] 
                        self.frame = self.frame[y1:y2, x1:x2]
                        mask_results, mask_accuracy = Mask_prediction(self.frame, self.mask_model).package()
                        #print(mask_results)
                        #mask_results = self.mask_encoder.inverse_transform([mask_results])[0]
                        if(mask_results == 0):
                            attendance_results, attendance_accuracy = Attendance_Frame_prediction(frame=frame, facenet_model=self.facenet, ann_model=self.ann_model, encoder=self.encoder).package()
                            if(attendance_accuracy < 80):
                                attendance_results = "Unknown Person"
                                attendance_accuracy = round(100 - attendance_accuracy,2)
                            label = "Mask : Mask OFF, Mask Accuracy : {}% , Name : {} , Accuracy : {} %".format(mask_accuracy,attendance_results, attendance_accuracy)
                            cv2.rectangle(frame, (x1,y1), (x2,y2), (255,0,0), 3)
                            cv2.putText(frame, label, (x1 - 430,y1 - 20),  cv2.FONT_HERSHEY_SIMPLEX,0.7, (255,0,0), 2)
                            cv2.putText(frame, "FPS : " + str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,255,0), 2)
                        else:
                            label = "Mask : Mask ON , Mask Accuracy {} %".format(mask_accuracy)
                            cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,0), 3)
                            cv2.putText(frame, label, (x1 - 50,y1 - 10),  cv2.FONT_HERSHEY_SIMPLEX,0.7, (0,255,0), 2)
                            cv2.putText(frame, "FPS : " + str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,255,0), 2)
                    else:
                        continue
            else:
                continue
            
            
            cv2.imshow('frame', cv2.cvtColor(frame,cv2.COLOR_BGR2RGB))



            if cv2.waitKey(1) & 0xFF == ord('q'):
                vid.release()
                cv2.destroyAllWindows()
                break
                
  
Camera().package()

 
  
