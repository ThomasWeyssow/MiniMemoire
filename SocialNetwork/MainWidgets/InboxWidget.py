from Widgets.CustomFloatLayout import CustomFloatLayout
from Widgets.IconButton import IconButton
from Widgets.ExtensibleScrollView import ExtensibleScrollView
from kivy.uix.label import Label


class InboxWidget(CustomFloatLayout):

    def __init__(self, **kwargs):
        """
        Widget contenant la boite de messagerie de l'utilisateur:
        contient des boutons permettant d'ouvrir une conversation
        avec un correpondant

        :param kwargs: Arguments clé/valeur de la classe parente
        """
        self.register_event_type("on_open_conversation")
        self.register_event_type("on_close")
        super(InboxWidget, self).__init__((.9, .9, .9), **kwargs)

        # Titre
        self.title = Label(
            text="Messages",
            color=(0, 0, 0, 1),
            size_hint=(1, .07),
            pos_hint={'x': 0, 'y': .93}
        )

        # Bouton de fermeture
        self.closeButton = IconButton(
            "./images/1_navigation_cancel.png",
            size_hint=(.08, .07),
            pos_hint={'x': .9, 'y': .93}
        )
        self.closeButton.bind(on_release=self.handleClose)

        # ScrollView
        self.scrollView = ExtensibleScrollView(
            size_hint=(1, .93),
            pos_hint={'x': 0, 'y': 0}
        )
        self.scrollView.bind(on_open_conversation=self.handleOpenConversation)

        self.add_widget(self.title)
        self.add_widget(self.closeButton)
        self.add_widget(self.scrollView)

    # TODO ne récupérer que les usernames, pas les conversations entières
    def update(self, conversations):
        """
        Mise à jour de la boite de messagerie

        :param conversations: Les nouvelles conversations
        :type conversations: list
        :return:
        :rtype: None
        """
        self.scrollView.clear()
        for conversation in conversations:
            self.addConversationButton(conversation.getAddresseeUsername())

    def addConversationButton(self, username):
        """
        Ajoute un bouton permettant d'ouvrir une nouvelle conversation

        :param username: Le nom d'utilisateur du correspondant
        :type username: str
        :return:
        :rtype: None
        """
        self.scrollView.addOpenConversationButton(username)

    def handleClose(self, instance):
        """
        Gère le cas où l'utilisateur ferme la boite de messagerie:
        déclenche l'événement <on_close>

        :param instance: Le bouton de fermeture
        :type instance: IconButton
        :return:
        :rtype: None
        """
        self.dispatch("on_close")

    def handleOpenConversation(self, instance, username):
        """
        Gère le cas où l'utilisateur ouvre une conversation: déclenche
        l'événement <on_open_conversation>

        :param instance: Le bouton d'ouverture de la conversation
        :type instance: Button
        :param username: Le nom d'utilisateur du correspondant
        :type username: str
        :return:
        :rtype: None
        """
        self.dispatch("on_open_conversation", username)

    def on_close(self):
        """
        L'Événement <on_close>

        :return:
        :rtype: None
        """
        pass

    def on_open_conversation(self, username):
        """
        L'événement <on_open_conversation>: passe le nom d'utilisateur
        du correspondant au récepteur de l'événement

        :param username: Le nom d'utilisateur du correspondant
        :type username: str
        :return:
        :rtype: None
        """
        pass