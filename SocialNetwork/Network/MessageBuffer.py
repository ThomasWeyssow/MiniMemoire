class MessageBuffer:

    def __init__(self, messageLength):
        """
        Classe représentant un buffer contenant message divisé en plusieurs
        morceaux

        :param messageLength: La taille du message
        :type messageLength: int
        """
        self.messageLength = messageLength
        self.bytesReceived = 0
        self.messageChuncks = []

    def bytesLeft(self):
        """
        Permet de savoir combien de bytes manquent pour que le message soit complet

        :return: Le nombre de bytes manquants
        :rtype: int
        """
        return self.messageLength - self.bytesReceived

    def addChunck(self, chunck):
        """
        Permet d'ajouter un morceaux au message

        :param chunck: Le morceau à ajouter
        :type chunck: byte
        :return: Le message s'il est complété, None sinon
        :rtype: bytearray
        """
        messageComplete = None

        self.bytesReceived += len(chunck)
        self.messageChuncks += [chunck]

        if self.bytesReceived == self.messageLength:
            messageComplete = b''.join(self.messageChuncks)

        return messageComplete