import os
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"  
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
from tensorflow.keras.models import load_model
from tensorflow.keras.models import Sequential
import numpy
from PIL import Image

class NeuralNetwork:
    def __init__(self, modelPath):
        # variables
        self.__leafCategory = []
        self.__model = Sequential()
        
        # initiating methods
        self.__loadCategory()
        self.__loadModel(modelPath)
        
#================================ load method ================================#
    def __loadCategory(self):
        fptr = open('./files/leafCategory.txt','r+')
        while(True):
            record = fptr.readline().replace('\n','')
            if(record == ''):
                break
            self.__leafCategory.append(record)
        fptr.close()
    def __loadModel(self, modelPath):
        self.__model = load_model(modelPath)
    
#============================ application method =============================#
    def queryDEBUG(self,number):
        imgPath = '../PlantVillage/Apple___Apple_scab/1_'+str(number)+'.JPG'
        img = Image.open(imgPath)
        img = numpy.array(img).reshape(1,256,256,3)/255.0
        result = self.__model.predict(img)
        category = numpy.argmax(result)
        category = self.__leafCategory[category]
        return category
    
    # assuming that previous steps have already resize to a correct form
    # correct form: numpy.array(image).reshape(1,256,256,3)/255.0
    def query(self, img):
        result = self.__model.predict(img)
        category = numpy.argmax(result)
        category = self.__leafCategory[category]
        return category
    
    def train(self):
        pass