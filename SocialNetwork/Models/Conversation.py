class Conversation:

    def __init__(self, username, addresseeUsername, messages=None):
        """
        Classe représentant une conversation entre deux utilisateurs

        :param username: Le nom d'utilisateur de l'utilisateur connecté
        :type username: str
        :param addresseeUsername: Le nom d'utilisateur du correspondant
        :type addresseeUsername: str
        """
        self.username = username
        self.addresseeUsername = addresseeUsername
        self.messages = [] if not messages else messages

    def getUsername(self):
        """
        Getter de l'attribut username

        :return: Le nom d'utilisateur de l'utilisateur connecté à l'application
        :rtype: str
        """
        return self.username

    def getAddresseeUsername(self):
        """
        Getter de l'attribut addresseeUsername

        :return: Le nom d'utilisateur du correspondant
        :rtype: str
        """
        return self.addresseeUsername

    def getMessages(self):
        """
        Getter de l'attributs messages

        :return: Les messages échangés entre les utilisateurs
        :rtype: list
        """
        return self.messages

    def setUsername(self, username):
        """
        Setter de l'attribut username

        :param username: Le nouveau nom d'utilisateur
        :type username: str
        :return:
        :rtype: None
        """
        self.username = username

    def setAddresseeUsername(self, addresseUsername):
        """
        Setter de l'attribut addresseUsername

        :param addresseUsername: Le nouveau nom d'utilisateur du correspondant
        :type addresseUsername: str
        :return:
        :rtype: None
        """
        self.addresseeUsername = addresseUsername

    def setMessages(self, messages):
        """
        Setter de l'attribut messages

        :param messages: Les nouveaux messages échangés entre les utilisateurs
        :type messages: list
        :return:
        :rtype: None
        """
        self.messages = messages

    def addSentMessage(self, message):
        """
        Permet d'ajouter un message envoyé à la liste des messages

        :param message: Le nouveau message
        :type message: str
        :return:
        :rtype: None
        """
        self.messages += [(message, True)]

    def addReceivedMessage(self, message):
        """
        Permet d'ajouter un message reçu à la liste des messages

        :param message: Le nouveau message
        :type message: str
        :return:
        :rtype: None
        """
        self.messages += [(message, False)]

    def removeMessage(self, message):
        """
        Permet de retirer un message de la liste des messages

        :param message: Le message à retirer
        :type message: str
        :return:
        :rtype: None
        """
        self.messages.remove(message)