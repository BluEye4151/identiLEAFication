import socket
import Struct
import NeuralNetwork

class ServerPort:
    def __init__(self):
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverPort = 12345
        self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serverSocket.bind(('', self.serverPort))
        self.network = NeuralNetwork.NeuralNetwork('../model_gen2/model2_myCNN.h5')
        
    def receiveQuery(self):
        while True:
            self.serverSocket.listen(1)
            print('The server is ready to receive')
            message = Struct.MessageStruct()
            maxLength = message.getMaxTotalLength()
            connectionSocket, addr = self.serverSocket.accept()
            print('one client is connecting...',addr)
            count = 0
            while True:
                packet = connectionSocket.recv(maxLength).decode() #according to my protocol
                message.extractMessage(packet, number=count)
                count += 1
                if(message.getState()=='QueryTail'):
                    break
            print('processing...')
            message.convertMessage()
            result = self.__operateQuery(message)
            connectionSocket.send(result.encode())
            connectionSocket.close()
            
    def getCurrentQuery(self):
        return self.currentQuery
    
    def __operateQuery(self, Message):
        if(Message.getMode()=='NN'):
            return self.network.query(Message.getMessageBody())
        if(Message.getMode()=='DB'):
            pass
    