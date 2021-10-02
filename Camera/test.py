import pickle
import os
mask_encoder = pickle.load(open(os.getcwd() + "/Training/AI_Models/Mask_encoder.pickle","rb"))
print(mask_encoder.inverse_transform([1])[0])
