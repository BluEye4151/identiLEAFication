import socket

class ClientPort:
    def __init__(self, struct):
        self.serverName ='NCAMR'
        self.serverPort = 12345
        self.clientSocket = None
        self.struct = struct

    def __connectToServer(self):
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientSocket.settimeout(8)
        self.clientSocket.connect((self.serverName, self.serverPort))
        
    # use this method to test whether can connect to a certain site
    # connectiontest method
    def __connectToSite(self,testserver):
        s=socket.socket()
        s.settimeout(3)
        try:
            status = s.connect_ex(testserver)
            if status == 0:
                s.close()
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False
        
    def sendQuery(self):
        self.__connectToServer()
        for i in range(self.struct.getAmount()):
            part = self.struct.partMessage(i)
            nret = self.clientSocket.send(self.struct.wrapMessage(part,i).encode())
            #print(str(i) + ' : ' + str(nret)+' Bytes sent.')
        print('Waiting for reply...')
        result = self.clientSocket.recv(1024).decode()
        self.clientSocket.close()
        return result
        
    def testConnection(self):
        connectionScore = 0
        testSites = ['www.baidu.com','www.csdn.net','cnki.net','bilibili.com','scu.edu.cn']
        testNumber = len(testSites)
        for i in range(testNumber):
            connectionScore += self.__connectToSite((testSites[i],443))
        if(connectionScore<=1):
            return -1 # bad network connetion
        elif(connectionScore<=4):
            return 0 # network likely to be usable
        else:
            return 1 # network available