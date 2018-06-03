from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from Widgets.CustomBoxLayout import CustomBoxLayout
from Widgets.FriendRequestWidget import FriendRequestWidget
from Widgets.TextSizeLabel import TextSizeLabel
from Widgets.FeedWidget import FeedWidget
from Widgets.PublicationWidget import PublicationWidget


class ExtensibleScrollView(CustomBoxLayout):

    def __init__(self, **kwargs):
        """
        ScrollView s'adaptant à la taille de son contenu; permet d'y ajouter:
            - des FriendRequestWidgets
            - des TextSizeLabels
            - des Buttons
            - des FeedWidgets
            - des PublicationWidgets

        :param kwargs: Arguments clé/valeur de la classe parente
        """
        self.register_event_type("on_friend_request_response")
        self.register_event_type("on_open_conversation")
        self.register_event_type("on_open_search_result")
        super(ExtensibleScrollView, self).__init__((.5, .5, .5), **kwargs)

        self.currentIndex = 0

        # La ScrollView
        self.scrollView = ScrollView()

        # Le layout contenu dans la ScrollView
        self.scrollViewLayout = CustomBoxLayout(
            (.5, .5, .5),
            orientation='vertical',
            spacing=10,
            padding=[10, 10],
            size_hint_y=None
        )
        self.scrollViewLayout.bind(
            minimum_height=self.scrollViewLayout.setter('height')
        )
        self.scrollView.add_widget(self.scrollViewLayout)

        self.add_widget(self.scrollView)

    def addTextSizeLabel(self, label, addAtBottom=False):
        """
        Permet d'ajouter un TextSizeLabel

        :param label: Le label à ajouter
        :type label: TextSizeLabel
        :param addAtBottom: Indique s'il faut ajouter le label par le bas
        :type addAtBottom: bool
        :return:
        :rtype: None
        """
        if addAtBottom:
            self.scrollViewLayout.add_widget(label)
        else:
            self.scrollViewLayout.add_widget(label, index=self.currentIndex)
        self.currentIndex += 1

    def addFriendRequestWidget(self, username):
        """
        Permet d'ajouter un FriendRequestWidget

        :param username: Le nom d'utilisateur de l'émetteur de la demande
        :type username: str
        :return:
        :rtype: None
        """
        friendRequestwidget = FriendRequestWidget(username)
        friendRequestwidget.bind(on_choice=self.handleFriendRequestResponse)
        self.scrollViewLayout.add_widget(friendRequestwidget, index=self.currentIndex)
        self.currentIndex += 1

    def addOpenConversationButton(self, otherUsername):
        """
        Permet d'ajouter un bouton permettant d'ouvrir une conversation

        :param otherUsername: Le nom d'utilisateur du correspondant
        :type otherUsername: str
        :return:
        :rtype: None
        """
        openConversationButton = Button(
            text=otherUsername,
            size_hint_y=None
        )
        openConversationButton.bind(on_press=self.handleOpenConversation)
        self.scrollViewLayout.add_widget(openConversationButton)

    def addOpenSearchResultButton(self, firstName, lastName, username):
        """
        Permet d'ajouter un bouton permattant d'ouvrir le profil d'un
        autre utilisateur apparaissant dans les résultat d'une recherche

        :param firstName: Le prénom de l'autre utilisateur
        :type firstName: str
        :param lastName: Le nom de l'autre utilisateur
        :type lastName: str
        :param username: Le nom d'utilisateur de l'autre utilisateur
        :type username: str
        :return:
        :rtype: None
        """
        searchResultButton = Button(
            text="{:s} {:s} @{:s}".format(firstName, lastName, username),
            size_hint_y=None
        )
        searchResultButton.bind(on_release=self.handleSearchResultSelected)
        self.scrollViewLayout.add_widget(searchResultButton)

    def addFeedWidget(self, feedWidget):
        """
        Permet d'ajouter une publication (dans un fil d'actualité)

        :param feedWidget: La publication
        :type feedWidget: FeedWidget
        :return:
        :rtype: None
        """
        self.scrollViewLayout.add_widget(feedWidget, index=self.currentIndex)
        self.currentIndex += 1

    def addPublicationWidget(self, publicationWidget):
        """
        Permet d'ajouter une publication (dans un espace de publication)

        :param publicationWidget: La publication
        :type publicationWidget: PublicationWidget
        :return:
        :rtype: None
        """
        self.scrollViewLayout.add_widget(publicationWidget, index=self.currentIndex)
        self.currentIndex += 1

    def clear(self):
        """
        Permet de réinitialiser la ScrollView

        :return:
        :rtype: None
        """
        self.scrollViewLayout.clear_widgets()
        self.currentIndex = 0

    def handleOpenConversation(self, instance):
        """
        Gère le cas où l'utilisateur ouvre une conversation: déclenche
        lévénement <on_open_conversation>

        :param instance: Le bouton d'ouverture de conversation
        :type instance: Button
        :return:
        :rtype: None
        """
        self.dispatch("on_open_conversation", instance.text)

    def handleFriendRequestResponse(self, instance, accepted, username):
        """
        Gère le cas où l'utilisateur répond à une demande d'ami: déclenche
        l'événement <on_friend_request_response>

        :param instance: Le FriendRequestWidget
        :type instance: FriendRequestWidget
        :param accepted: Indique si la demande est acceptée
        :type accepted: bool
        :param username: Le nom d'utilisateur de l'émetteur de la demande
        :type username: str
        :return:
        :rtype: None
        """
        self.scrollViewLayout.remove_widget(instance)
        self.currentIndex -= 1
        self.dispatch(
            "on_friend_request_response", accepted, username)

    def handleSearchResultSelected(self, instance):
        """
        Gère le cas où l'utilisateur sélectionne un résultat d'une
        recherche d'autres utilisateurs: déclenche l'événement
        <on_search_result_selected>

        :param instance: Le bouton ayant appelé la méthode
        :type instance: Button
        :return:
        :rtype: None
        """
        username = instance.text.split('@')[1]
        self.dispatch("on_open_search_result", username)

    def on_open_conversation(self, username):
        """
        Évenement <on_open_conversation>: passe le nom d'utilisateur
        du correspondant au récepteur

        :param username: Le nom d'utilisateur du correspondant
        :type username: str
        :return:
        :rtype: None
        """
        pass

    def on_friend_request_response(self, accepted, username):
        """
        Évenement <on_friend_request_response>: passe un booléen indiquant
        si l'utilisateur à accepté la demande et le nom d'utilisateur de
        l'émetteur de la demande au récepteur de l'événement

        :param accepted: Indique si la demande est acceptée
        :type accepted: bool
        :param username: Le nom d'utilisateur de l'émetteur de la demande
        :type username: str
        :return:
        :rtype: None
        """
        pass

    def on_open_search_result(self, username):
        """
        Événement <on_search_result_selected>: passe le nom
        d'utilisateur de l'utilisateur sélectionné au récepteur de
        lévénement

        :param username: Le nom d'utilisateur de l'utilisateur sélectionné
        :type username: str
        :return:
        :rtype: None
        """
        pass
