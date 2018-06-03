import sys
import select
import socket
import pickle
import struct

from DAO import DAO
from ClientSocket import ClientSocket
from MessageBuffer import MessageBuffer


class Server:

    PORT = 80

    def __init__(self):
        """
        Classe représentant un serveur permettant d'accepter des connexions
        TCP avec le côté client de l'application
        """
        self.welcomeSocket = self.initConnection()
        self.inputs = [self.welcomeSocket]
        self.outputs = []
        self.clients = {}

    def initConnection(self):
        """
        Initialisation du socket TCP de bienvenue

        :return: Le socket de bienvenue
        :rtype: socket.socket
        """
        # Création du socket TCP de bienvenue
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as error:
            print("Failed to create socket. Error code: {:d}, Error message: {:s}"
                  .format(error.args[0], error.args[1]))
            sys.exit()
        print("> Welcome socket creation complete")

        # Optimisation du socket
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print("> Welcome socket optimization complete")

        sock.setblocking(0)

        # Liaison du socket avec le port choisi
        try:
            sock.bind(('', self.PORT))
        except socket.error as error:
            print("Bind failed. Error code: {:d}, Error message: {:s}"
                  .format(error.args[0], error.args[1]))
            sys.exit()
        print("> Welcome socket binding complete")

        # Écoute des requêtes de connection
        sock.listen(10)
        print("> Welcome socket is now listening")

        return sock

    def start(self):
        """
        Boucle principale permettant de gérer les demandes de connexion, l'envoi et
        la réception de messages

        :return:
        :rtype: None
        """
        while self.inputs:

            readableFds, writableFds, inErrorFds = select.select(
                self.inputs, self.outputs, self.inputs)

            # Réception de messages
            for fd in readableFds:

                # Réception d'une demande de connexion
                if fd is self.welcomeSocket:
                    self.handleConnectionRequest()

                # Réception d'un message
                else:
                    self.receiveMessageChunck(fd)

            # Envoi d'un message
            for fd in writableFds:
                self.sendMessage(fd)

            # Gestion des erreurs de connexion
            for fd in inErrorFds:
                self.closeClientSocket(fd)

    def handleConnectionRequest(self):
        """
        Permet de gérer une demande de connexion au serveur

        :return:
        :rtype: None
        """
        (clientSocket, (addr, port)) = self.welcomeSocket.accept()
        clientSocket.setblocking(0)

        self.inputs += [clientSocket]

        address = "{:s}:{:d}".format(addr, port)
        self.clients[clientSocket] = ClientSocket(address)

        print("> [+] New connection socket opened for {:s}".format(
            address))

    def sendMessage(self, sock):
        """
        Permet d'envoyer un message au travers d'un socket ouvert pour un client

        :param sock: Le socket
        :type sock: socket.socket
        :return:
        :rtype: None
        """
        data = self.clients[sock].getMessage()

        if data:
            data = pickle.dumps(data)
            length = len(data)
            sock.sendall(struct.pack('!I', length))
            sock.sendall(data)
        else:
            self.outputs.remove(sock)

    def receiveMessageChunck(self, sock):
        """
        Permet de gérer la réception d'un morceau de message de la part d'un client
        connecté au serveur

        :param sock: Le socket ouvert pour le client
        :type sock: socket.socket
        :return:
        :rtype: None
        """
        client = self.clients[sock]
        clientBuffer = client.getBuffer()

        # Création d'un buffer s'il s'agit du premier morceau du message
        if not clientBuffer:

            messageLength = sock.recv(4)

            if messageLength:
                length, = struct.unpack('!I', messageLength)
                client.setBuffer(MessageBuffer(length))
            else:
                self.closeClientSocket(sock)

        # Remplissage du buffer sinon
        else:

            message = sock.recv(clientBuffer.bytesLeft())

            if message:
                completeMessage = clientBuffer.addChunck(message)

                # Si le message est complété, gestion de la requête
                if completeMessage:
                    client.clearBuffer()
                    self.handleRequestReceived(
                        sock, pickle.loads(completeMessage))

            else:
                self.closeClientSocket(sock)

    def closeClientSocket(self, clientSocket):
        """
        Permet de fermer un socket

        :param clientSocket: Le socket à fermer
        :type clientSocket: socket.socket
        :return:
        :rtype: None
        """
        clientAddress = self.clients[clientSocket].getAddress()

        print("> Connection with {:s} lost".format(clientAddress))

        self.inputs.remove(clientSocket)
        if clientSocket in self.outputs:
            self.outputs.remove(clientSocket)
        del self.clients[clientSocket]
        clientSocket.close()

        print("> [-] Connection socket opened for {:s} closed".format(
            clientAddress))

    def registerClientUsername(self, clientSocket, username):
        """
        Permet d'associer un nom d'utilisateur au socket correspondant

        :param clientSocket: Le socket
        :type clientSocket: socket.socket
        :param username: Le nom d'utilisateur
        :type username: str
        :return:
        :rtype: None
        """
        self.clients[clientSocket].setUsername(username)

    def getClientSocketByUsername(self, username):
        """
        Permet de récupérer un socket sur base d'un nom d'utilisateur

        :param username: Le nom d'utilisateur
        :type username: str
        :return: Le socket correspondant
        :rtype: socket.socket
        """
        clientSocket = None

        for sock, client in self.clients.items():
            if client.getUsername() == username:
                clientSocket = sock

        return clientSocket

    def send(self, clientSocket, message):
        """
        Permet de préparer un message à l'envoi au travers du socket d'un client

        :param clientSocket: Le socket du client
        :type clientSocket: socket.socket
        :param message: Le message à envoyer
        :type message: dict
        :return:
        :rtype: None
        """
        self.clients[clientSocket].putMessage(message)
        if clientSocket not in self.outputs:
            self.outputs += [clientSocket]

    def handleRequestReceived(self, clientSocket, data):
        """
        Permet de gérer la réception d'une requête provenant d'un client

        :param clientSocket: Le socket du client
        :type clientSocket: socket.socket
        :param data: La requête
        :type data: dict
        :return:
        :rtype: None
        """
        request = data["request"]

        if request == "signIn":
            print("> Sign in request received from {:s}".format(
                self.clients[clientSocket].getAddress()))

            self.handleSignInRequest(
                clientSocket, data["username"], data["password"])

        elif request == "signUp":
            print("> Sign up request received from {:s}".format(
                self.clients[clientSocket].getAddress()))

            self.handleSignUpRequest(clientSocket, data["userData"])

        elif request == "search":
            print("> Search request received from {:s}".format(
                self.clients[clientSocket].getAddress()))

            self.handleSearchRequest(data["username"], data["searchInput"])

        elif request == "displayOtherUserProfile":
            print("> Profile request received from {:s}".format(
                self.clients[clientSocket].getAddress()))

            self.handleOtherUserProfileRequest(
                data["username"], data["otherUsername"])

        elif request == "publication":
            print("> Publication request received from {:s}".format(
                self.clients[clientSocket].getAddress()))

            self.handlePublicationRequest(data["publication"])

        elif request == "friendRequest":
            print("> Friend request received from {:s}".format(
                self.clients[clientSocket].getAddress()))

            self.handleFriendRequest(
                data["username"], data["otherUsername"])

        elif request == "friendRequestResponse":
            print("> Add friend request received from {:s}".format(
                self.clients[clientSocket].getAddress()))

            self.handleFriendRequestResponse(
                data["username"], data["otherUsername"], data["accepted"])

        elif request == "sendMessage":
            print("> Send message request received from {:s}".format(
                self.clients[clientSocket].getAddress()))

            self.handleSendMessage(
                data["username"], data["otherUsername"], data["message"])

        elif request == "notificationsRead":
            print("> Notifications read request received from {:s}".format(
                self.clients[clientSocket].getAddress()))

            self.handleNotificationsRead(data["username"])

        elif request == "changePrivacySetting":
            print("> Change privacy settings request received from {:s}".format(
                self.clients[clientSocket].getAddress()))

            self.handleChangePrivacySettings(
                data["username"], data["setting"])

        elif request == "comment":
            print("> New comment request received from {:s}".format(
                self.clients[clientSocket].getAddress()))

            self.handleAddComment(
                data["username"], data["otherUsername"], data["comment"])

    def handleSignInRequest(self, clientSocket, username, password):
        """
        Permet de gérer la récpetion d'une reqête de connexion à l'application

        :param clientSocket: Le socket correspondant à l'utilisateur
        :type clientSocket: socket.socket
        :param username: Le nom d'utilisateur
        :type username: str
        :param password: Le mot de passe de l'utilisateur
        :type password: str
        :return:
        :rtype: None
        """
        reply = {
            "request": "signIn",
            "isValid": False,
            "userData": None
        }

        db = DAO("Users.db")

        # Vérification du mot de passe
        if db.userIsValid(username, password):

            reply["userData"] = db.getUserInfos(username)
            reply["isValid"] = True

            # Enregistrement du nom d'utilisateur; le serveur peut alors
            # l'utiliser pour trouver le socket correspondant à cet utilisateur
            self.registerClientUsername(clientSocket, username)

        db.close()

        # Envoi de la validation au client
        self.send(clientSocket, reply)

    def handleSignUpRequest(self, clientSocket, userData):
        """
        Permet de gérer la réception d'une requête d'enregistrement à l'application

        :param clientSocket: Le socket correspondant à l'utilisateur
        :type clientSocket: socket.socket
        :param userData: Les données correspondantes à la requête
        :type userData: dict
        :return:
        :rtype: None
        """
        reply = {"request": "signUp", "isValid": False}

        # Modification de la base de donnée si la requête est valide
        db = DAO("Users.db")
        if not (db.usernameExists(userData["username"]) or
                db.passwordExists(userData["password"])):
            reply["isValid"] = True
            db.addUser(userData)
        db.close()

        # Envoi de la validation au client
        self.send(clientSocket, reply)

    def handleSearchRequest(self, username, searchInput):
        """
        Permet de gérer une reqête de recherche d'autres utilisateurs

        :param username: L'utilisateur ayant envoyé la requête
        :type username: str
        :param searchInput: La recherche entrée par l'utilisateur
        :type searchInput: str
        :return:
        :rtype: None
        """
        # Récupération des donées de recherche
        firstWord = searchInput[0]
        secondWord = searchInput[1] if len(searchInput) == 2 else None

        # Recherche dans la base données
        db = DAO("Users.db")
        results = db.search(firstWord, secondWord)
        db.close()

        # Envoi des résultats au client
        reply = {"request": "search", "results": results}
        userSocket = self.getClientSocketByUsername(username)
        self.send(userSocket, reply)

    def handleOtherUserProfileRequest(self, username, otherUsername):
        """
        Permet de gérer une requête d'affichage du profil d'un autre
        utilisateur

        :param username: Le nom d'utilisateur de l'émetteur de la requête
        :type username: str
        :param otherUsername: L'autre utilisateur
        :type otherUsername: str
        :return:
        :rtype: None
        """
        # Récupération des données dans la base donnée
        db = DAO("Users.db")
        reply = {
            "request": "displayOtherUserProfile",
            "otherUserInfos": db.getOtherUserInfos(username, otherUsername)
        }
        db.close()

        # Envoi des données à l'utilisateur
        userSocket = self.getClientSocketByUsername(username)
        self.send(userSocket, reply)

    def handleFriendRequest(self, username, otherUsername):
        """
        Gestion de la réception d'une demande d'ami

        :param username: L'émetteur de la requête
        :type username: str
        :param otherUsername: L'utilisateur concerné par la demande
        :type otherUsername: str
        :return:
        :rtype: None
        """
        notification = "{:s} sent you a friend request!".format(username)

        # Enregistrement de la demande dans la base de donnée
        db = DAO("Users.db")
        db.addReceivedFriendRequest(otherUsername, username)
        db.addSentFriendRequest(username, otherUsername)
        db.addNotification(otherUsername, notification)
        db.close()

        # Envoi de la demande à l'ami s'il est actuellement connecté
        friendSocket = self.getClientSocketByUsername(otherUsername)
        if friendSocket:
            reply = {"request": "friendRequest", "username": username}
            self.send(friendSocket, reply)

    def handleFriendRequestResponse(self, username, otherUsername, accepted):
        """
        Gestion de la réception d'une réponse à une demande d'ami

        :param username: L'émetteur de la réponse
        :type username: str
        :param otherUsername: L'utilisateur ayant envoyé la demande d'ami
        :type otherUsername: str
        :param accepted: Indique si la demande est acceptée ou non
        :type accepted: bool
        :return:
        :rtype: None
        """
        if accepted:
            notification = "{:s} accepted your friend request!".format(username)
        else:
            notification = "{:s} refused your friend request!".format(username)

        db = DAO("Users.db")

        # Suppression de la demande d'ami
        db.removeReceivedFriendRequest(username, otherUsername)
        db.removeSentFriendRequest(otherUsername, username)
        # Enregistrement de l'ami dans la base de donnée si la demande est acceptée
        if accepted:
            db.addFriend(username, otherUsername)
        db.addNotification(otherUsername, notification)

        # Envoi de la réponse à la demande à l'ami s'il est actuellement connecté
        friendSocket = self.getClientSocketByUsername(otherUsername)
        if friendSocket:
            reply = {
                "request": "friendRequestResponse",
                "otherUsername": username,
                "accepted": accepted
            }
            self.send(friendSocket, reply)

        db.close()

    def handlePublicationRequest(self, publicationData):
        """
        Permet de gérer la réception d'une requête de publication

        :param publicationData: Les données correspondantes à la publication
        :type publicationData: dict
        :return:
        :rtype: None
        """
        username = publicationData["username"]
        identifier = publicationData["identifier"]
        publication = publicationData["publication"]

        notification = "{:s} published something!".format(username)

        db = DAO("Users.db")
        db.addPublication(username, identifier, publication)

        # Enregistrement de la publication dans les entrées de la base de donnée
        # correspondants aux amis de l'utilisateur
        for friendUsername in db.getFriends(username):

            # Ajout de la publication dans le fil d'actualité des amis de
            # l'utilisateur
            db.addFeed(friendUsername, username, identifier, publication)
            db.addNotification(friendUsername, notification)

            # Envoi de la publication aux amis de l'utilisateur qui sont
            # actuellement connectés
            friendSocket = self.getClientSocketByUsername(friendUsername)
            if friendSocket:
                reply = {
                    "request": "feed",
                    "feed": publicationData
                }
                self.send(friendSocket, reply)

        db.close()

    def handleSendMessage(self, username, otherUsername, message):
        """
        Gestion de la réception d'une requête d'envoi de message à un autre
        utilisateur

        :param username: L'émetteur de la requête
        :type username: str
        :param otherUsername: L'utilisateur devant recevoir le message
        :type otherUsername: str
        :param message: Le message
        :type message: str
        :return:
        :rtype: None
        """
        notification = "You received a message from {:s}!".format(username)

        # Mise à jour de la base de données
        db = DAO("Users.db")
        db.addMessage(username, otherUsername, message)
        db.addNotification(otherUsername, notification)
        db.close()

        # Envoi du message au récepteur s'il est connecté
        otherUserSocket = self.getClientSocketByUsername(otherUsername)
        if otherUserSocket:
            reply = {
                "request": "sendMessage",
                "otherUsername": username,
                "message": message
            }
            self.send(otherUserSocket, reply)

    def handleNotificationsRead(self, username):
        """
        Gestion d'une requête d'indication que les notifications ont été lues

        :param username: L'émetteur de la requête
        :type username: str
        :return:
        """
        db = DAO("Users.db")
        db.markNotificationsAsRead(username)
        db.close()

    def handleChangePrivacySettings(self, username, setting):
        """
        Gestion d'une requête de changement de préférence de privacité

        :param username: L'émetteur de la requête
        :type username: str
        :param setting: Le nouveau paramètre de privacité
        :type setting: str
        :return:
        :rtype: None
        """
        db = DAO("Users.db")
        db.updatePrivacySetting(username, setting)
        db.close()

    def handleAddComment(self, username, otherUsername, comment):
        """
        Permet de gérer la réception d'un commentaire d'une publication

        :param username: L'émetteur du commentaire
        :type username: str
        :param otherUsername: L'auteur de la publication
        :type otherUsername: str
        :param comment: Les données concernant le commentaire
        :type comment: dict
        :return:
        :rtype: None
        """
        notification = "{:s} commented one of your publications!"\
            .format(otherUsername)

        db = DAO("Users.db")
        db.addCommentToPublication(otherUsername, comment)
        db.addNotification(otherUsername, notification)

        # Envoi du commentaire à l'auteur de la publication
        userSocket = self.getClientSocketByUsername(otherUsername)
        if userSocket:
            reply = {
                "request": "comment",
                "comment": comment
            }
            self.send(userSocket, reply)

        # Envoi du commentaire aux amis de l'auteur de la publication
        for friend in db.getFriends(otherUsername):
            if db.addCommentToFeed(friend, comment):
                friendSocket = self.getClientSocketByUsername(friend)
                if friendSocket and \
                        (friend != otherUsername) and \
                        (friend != username):
                    reply = {
                        "request": "feedComment",
                        "comment": comment
                    }
                    self.send(friendSocket, reply)

        db.close()


if __name__ == '__main__':

    try:
        Server().start()
    except KeyboardInterrupt:
        print("> Server stopped")
