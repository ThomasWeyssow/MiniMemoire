from Models.User import User
from Models.Publication import Publication
from Models.Conversation import Conversation


class LoggedInUser(User):

    def __init__(self, username, firstName, lastName, privacySetting,
                 email=None, publications=None, friends=None,
                 receivedFriendRequests=None, sentFriendRequests=None,
                 activityFeed=None, conversations=None, notifications=None,
                 notificationsViewed=None):
        """
        Classe représantant un utilisateur connecté à l'application

        :param username: Le nom d'utilisateur
        :type username: str
        :param firstName: Le prénom de l'utilisateur
        :type firstName: str
        :param lastName: Le nom de l'utilisateur
        :type lastName: str
        :param privacySetting: La préférence de privacité de l'utilisateur
        :type privacySetting: str
        """
        super(LoggedInUser, self).__init__(
            username, firstName, lastName, privacySetting,
            email, publications, friends)
        self.receivedFriendRequests = [] if not receivedFriendRequests else \
            receivedFriendRequests
        self.sentFriendRequests = [] if not sentFriendRequests else \
            sentFriendRequests
        self.activityFeed = [] if not activityFeed else activityFeed
        self.conversations = [] if not conversations else conversations
        self.notifications = [] if not notifications else notifications
        self.notificationsViewed = True if not notificationsViewed else \
            notificationsViewed

    def getReveivedFriendRequests(self):
        """
        Getter de l'attribut friendRequests

        :return: Les demandes d'amis reçues par l'utilisateur
        :rtype: list
        """
        return self.receivedFriendRequests

    def getSentFriendRequests(self):
        """
        Getter de l'attribut sentFriendRequests

        :return: Les demandes d'amis envoyées par l'utilisateur
        :rtype: list
        """
        return self.sentFriendRequests

    def getActivityFeed(self):
        """
        Getter de l'attribut activityFeed

        :return: Le fil d'actualité de l'utilisateur
        :rtype: list
        """
        return self.activityFeed

    def getConversations(self):
        """
        Getter de l'attribut conversations

        :return: Les conversations de l'utilisateur
        :rtype: list
        """
        return self.conversations

    def getNotifications(self):
        """
        getter de l'attribut notifications

        :return: Les notifications de l'utilisateur
        :rtype: list
        """
        return self.notifications

    def viewedNotifications(self):
        """
        Getter de l'attribut notificationsViewed

        :return: vrai si l'utilisateur à vu ses notifications, faux sinon
        :rtype: bool
        """
        return self.notificationsViewed

    def setReceivedFriendRequests(self, friendRequests):
        """
        Setter de l'attribut friendRequests

        :param friendRequests: La nouvelle liste de demandes d'ami reçues
        :type friendRequests: list
        :return:
        :rtype: None
        """
        self.receivedFriendRequests = friendRequests

    def setSentFriendRequests(self, sentFriendRequests):
        """
        Setter de l'attribut sentFriendRequests

        :param sentFriendRequests: La nouvelle liste de demandes d'ami envoyées
        :type sentFriendRequests: str
        :return:
        :rtype: None
        """
        self.sentFriendRequests = sentFriendRequests

    def setAcivityFeed(self, activityFeed):
        """
        Setter de l'attribut activityFeed

        :param activityFeed: Le nouveau fil d'actualité
        :type activityFeed: list
        :return:
        :rtype: None
        """
        self.activityFeed = activityFeed

    def setConversations(self, conversations):
        """
        Setter de l'attribut conversations

        :param conversations: Les nouvelles conversations
        :type conversations: list
        :return:
        :rtype: None
        """
        self.conversations = conversations

    def setNotifications(self, notifications):
        """
        Setter de l'attribut notifications

        :param notifications: Les nouvelles notiications
        :type notifications: list
        :return:
        :rtype: None
        """
        self.notifications = notifications

    def setNotificationsViewed(self, notificationsViewed):
        """
        Setter de l'attribut notificationsViewed

        :param notificationsViewed: La nouvelle valeur de notificationsViewed
        :type notificationsViewed: bool
        :return:
        :rtype: None
        """
        self.notificationsViewed = notificationsViewed

    def addReceivedFriendRequest(self, username):
        """
        Permet d'ajouter une demande d'ami à la liste de demandes

        :param username: Le nom d'utilisateur de l'émetteur
        :type username: str
        :return:
        :rtype: None
        """
        self.receivedFriendRequests += [username]

    def removeReceivedFriendRequest(self, username):
        """
        Permet de retirer une demande d'ami de la liste de demandes

        :param username: Le nom d'utilisateur de l'émetteur
        :type username: str
        :return:
        :rtype: None
        """
        self.receivedFriendRequests.remove(username)

    def addSentFriendRequest(self, username):
        """
        Permet d'ajouter une demande d'ami envoyée à la liste de demandes

        :param username: Le nom d'utilisateur du récepteur
        :type username: str
        :return:
        :rtype: None
        """
        self.sentFriendRequests += [username]

    def removeSentFriendRequest(self, username):
        """
        Permet de retirer une demande d'ami envoyée de la liste de demandes

        :param username: Le nom d'utilisateur du récepteur
        :type username: str
        :return:
        :rtype: None
        """
        self.sentFriendRequests.remove(username)

    def addFeed(self, feed):
        """
        Permet d'ajouter une publication au fil d'actualité

        :param feed: La nouvelle publication
        :type feed: Publication
        :return:
        :rtype: None
        """
        self.activityFeed += [feed]

    def removeFeed(self, feed):
        """
        Permet de retirer une publication du fil d'actualité

        :param feed: La publication à retirer
        :type feed: Publication
        :return:
        :rtype: None
        """
        self.activityFeed.remove(feed)

    def getFeedByNameAndID(self, username, identifier):
        """
        Permet de récupérer une publication dans le fil d'actualité à partir
        de son identifiant

        :param username: Le nom d'utilisateur de l'auteur de la publication
        :type username: str
        :param identifier: L'identifiant de la publication à récupérer
        :type identifier: int
        :return: La publication si elle existe, None sinon
        :rtype: Publication
        """
        result = None
        found = False
        index = 0
        while (not found) and (index < len(self.activityFeed)):
            feed = self.activityFeed[index]
            if feed.getUsername() == username and feed.getID() == identifier:
                result = feed
                found = True
            index += 1
        return result

    def addConversation(self, conversation):
        """
        Permet d'ajouter une conversation à la liste de conversations

        :param conversation: La nouvelle conversation
        :type conversation: Conversation
        :return:
        :rtype: None
        """
        self.conversations += [conversation]


    def removeConversation(self, conversation):
        """
        Permet de retirer une conversation de la liste de conversations

        :param conversation: La conversation à retirer
        :type conversation: Conversation
        :return:
        :rtype: None
        """
        conversation = self.getConversationByUsername(conversation)
        self.conversations.remove(conversation)

    def getConversationByUsername(self, otherUsername):
        """
        Permet de récupérer une conversation sur base du nom d'utilisateur
        du correspondant

        :param otherUsername: Le nom d'utilisateur du correspondant
        :type otherUsername: str
        :return:
        :rtype: Conversation
        """
        result = None
        found = False
        index = 0
        while (not found) and (index < len(self.conversations)):
            conversation = self.conversations[index]
            if conversation.getAddresseeUsername() == otherUsername:
                result = conversation
                found = True
            index += 1
        return result

    def addNotification(self, notification):
        """
        Permet d'ajouter une notification à la liste de notifications

        :param notification: La nouvelle notification
        :type notification: str
        :return:
        :rtype: None
        """
        self.notifications += [notification]

    def removeNotification(self, notification):
        """
        Permet de retirer une notification de la liste de notification

        :param notification: La notification à retirer
        :type notification: str
        :return:
        :rtype: None
        """
        self.notifications.remove(notification)

    def clearNotifications(self):
        """
        Permet de vider la liste de notifications

        :return:
        :rtype: None
        """
        self.notifications = []

    def toggleViewedNotifications(self):
        """
        Permet d'inverser la valeur de l'attribut notificationsViewed

        :return:
        :rtype: None
        """
        self.notificationsViewed = not self.notificationsViewed