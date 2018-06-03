import shelve
import copy


class DAO:

    def __init__(self, name):
        """
        Classe représentant une base de donnée en utilisant le module shelve

        :param name: Le chemin vers le fichier contenant la base de données
        :type name: str
        """
        self.db = shelve.open(name, writeback=True)

    def addUser(self, userInfos):
        """
        Permet d'ajouter un utilisateur à la base de données

        :param userInfos: Les informations concernant l'utilisateur
        :type userInfos: dict
        :return:
        :rtype: None
        """
        self.db[userInfos["username"]] = {
            "username": userInfos["username"],
            "password": userInfos["password"],
            "firstName": userInfos["firstName"],
            "lastName": userInfos["lastName"],
            "email": userInfos["email"],
            "publications": [],
            "friends": [],
            "receivedFriendRequests": [],
            "sentFriendRequests": [],
            "activityFeed": [],
            "conversations": [],
            "notifications": [],
            "notificationsViewed": True,
            "privacySetting": "everybody"
        }

    def close(self):
        """
        Permet de fermer la base de donnée

        :return:
        :rtype: None
        """
        self.db.close()

    def usernameExists(self, username):
        """
        Permet de vérifier si un nom d'utilisateur existe déjà dans la
        base de données

        :param username: Le nom d'utilisateur à vérifier
        :type username: str
        :return: Vrai si le nom d'utilisateur existe, faux sinon
        :rtype: bool
        """
        return username in self.db

    def passwordExists(self, password):
        """
        Permet de vérifier si un mot de passe existe déjà dans la base de données

        :param password: Le mot de passe à vérifier
        :type password: str
        :return: Vrai si le mot de passe existe, faux sinon
        :rtype: bool
        """
        passwordExist = any(
            (("password", password) in self.db[user].items()) for user in self.db
        )
        return passwordExist

    def userIsValid(self, username, password):
        """
        Permet de vérifier si un mot de passe donné correspond à un nom
        d'utilisateur donné

        :param username: Le nom d'utilisateur
        :type username: str
        :param password: Le mot de passe
        :type password: str
        :return: Vrai si le mat de passe correspond, faux sinon
        :rtype: bool
        """
        userIsValid = (self.usernameExists(username) and
                       self.db[username]["password"] == password)
        return userIsValid

    def getUserInfos(self, username):
        """
        Permet de récupérer les informations concernant un utilisateur
        connecté à l'application

        :param username: L'utilisateur
        :type username: str
        :return: Les informations concernant l'utilisateur
        :rtype: dict
        """
        userInfos = copy.deepcopy(self.db[username])
        del userInfos["password"]
        return userInfos

    def getOtherUserInfos(self, username, otherUsername):
        """
        Permet de réupérer les informations d'une autre utilisateur dans la
        base de donnée

        :param username: L'utilisateur connecté à l'application
        :type username: str
        :param otherUsername: L'autre utilisateur
        :type otherUsername: str
        :return: Les informations concernant l'autre utilisateur
        :rtype: dict
        """
        otherUserInfos = {
            "username": self.db[otherUsername]["username"],
            "firstName": self.db[otherUsername]["firstName"],
            "lastName": self.db[otherUsername]["lastName"],
            "privacySetting": self.db[otherUsername]["privacySetting"],
        }

        if not self.otherUserInfosAreHidden(username, otherUsername):
            otherUserInfos["email"] = self.db[otherUsername]["email"]
            otherUserInfos["publications"] = self.db[otherUsername]["publications"]
            otherUserInfos["friends"] = self.db[otherUsername]["friends"]

        return otherUserInfos

    def otherUserInfosAreHidden(self, username, otherUsername):
        """
        Permet de savoir si les informations personnelles d'un autre utilisateur
        peuvent être vues par l'utilisateur connecté à l'application

        :param username: L'utilisateur connecté à l'application
        :type username: str
        :param otherUsername: L'autre utilisateur
        :type otherUsername: str
        :return: Vrai si les infos peuvent être vues, faux sinon
        :rtype: bool
        """
        privacySetting = self.db[otherUsername]["privacySetting"]

        infosAreHidden = ((privacySetting == "nobody") or
                          ((privacySetting == "friendsOnly") and
                           (username not in self.db[otherUsername]["friends"])))

        return infosAreHidden

    def search(self, firstWord, secondWord):
        """
        Permet de rechercher des utilisateurs dans la base de données sur base
        d'une partie de nom d'utilisateur ou de nom

        :param firstWord: Une partie du nom d'utilisateur ou du prénom
        :type firstWord: str
        :param secondWord: Une partie du nom de famille de l'utilisateur
        :type secondWord: str
        :return: Les informations concernant les utilisateurs trouvés
        """
        results = []

        # Si 'secondWord' est à None, 'firstWord' est un nom d'utilisateur
        if not secondWord:
            for user in self.db:

                # Condition pour laquelle l'utilisateur est valide
                test = firstWord in user or \
                       firstWord in self.db[user]["firstName"] or \
                       firstWord in self.db[user]["lastName"]

                if test:
                    results += [{
                        "username": self.db[user]["username"],
                        "firstName": self.db[user]["firstName"],
                        "lastName": self.db[user]["lastName"]
                    }]

        # Sinon, 'firstWord' et 'secondWord' sont respectivement un prénom et
        # un nom ou un nom et un prénom
        else:
            for user in self.db:

                # Conditions pour lesquelles l'utilisateur est valide
                test1 = (firstWord in self.db[user]["firstName"]) and \
                        (secondWord in self.db[user]["lastName"])
                test2 = (firstWord in self.db[user]["lastName"]) and \
                        (secondWord in self.db[user]["firstName"])

                if test1 or test2:
                    results += [{
                        "username": self.db[user]["username"],
                        "firstName": self.db[user]["firstName"],
                        "lastName": self.db[user]["lastName"]
                    }]

        return results

    def addReceivedFriendRequest(self, username, friend):
        """
        Permet d'enregistrer une demande d'ami reçue

        :param username: L'utilisateur ayant reçu la demande
        :type username: str
        :param friend: L'utilisateur ayant envoyé la demande
        :type friend: str
        :return:
        :rtype: None
        """
        self.db[username]["receivedFriendRequests"] += [friend]

    def removeReceivedFriendRequest(self, username, friend):
        """
        Permet de supprimer une demande d'ami reçue

        :param username: L'utilisateur ayant reçu la demande
        :type username: str
        :param friend: L'utilisateur ayant envoyé la demande
        :type friend: str
        :return:
        :rtype: None
        """
        self.db[username]["receivedFriendRequests"].remove(friend)

    def addSentFriendRequest(self, username, otherUsername):
        """
        Permet d'enregistrer une demande d'ami envoyée

        :param username:      L'emetteur de la demande
        :type username: str
        :param otherUsername: Le récepteur de la demande
        :type otherUsername: str
        :return:
        :rtype: None
        """
        self.db[username]["sentFriendRequests"] += [otherUsername]

    def removeSentFriendRequest(self, username, otherUsername):
        """
        Permet de supprimer une demande d'ami envoyée

        :param username:      L'emetteur de la demande
        :type username: str
        :param otherUsername: Le récepteur de la demande
        :type otherUsername: str
        :return:
        :rtype: None
        """
        self.db[username]["sentFriendRequests"].remove(otherUsername)

    def addFriend(self, username, friend):
        """
        Permet d'enregistrer un nouvel ami d'un utilisateur

        :param username: L'utilisateur
        :type username: str
        :param friend: Le nouvel ami
        :type friend: str
        :return:
        :rtype: None
        """
        self.db[username]["friends"] += [friend]
        self.db[friend]["friends"] += [username]

    def addPublication(self, username, identifier, publication):
        """
        Permet d'enregistrer une nouvelle publication d'un utilisateur dans
        la base de données

        :param username: L'utilisateur
        :type username: str
        :param identifier: L'identifiant de la publication
        :type identifier: int
        :param publication: La publication
        :type publication: str
        :return:
        :rtype: None
        """
        self.db[username]["publications"] += [{
            "username": username,
            "identifier": identifier,
            "publication": publication,
            "comments": [],
            "likes": 0,
            "shares": 0
        }]

    def getFriends(self, username):
        """
        Permet de récupérer la liste d'amis d'un utilisateur

        :param username: L'utilisateur
        :type username: str
        :return: La liste d'ami
        :rtype: list
        """
        return self.db[username]["friends"]

    def addFeed(self, username, otherUsername, identifier, feed):
        """
        Permet d'enregistrer une nouvelle publication dans le fil d'actualité
        d'un utilisateur

        :param username: L'utilisateur
        :type username: str
        :param otherUsername: L'auteur de la publication
        :type otherUsername: str
        :param identifier: L'identifiant de la publication
        :type identifier: int
        :param feed: La publication
        :type feed: str
        :return:
        :rtype: None
        """
        self.db[username]["activityFeed"] += [{
            "username": otherUsername,
            "identifier": identifier,
            "publication": feed,
            "comments": [],
            "likes": 0,
            "shares": 0
        }]

    def addMessage(self, username, otherUsername, message):
        """
        Permet d'ajouter un nouveau message à une conversation

        :param username: L'émetteur du message
        :type username: str
        :param otherUsername: Le récepteur du message
        :type otherUsername: str
        :param message: Le message
        :type message: str
        :return:
        :rtype: None
        """
        userConversations = self.db[username]["conversations"]
        otherUserConversations = self.db[otherUsername]["conversations"]

        userConversation = self.getConversation(username, otherUsername)

        # Le message est ajouté si une conversation existe déjà
        if userConversation:

            otherUserConversation = self.getConversation(otherUsername, username)
            otherUserConversation["messages"] += [(message, True)]
            userConversation["messages"] += [(message, False)]

        # Une conversation est créée sinon
        else:

            userConversations += [{
                "username": username,
                "addresseeUsername": otherUsername,
                "messages": [(message, False)]
            }]

            otherUserConversations += [{
                "username": otherUsername,
                "addresseeUsername": username,
                "messages": [(message, True)]
            }]

    def getConversation(self, username, otherUsername):
        """
        Permet de récupérer la conversation entre un utilisateur et un autre
        utilisateur

        :param username: L'utilisateur
        :type username: str
        :param otherUsername: L'autre utilisateur
        :type otherUsername: str
        :return: La conversation si elle existe, None sinon
        :rtype: dict
        """
        conversations = self.db[username]["conversations"]
        conversation = None

        found = False
        index = 0
        while not found and index < len(conversations):

            if conversations[index]["addresseeUsername"] == otherUsername:
                found = True
                conversation = conversations[index]

            index += 1

        return conversation

    def addNotification(self, username, notification):
        """
        Permet d'enregistrer une nouvelle notification

        :param username: L'utilisateur concerné
        :type username: str
        :param notification: La notification
        :type notification: str
        :return:
        :rtype: None
        """
        self.db[username]["notifications"] += [notification]
        self.db[username]["notificationsViewed"] = False

    def markNotificationsAsRead(self, username):
        """
        Permet de marquer les notifications d'un utilisateur comme étant lues

        :param username: L'utilisateur
        :type username: str
        :return:
        :rtype: None
        """
        self.db[username]["notificationsViewed"] = True

    def updatePrivacySetting(self, username, setting):
        """
        Permet de mettre à jour le paramètre de privacité d'un utilisateur

        :param username: L'utilisateur
        :type username: str
        :param setting: Le nouveau paramètre de privacité
        :type setting: str
        :return:
        :rtype: None
        """
        self.db[username]["privacySetting"] = setting

    def addCommentToPublication(self, username, comment):
        """
        Permet d'ajouter un commentaire à une publication d'un utilisateur

        :param username: L'utilisateur
        :type username: str
        :param comment: Les données concernant le commentaire
        :type comment: dict
        :return:
        :rtype: None
        """
        publications = self.db[username]["publications"]
        found = False
        publicationIndex = 0
        while (not found) and (publicationIndex < len(publications)):
            publication = publications[publicationIndex]
            if comment["publicationID"] == publication["identifier"]:
                publication["comments"] += [comment]
                found = True
            publicationIndex += 1

    def addCommentToFeed(self, username, comment):
        """
        Permet d'ajouter un commentaire à une publication du fil d'actualité
        d'un utilisateur

        :param username: L'utilisateur
        :type username: str
        :param comment: Les inormations concernant le commentaire
        :type comment: dict
        :return: Vrai si la publication à été trouvée, faux sinon
        :rtype: bool
        """
        feeds = self.db[username]["activityFeed"]
        found = False
        feedIndex = 0
        while (not found) and (feedIndex < len(feeds)):
            feed = feeds[feedIndex]
            if (comment["publicationID"] == feed["identifier"] and
                    comment["publicationUsername"] == feed["username"]):
                feed["comments"] += [comment]
                found = True
            feedIndex += 1
        return found