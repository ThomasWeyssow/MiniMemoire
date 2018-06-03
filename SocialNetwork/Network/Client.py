from kivy.event import EventDispatcher

import select
import socket
import queue
import pickle
import struct

from threading import Thread

from Network.MessageBuffer import MessageBuffer


class Client(EventDispatcher):

    PORT = 80
    instance = None

    def __init__(self, ipAddress, **kwargs):
        """
        Classe permettant de se connecter au serveur , de lui envoyer des données
        et de recevoir des données de sa part
        """
        self.register_event_type("on_connection_lost")
        self.register_event_type("on_data_received")
        super(Client, self).__init__(**kwargs)

        self.connected = True
        self.clientSocket = self.initConnection(ipAddress)
        self.inputs = [self.clientSocket]
        self.outputs = []
        self.buffer = None
        self.messageQueue = queue.Queue()

    def __new__(cls, *args, **kwargs):
        """
        Permet de s'assurer qu'il n'existe qu'une instance de cette classe

        :return: L'instance du Client
        :rtype: Client
        """
        if not cls.instance:
            cls.instance = super(Client, cls).__new__(cls, *args, **kwargs)

        return cls.instance

    def initConnection(self, ipAddress):
        """
        Initialisation du socket permettant de communiquer avec le serveur

        :return: Le socket
        :rtype: socket.socket
        """
        sock = None

        # Création du socket TCP
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error:
            self.connected = False

        # Optimisation du socket
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Connection du socket au serveur
        try:
            sock.connect((ipAddress, self.PORT))
        except socket.error:
            self.connected = False

        sock.setblocking(0)

        return sock

    def isConnected(self):
        """
        Permet de vérifier si la connexion avec le serveur existe

        :return: Vrai si la connexion existe, faux sinon
        :rtype: bool
        """
        return self.connected

    def start(self):
        """
        Boucle permettant la réception et l'envoi de données

        :return:
        :rtype: None
        """
        while self.inputs:

            readableFds, writableFds, inErrorFds = select.select(
                self.inputs, self.outputs, self.inputs, 0)

            # Réception de données
            if self.clientSocket in readableFds:

                if not self.buffer:
                    messageLength = self.clientSocket.recv(4)

                    if messageLength:
                        length, = struct.unpack('!I', messageLength)
                        self.buffer = MessageBuffer(length)
                    else:
                        self.dispatch("on_connection_lost")
                        self.closeSocket()
                else:
                    message = self.clientSocket.recv(self.buffer.bytesLeft())

                    if message:
                        completeMessage = self.buffer.addChunck(message)
                        if completeMessage:
                            self.buffer = None
                            data = pickle.loads(completeMessage)
                            self.dispatch("on_data_received", data)
                    else:
                        self.dispatch("on_connection_lost")
                        self.closeSocket()

            # Envoi de données
            if self.clientSocket in writableFds:
                try:
                    message = self.messageQueue.get_nowait()
                except queue.Empty:
                    message = None

                if message:
                    message = pickle.dumps(message)
                    length = len(message)
                    self.clientSocket.sendall(struct.pack('!I', length))
                    self.clientSocket.sendall(message)
                else:
                    self.outputs.remove(self.clientSocket)

            # Gestion des erreurs de connexion
            if self.clientSocket in inErrorFds:
                self.dispatch("on_connection_lost")
                self.closeSocket()

    def send(self, message):
        """
        Permet d'envoyer des données au serveur

        :param message: Les données à envoyer
        :type message: dict
        :return:
        :rtype: None
        """
        self.messageQueue.put(message)
        if self.clientSocket not in self.outputs:
            self.outputs += [self.clientSocket]

    def closeSocket(self):
        """
        Permet de fermer le socket

        :return:
        :rtype: None
        """
        self.inputs.remove(self.clientSocket)
        if self.clientSocket in self.outputs:
            self.outputs.remove(self.clientSocket)
        self.clientSocket.close()

    def on_connection_lost(self):
        """
        L'événement <on_connection_lost>

        :return:
        :rtype: None
        """
        pass

    def on_data_received(self, data):
        """
        L'événement <on_data_received>: passe les données reçues
        au récepteur de l'événement

        :param data: Les données reçues
        :type data: dict
        :return:
        :rtype: None
        """
        pass