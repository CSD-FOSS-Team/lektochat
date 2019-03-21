import socket
import multiprocessing


class ConnectionHandler:

    # This class will contain the following methods:

    # - handshakeListener()
    def __init__(self):
        self.stopHandshakeListening = False
        self.HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
        self.PORT = 7890  # Port to listen on (non-privileged ports are > 1023)
        self.connectedClients = []
        self.handshakeListener()



    def handshakeListener(self):
        print("*** Server is up and running! ***")

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as handshakeSocket:

            handshakeSocket.bind((self.HOST, self.PORT))
            handshakeSocket.listen(5)

            while not self.stopHandshakeListening:
                # accept an incoming handshake from a new client,
                # and create a new socket for this particular client

                connectionSocket, connectionAddress = handshakeSocket.accept()
                with connectionSocket:
                    print('Connected by', connectionAddress)

                    # create a new thread to run the request handler
                    # for this specific connection
                    try:

                        self.connectedClients.append(ConnectedClient(connectionSocket))
                    except:
                        print("Error: unable to start thread")


                    # while True:
                    #     data = conn.recv(1024)
                    #     if not data:
                    #         break
                    #     conn.sendall(data)


    def connectToServer(self):



    def createConnectedClient(self):






class ConnectedClient:
    # This class will contain the following methods:
    # send()
    # receive()
    # requestHandler()

    def __init__(self, connectionSocket):

        self.requestHandlerProcess = multiprocessing.Process(target=self.requestHandler, args=(connectionSocket, ))
        self.requestHandlerProcess.start()



    def requestHandler(self, connectionSocket):

    def send(self):

    def receive(self):






class Server:
    # This class  will contain the following fields:
    # - info (struct) ???

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port