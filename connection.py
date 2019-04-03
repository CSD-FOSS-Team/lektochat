import socket
import multiprocessing
import struct


class ConnectionHandler:

    # This class will contain the following methods:

    # - handshakeListener()
    def __init__(self):
        self.stopHandshakeListening = False
        # Standard loopback interface address (localhost)
        self.HOST = '127.0.0.1'
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

                        self.connectedClients.append(
                            ConnectedClient(connectionSocket))
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

        self.requestHandlerProcess = multiprocessing.Process(
            target=self.requestHandler, args=(connectionSocket, ))
        self.requestHandlerProcess.start()

    def requestHandler(self, connectionSocket):

    def sendMsg(self, msg, sock):
        # Used to form the message that we will send in a proper form (length + message) and ensure that
        # the whole message will be sent at once

        # Prefix each message with a 4-byte length (network byte order)

        # https://stackoverflow.com/questions/9742449/sending-sockets-data-with-a-leading-length-value
        # https://stackoverflow.com/questions/17667903/python-socket-receive-large-amount-of-data

        msg = struct.pack('>I', len(msg)) + msg
        sock.sendall(msg)

    def receiveMsg(self, sock):
        # Will be used to ensure that the whole message is received every time through the socket

        # https://stackoverflow.com/questions/17667903/python-socket-receive-large-amount-of-data

        # Read message length and unpack it into an integer

        rawMsgLen = self.receiveAll(sock, 4)
        if not rawMsgLen:
            return None
        msgLen = struct.unpack('>I', rawMsgLen)[0]
        # Read the message data
        return self.receiveAll(sock, msgLen)

    def receiveAll(self, sock, n):
        # https://stackoverflow.com/questions/17667903/python-socket-receive-large-amount-of-data

        # Helper function to recv n bytes or return None if EOF is hit

        data = b''
        while len(data) < n:
            packet = sock.recv(n - len(data))
            if not packet:
                return None
            data += packet
        return data


class Server:
    # This class  will contain the following fields:
    # - info (struct) ???

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
