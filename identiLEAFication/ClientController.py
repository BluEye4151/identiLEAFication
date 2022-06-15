import ClientPort
import numpy
import Struct
from PIL import Image
import NeuralNetwork
import pymysql

class ClientController:
    def __init__(self): # load necessary data and code when lauching the programme
        self.neuralNetwork = NeuralNetwork.NeuralNetwork('../model_gen2/model2_myCNN.h5')
        self.conn = pymysql.connect(host='127.0.0.1',user='Yy', 
                                    passwd='20011231YYydmYHQ', db="plantvillage")
        self.cursor=self.conn.cursor()
        
    #======================neural network related methods=====================#
    def __normalizeMessage(self,img):
        img = img.resize((256,256))
        pic = numpy.array(img).reshape(256*256*3)
        stringpic = ''
        for i in range(len(pic)):
            stringpic+=(str(pic[i])+',')
        stringpic = stringpic[:len(stringpic)-1]
        return stringpic

    def queryNN(self, message): # not finished yet, the API needs changeing
        struct = Struct.MessageStruct(mode='NN', message=self.__normalizeMessage(message))
        port = ClientPort.ClientPort(struct)
        if(port.testConnection()==1):
            return port.sendQuery()
        else:
            pic= message.resize((256,256))
            pic = numpy.array(pic).reshape(1,256,256,3)/255.0
            result = self.neuralNetwork.query(pic)
            return result
        
    #========================database related methods=========================#
    def authorization(self, newAuthority=''):
        if(newAuthority!='admin' and 'user'):
            print('bad authorization choice from DatabaseStruct')
            return
        self.authority = newAuthority
    
    def inquire(self, query, mode):
        # 查询内容:叶片图像、病害细节、纲-科关系、科-种关系、种-病害关系
        # 分别属于mode=image mode=detail mode=relation
        self.cursor.execute(query)
        result = []
        while True:
            Tuple = self.cursor.fetchone()
            if Tuple is None:
                break
            result.append(list(Tuple))
        # decode return message
        if mode=='relation':
            return result
        elif mode=='info':
            for i in range(len(result)):
                result[i][2] = result[i][2].decode()
                result[i][3] = result[i][3].decode()
            return result
        elif mode=='image':
            for i in range(len(result)):
                temp = result[i][2].decode().split(',')
                picVector = list(map(int,temp))
                picVector = numpy.array(picVector).reshape(256,256,3)
                result[i][2] = Image.fromarray(numpy.uint8(picVector))
            return result
        elif mode=='table':
            try:
                result[0][0] = result[0][0].decode()
            except:
                result[0][0] = result[0][0]    
            return result[0][0]
        else:
            print('bad mode selection in DatabaseStruct.inquire()...')
            return -1     