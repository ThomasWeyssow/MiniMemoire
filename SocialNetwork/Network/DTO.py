from Models.Comment import Comment
from Models.Conversation import Conversation
from Models.Publication import Publication
from Models.User import User
from Models.LoggedInUser import LoggedInUser


class DTO:

    instance = None

    def __init__(self):
        """
        Classe utilitaire permettant de sérialiser et désérialiser les données
        envoyées et reçues du serveur
        """
        pass

    def __new__(cls, *args, **kwargs):
        """
        Permet de s'assurer qu'il n'existe qu'une instance de cette classe

        :return: L'instance du DTO
        :rtype: DTO
        """
        if not cls.instance:
            cls.instance = super(DTO, cls).__new__(cls, *args, **kwargs)

        return cls.instance

    def serializeComment(self, comment):
        """
        Permet de sérialiser un commentaire

        :param comment: Le commentaire à sérialisé
        :type comment: Comment
        :return: Le commentaire sérialisé
        :rtype: dict
        """
        serializedComment = {
            "username": comment.getUsername(),
            "publicationUsername": comment.getPublicationUsername(),
            "publicationID": comment.getPublicationID(),
            "comment": comment.getComment()
        }
        return serializedComment

    def serializeComments(self, comments):
        """
        Permet de sérialiser une liste de commentaires

        :param comments: La liste de commentaire à sérialiser
        :type comments: list
        :return: La liste de commentaire sérialisée
        :rtype: list
        """
        return [self.serializeComment(comment) for comment in comments]

    def unSerialiseComment(self, serializedComment):
        """
        Permet de désérialiser un commentaire

        :param serializedComment: le commentaire sérialisé
        :type serializedComment: dict
        :return: Le commentaire désérialisé
        :rtype: Comment
        """
        comment = Comment(
            serializedComment["username"],
            serializedComment["comment"],
            serializedComment["publicationUsername"],
            serializedComment["publicationID"],
        )
        return comment

    def unserializeComments(self, serializedComments):
        """
        Permet de désérialiser une liste de commentaires

        :param serializedComments: la liste de commentaires sérialisée
        :type serializedComments: list
        :return: la liste de commentaires désérialisée
        :rtype: list
        """
        comments = []
        for serializedComment in serializedComments:
            comment = self.unSerialiseComment(serializedComment)
            comments += [comment]
        return comments

    def serializeConversation(self, conversation):
        """
        Permet de sérialiser une conversation

        :param conversation: La conversation à sérialiser
        :type conversation: Conversation
        :return: La conversation sérialisée
        :rtype: dict
        """
        serializedConversation = {
            "username": conversation.getUsername(),
            "addresseeUsername": conversation.getAddresseeUsername(),
            "messages": conversation.getMessages()
        }
        return serializedConversation

    def serializeConversations(self, conversations):
        """
        Permet de sérialiser une liste de conversations

        :param conversations: La liste de conversations à sérialiser
        :type conversations: list
        :return: La liste de conversations sérialisée
        :rtype: list
        """
        return [self.serializeConversation(conversation)
                for conversation in conversations]

    def unserializeConversation(self, serializedConversation):
        """
        Permet de désérialiser une conversation

        :param serializedConversation: la conversation sérialisée
        :type serializedConversation: dict
        :return: la conversation désérialisé
        :rtype: Conversation
        """
        conversation = Conversation(
            serializedConversation["username"],
            serializedConversation["addresseeUsername"],
            serializedConversation["messages"]
        )
        return conversation

    def unserializeConversations(self, serializedConversations):
        """
        Permet de désérialiser une liste de conversations

        :param serializedConversations: la liste de conversations sérialisée
        :type serializedConversations: list
        :return: la liste de conversations désérialisée
        :rtype: list
        """
        conversations = []
        for serializedConversation in serializedConversations:
            conversation = self.unserializeConversation(serializedConversation)
            conversations += [conversation]
        return conversations

    def serializePublication(self, publication):
        """
        Permet de sérialiser une publication

        :param publication: La publication à sérialiser
        :type publication: Publication
        :return: La publication sérialisée
        :rtype: dict
        """
        serializedPublication = {
            "username": publication.getUsername(),
            "identifier": publication.getID(),
            "publication": publication.getPublication(),
            "comments": self.serializeComments(publication.getComments()),
            "likes": publication.getLikes(),
            "shares": publication.getShares()
        }
        return serializedPublication

    def serializePublications(self, publications):
        """
        Permet de sérialiser une liste de publications

        :param publications: La liste de publications à sérialiser
        :type publications: list
        :return: La liste de publications sérialisée
        """
        return [self.serializePublication(publication)
                for publication in publications]

    def unserializePublication(self, serializedPublication):
        """
        Permet de désérialiser une publication

        :param serializedPublication: La publication sérialisée
        :type serializedPublication: dict
        :return: La publication désérialisée
        :rtype: Publication
        """
        publication = Publication(
            serializedPublication["username"],
            serializedPublication["identifier"],
            serializedPublication["publication"],
            self.unserializeComments(serializedPublication["comments"]),
            serializedPublication["likes"],
            serializedPublication["shares"]
        )
        return publication

    def unserializePublications(self, serializedPublications):
        """
        Permet de désérialiser une liste de publications

        :param serializedPublications: la liste de publications sérialisée
        :type serializedPublications: list
        :return: la liste de publications désérialisée
        :rtype: list
        """
        publications = []
        for serializedPublication in serializedPublications:
            publication = self.unserializePublication(serializedPublication)
            publications += [publication]
        return publications

    def serializeUser(self, user):
        """
        Permet de sérialiser un utilisateur

        :param user: L'utilisateur à sérialiser
        :type user: User
        :return: L'utilisateur sérialisé
        :rtype: dict
        """
        serializedUser = {
            "username": user.getUsername(),
            "firstName": user.getFirstName(),
            "lastName": user.getLastName(),
            "privacySetting": user.getPrivacySetting(),
            "email": user.getEmail(),
            "publications": self.serializePublications(user.getPublications()),
            "friends": user.getFriends()
        }
        return serializedUser

    def unserializeUser(self, serializedUser):
        """
        Permet de désérialiser un utilisateur

        :param serializedUser: L'utilisateur sérialisé
        :type serializedUser: dict
        :return: L'utilisateur désérialisé
        :rtype: User
        """
        email = None if "email" not in serializedUser else \
            serializedUser["email"]
        publications = None if "publications" not in serializedUser else \
            self.unserializePublications(serializedUser["publications"])
        friends = None if "friends" not in serializedUser else \
            serializedUser["friends"]

        user = User(
            serializedUser["username"],
            serializedUser["firstName"],
            serializedUser["lastName"],
            serializedUser["privacySetting"],
            email,
            publications,
            friends
        )
        return user

    def serializeLoggedInUser(self, user):
        """
        Permet de sérialiser un utilisateur connecté à l'application

        :param user: L'utilisateur à sérialiser
        :type user: LoggedInUser
        :return: L'utilisateur sérialisé
        :rtype: dict
        """
        serializedUser = {
            "username": user.getUsername(),
            "firstName": user.getFirstName(),
            "lastName": user.getLastName(),
            "privacySetting": user.getPrivacySetting(),
            "email": user.getEmail(),
            "publications": self.serializePublications(user.getPublications()),
            "friends": user.getFriends(),
            "receivedFriendRequests": user.getReveivedFriendRequests(),
            "sentFriendRequests": user.getSentFriendRequests(),
            "activityFeed": self.serializePublications(user.getActivityFeed()),
            "conversations": self.serializeConversations(user.getConversations()),
            "notifications": user.getNotifications(),
            "notificationsViewed": user.viewedNotifications()
        }
        return serializedUser

    def unserializeLoggedInUser(self, serializedUser):
        """
        Permet de désérialiser un utilisateur connecté à l'application

        :param serializedUser: L'utilisateur sérialisé
        :type serializedUser: dict
        :return: L'utilisateur désérialisé
        :rtype: LoggedInUser
        """
        user = LoggedInUser(
            serializedUser["username"],
            serializedUser["firstName"],
            serializedUser["lastName"],
            serializedUser["privacySetting"],
            serializedUser["email"],
            self.unserializePublications(serializedUser["publications"]),
            serializedUser["friends"],
            serializedUser["receivedFriendRequests"],
            serializedUser["sentFriendRequests"],
            self.unserializePublications(serializedUser["activityFeed"]),
            self.unserializeConversations(serializedUser["conversations"]),
            serializedUser["notifications"],
            serializedUser["notificationsViewed"]
        )
        return user