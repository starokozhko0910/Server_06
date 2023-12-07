import socket
import pickle
import numpy as np
from Message import Message
from concurrent.futures import ThreadPoolExecutor

class Server:

    def __init__(self, server_address):
        self.server_address = server_address

    def _matrix_multiply(self, fm, sm):
        return np.dot(fm, sm)

    def _satisfy_client(self, client_socket):
        try:
            mess = Message(client_socket)
            fm, sm = mess.LoadMessage()

            if fm.shape[1] != sm.shape[0]:
                error_message = "Помилка: Несумісні розміри масивів"
                client_socket.sendall(len(error_message).to_bytes(4, byteorder='big'))
                client_socket.sendall(error_message.encode())
                return
            result = self._matrix_multiply(fm, sm)
            mess.PushMessage(result)

        except Exception as e:
            error_message = f"Помилка: {str(e)}"
            client_socket.sendall(len(error_message).to_bytes(4, byteorder='big'))
            client_socket.sendall(error_message.encode())
        finally:
            client_socket.close()

    def start_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(self.server_address)
        server_socket.listen(5)

        with ThreadPoolExecutor(max_workers=5) as executor:
            try:
                while True:
                    client_socket, addr = server_socket.accept()
                    print(f"Отримали з\'єднання від: {addr}")
                    executor.submit(self._satisfy_client, client_socket)
            except KeyboardInterrupt:
                print("Сервер зупинено.")
            finally:
                server_socket.close()


