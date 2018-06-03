import queue


class ClientSocket:

    def __init__(self, address):
        """
        Classe représentant le socket ouvert pour un utilisateur de
        l'application

        :param address:
        """
        self.address = address
        self.messageQueue = queue.Queue()
        self.buffer = None
        self.username = None

    def getAddress(self):
        """
        Getter de l'attribut address

        :return: L'addresse IP et le port associé au socket
        :rtype: str
        """
        return self.address

    def getMessageQueue(self):
        """
        Getter de l'attribut messageQueue

        :return: La queue de messages
        :rtype: queue.Queue
        """
        return self.messageQueue

    def getBuffer(self):
        """
        Getter de l'attribut buffer

        :return: Le buffer contenant les morceaux de messages reçus
        :rtype: MessageBuffer
        """
        return self.buffer

    def getUsername(self):
        """
        Getter de l'attribut username

        :return: Le nom d'utilisateur correspondant au socket
        :rtype: str
        """
        return self.username

    def setAddress(self, address):
        """
        Setter de l'attribut address

        :param address: L'addresse IP et le port associé au socket
        :type address: str
        :return:
        :rtype: None
        """
        self.address = address

    def setMessageQueue(self, messageQueue):
        """
        Setter de l'attribut messageQueue

        :param messageQueue: La queue de messages
        :type messageQueue: queue.Queue
        :return:
        :rtype: None
        """
        self.messageQueue = messageQueue

    def setBuffer(self, buffer):
        """
        Setter de l'attribut buffer

        :param buffer: Le buffer contenant les morceaux de messages reçus
        :type buffer: MessageBuffer
        :return:
        :rtype: None
        """
        self.buffer = buffer

    def setUsername(self, username):
        """
        Setter de l'attribut username

        :param username: Le nom d'utilisateur correspondant au socket
        :type username: str
        :return:
        :rtype: None
        """
        self.username = username

    def getMessage(self):
        """
        Permet de récupérer un message dans la queue de messages

        :return: Le message récupéré
        :rtype: str
        """
        try:
            message = self.messageQueue.get_nowait()
        except queue.Empty:
            message = None
        return message

    def putMessage(self, message):
        """
        Permet d'ajouter un message dans la queue de messages

        :param message: Le message à ajouter
        :type message: str
        :return:
        :rtype: None
        """
        self.messageQueue.put(message)

    def clearBuffer(self):
        """
        Permet de vider le buffer

        :return:
        :rtype: None
        """
        self.buffer = None