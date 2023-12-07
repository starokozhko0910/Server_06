import socket
import pickle
import struct
class Message:
    def __init__(self, socket):
        self.socket = socket
    def LoadMessage(self):
        data_length = int.from_bytes(self.socket.recv(4), byteorder='big')
        data = self.socket.recv(data_length)
        two_matrix = pickle.loads(data)
        return two_matrix['first_matrix'], two_matrix['second_matrix']

    def PushMessage(self, result_matrix):
        serialized_result = pickle.dumps({'Result': result_matrix})
        self.socket.sendall(len(serialized_result).to_bytes(5, byteorder='big'))
        self.socket.sendall(serialized_result)



