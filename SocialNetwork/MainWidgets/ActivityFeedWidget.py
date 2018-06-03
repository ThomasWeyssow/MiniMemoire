from Widgets.ExtensibleScrollView import ExtensibleScrollView
from Widgets.FeedWidget import FeedWidget
from Widgets.CustomFloatLayout import CustomFloatLayout
from Models.Comment import Comment
from Models.Publication import Publication


class ActivityFeedWidget(CustomFloatLayout):

    def __init__(self, **kwargs):
        """
        Widget contenant le fil d'actualité d'un utilisateur et permettant
        à l'utilisateur d'ajouter un commentaire à une publication

        :param kwargs: Arguments clé/valeur de la classe parente
        """
        self.register_event_type("on_add_comment")
        super(ActivityFeedWidget, self).__init__((.9, .9, .9), **kwargs)

        self.username = None
        self.feedWidgets = []

        # ScrollView contenant le fil d'actualité
        self.activityFeedScrollView = ExtensibleScrollView()

        self.add_widget(self.activityFeedScrollView)

    def setUsername(self, username):
        """
        Setter de l'attribut username

        :param username: Le nouveau nom d'utilisateur
        :type username: str
        :return:
        :rtype: None
        """
        self.username = username

    def getFeedWidgetByIDAndUsername(self, identifier, username):
        """
        Permet de récupérer le widget contenant une publication sur
        base de l'identifiant de la publication

        :param identifier: L'identifiant de la publication
        :type identifier: int
        :param username: Le nom d'utilisateur de l'auteur de la publication
        :type username: str
        :return: Le widget contenant la publication
        :rtype: FeedWidget
        """
        feedWidget = None
        found = False
        index = 0
        while not found and index < len(self.feedWidgets):
            feedWidget = self.feedWidgets[index]
            publication = feedWidget.getPublication()
            if publication.getID() == identifier and \
                    publication.getUsername() == username:
                found = True
            index += 1
        return feedWidget

    def addComment(self, comment):
        """
        Permet d'ajouter un commentaire à une publication sur base
        de l'identifiant de la publication et du nom d'utilisateur de l'auteur
        de la publication

        :param comment: Le commentaire à ajouter
        :type comment: Comment
        :return:
        :rtype: None
        """
        self.getFeedWidgetByIDAndUsername(
            comment.getPublicationID(), comment.getPublicationUsername()
        ).addComment(comment, 1)

    def addFeed(self, feed):
        """
        Ajoute une publication au fil d'actualité

        :param feed: La nouvelle publication
        :type feed: Publication
        :return:
        :rtype: None
        """
        feedWidget = FeedWidget(self.username, feed)
        feedWidget.bind(on_add_comment=self.handleNewComment)
        self.feedWidgets += [feedWidget]
        self.activityFeedScrollView.addFeedWidget(feedWidget)

    def update(self, activityFeed):
        """
        Mise à jour du fil d'actualité

        :param activityFeed: Le nouveau fil d'actualité à afficher
        :return:
        :rtype: None
        """
        self.feedWidgets = []
        self.activityFeedScrollView.clear()
        for feed in activityFeed:
            self.addFeed(feed)

    def handleNewComment(self, instance, comment):
        """
        Gère le cas où l'utilisateur entre un commentaire: déclenche
        l'événement <on_add_comment>

        :param instance: Le widget FeedView qui a déclenché l'événement
        :type instance: FeedWidget
        :param comment: Le commentaire entré par l'utilisateur
        :type comment: Comment
        :return:
        :rtype: None
        """
        self.dispatch("on_add_comment", comment)

    def on_add_comment(self, comment):
        """
        L'événement <on_add_comment>: passe le nouveau commentaire au
        récepteur

        :param comment: Le nouveau commentaire
        :type comment: Comment
        :return:
        :rtype: None
        """
        pass