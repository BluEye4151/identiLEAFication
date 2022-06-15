import time
import numpy

class MessageStruct:
    #[{mode}, {total amount}, {source IP}, {time stamp}, {message}]
    def __init__(self, mode='', message=''):
        #===========================members====================================
        self.mode = mode # 'NN' for neural network query and 'DB' for database query
        ### DB won`t be using here due to change of architecture ###
        self.amount = -1 # the amount of packet that this message is to be divided into
        self.clientAddr = '0.0.0.0' # client IP address
        self.timeStamp=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) # time
        self.message = message # the main body of the message
        self.state = 'Continued'
        #====================parametres and init===============================
        self.maxTotalLength = 8192
        self.maxBodyLength = self.maxTotalLength-self.getLength(part='header')
        self.amount = len(self.message)//self.maxBodyLength+1
  
#========================= get methods ========================================
    def getMessageAll(self):
        completeMessage = ['',0,'','','','']
        completeMessage = [self.mode,self.amount,self.clientAddr,
                           self.timeStamp,self.message,self.state]
        return completeMessage
    
    def getMessageBody(self):
        return self.message
    
    def getLength(self, part='total'):
        length = 0
        if(part=='total'):
            length = len(self.mode) + len(str(self.amount)) + len(self.clientAddr)
            length+= len(self.timeStamp) + len(self.message) + len(self.state) + 5 # 5*'\n'
        elif(part=='body'):
            length = len(self.message)
        elif(part=='header'):
            length = (len(self.mode)+len(str(self.amount))
                      +len(self.clientAddr)+len(self.timeStamp)+len(self.state))+5 # 5*'\n'
        else:
            print('Bad part choice...')
            length = -1
        return length
    
    def getAmount(self):
        return self.amount
    
    def getState(self):
        return self.state
    
    def getMode(self):
        return self.mode
    
    def getMaxTotalLength(self):
        return self.maxTotalLength
   
#======================== application methods==================================
    # divide message part and get a part of 1000 bytes
    def partMessage(self, number): 
        self.maxBodyLength = self.maxTotalLength - self.getLength(part='header')
        bodyLength = self.maxBodyLength
        messagePart = ''
        # a message part of 1000 Bytes
        if(self.getLength(part='body') > (number+1)*bodyLength):
            messagePart = self.message[number*bodyLength:(number+1)*bodyLength]
        else:
            messagePart = self.message[number*bodyLength:]
        return messagePart
    
    # attach headers to a given part of message
    def wrapMessage(self, partedMessage, number, mode='string', querytail=False):
        if(number==self.amount-1):
            querytail = True
        wrappedMessage = ['',0,'','','','']
        wrappedMessage[0:4] = self.mode, self.amount, self.clientAddr, self.timeStamp
        wrappedMessage[4] = partedMessage
        if(mode=='string'):#[{mode},{amount},{source IP},{time stamp},{message},{finish?}]
            result = ''
            result+=(str(self.mode)+'\n')
            result+=(str(self.amount)+'\n')
            result+=(str(self.clientAddr)+'\n')
            result+=(str(self.timeStamp)+'\n')
            result+=(str(partedMessage)+'\n')
            if(querytail):
                result+=('QueryTail')
            else:
                result+=('Continued')
            return result
        elif(mode=='list'):
            if(querytail):
                wrappedMessage[5] = 'QueryTail'
            else:
                wrappedMessage[5] = 'Continued'
            return wrappedMessage
        else:
            print('Bad mode choice...')
            return -1
        
    # extract the struct of the user query, but mostly still in the form of string
    # number not 0 : join new parts to existing part
    def extractMessage(self, packet, number=0):
        msg = packet.split('\n')
        if(number==0):
            self.mode = msg[0]
            self.amount = int(msg[1])
            self.clientAddr = msg[2]
            self.timeStamp = msg[3]
            self.message = msg[4]
            self.state = msg[5]
        else:
            self.message += msg[4]
            self.state = msg[5]
        return
    
    # convert main message part to its correct form accordingly
    def convertMessage(self):
        if(self.mode=='NN'):
            temp = self.message.split(',')
            picVector = list(map(int,temp))
            picVector = numpy.array(picVector).reshape(1,256,256,3)/255.0
            self.message = picVector
        if(self.mode=='DB'):
            temp = self.message.split(',')
            picVector = list(map(int,temp))
            picVector = numpy.array(picVector).reshape(256,256,3)
        return self
    
def loadDictionary():
    # chinese to english
    fptr = open('./files/dictionary.txt','rt',encoding='utf-8')
    info = fptr.read().splitlines()
    fptr.close()
    dictionarylist = []
    dictionaryC2E = {}
    dictionaryE2C = {}
    for line in info:
        dictionarylist.append(line.split())
    for line in dictionarylist:
        dictionaryC2E.setdefault(line[1], line[0])
        dictionaryE2C.setdefault(line[0], line[1])
    return dictionaryC2E, dictionaryE2C