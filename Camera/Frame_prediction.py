import cv2
import numpy as np

class Attendance_Frame_prediction:

    def __init__(self, frame, facenet_model, ann_model, encoder):
        self.frame = frame
        self.facenet_model = facenet_model
        self.ann_model = ann_model
        self.encoder = encoder
    
    def package(self):
        self.frame = cv2.resize(self.frame, (160,160))
        self.frame = np.reshape(self.frame, (1,160,160,3))
        self.frame = self.facenet_model.embeddings(self.frame)
        self.prediction = self.ann_model.predict(self.frame)[0]
        self.accuracy = round(max(self.prediction)*100,2)
        self.label = self.encoder.inverse_transform([np.argmax(self.prediction)])[0]
        return [self.label, self.accuracy]

class Mask_prediction:

    def __init__(self,frame, mask_model):
        self.frame = frame
        self.mask_model = mask_model
        #self.mask_encoder = mask_encoder
        
    def package(self):
        self.frame = cv2.resize(self.frame, (160,160))
        self.frame = np.reshape(self.frame, (1,160,160,3))
        result = self.mask_model.predict(self.frame)[0]
        accuracy = round(max(result)*100,2)
        label = np.argmax(result)
        #label = self.mask_encoder.inverse_transform(label)[0]
        print("This is my label : ",label)
        return [label, accuracy]



        






        
