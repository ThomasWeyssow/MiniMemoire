from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from Widgets.CustomFloatLayout import CustomFloatLayout
from Widgets.IconButton import IconButton
from Widgets.ExtensibleScrollView import ExtensibleScrollView
from Widgets.TextSizeLabel import TextSizeLabel


class ConversationWidget(CustomFloatLayout):

    def __init__(self, **kwargs):
        """
        Widget contenant une conversation entre l'utilisateur et
        un correspondant

        :param kwargs: Arguments clé/valeur de la classe parente
        """
        self.register_event_type("on_send_message")
        self.register_event_type("on_close")
        super(ConversationWidget, self).__init__((.9, .9, .9), **kwargs)

        self.addresseeUsername = None

        # ===================== Attributs graphiques ====================== #

        # ------------ Label contenant le nom du correspondant ------------ #
        self.title = Label(
            color=(0, 0, 0, 1),
            size_hint=(1, .07),
            pos_hint={'x': 0, 'y': .93}
        )

        # ---------------------- Bouton de fermeture ---------------------- #
        self.closeButton = IconButton(
            "./images/1_navigation_cancel.png",
            size_hint=(.08, .07),
            pos_hint={'x': .9, 'y': .93}
        )
        self.closeButton.bind(on_release=self.handleClose)

        # --- TextInput permettant à l'utilisateur d'entrer un message ---- #
        self.textInput = TextInput(
            hint_text="Type your message here...",
            multiline=False,
            size_hint=(1, .07),
            pos_hint={'x': 0, 'y': 0}
        )
        self.textInput.bind(on_text_validate=self.handleSendMessage)

        # -------------- ScrollView contenant les messages ---------------- #
        self.scrollView = ExtensibleScrollView(
            size_hint=(1, .86),
            pos_hint={'x': 0, 'y': .07}
        )

        self.add_widget(self.title)
        self.add_widget(self.closeButton)
        self.add_widget(self.textInput)
        self.add_widget(self.scrollView)

    def getAddresseeUsername(self):
        """
        Getter de l'attribut addresseeUsername

        :return: Le nom d'utilisateur du correspondant
        :rtype: str
        """
        return self.addresseeUsername

    def displaySentMessage(self, message):
        """
        Permet d'afficher un message envoyé par l'utilisateur

        :param message: Le message à afficher
        :type message: str
        :return:
        :rtype: None
        """
        messageLabel = TextSizeLabel(
            (.2, .4, 1),
            text=message,
            size_hint_x=.9,
            pos_hint={'x': .1}
        )
        self.scrollView.addTextSizeLabel(messageLabel, True)

    def displayReceivedMessage(self, message):
        """
        Permet d'afficher un message reçu par l'utilisateur

        :param message: Le message à afficher
        :type message: str
        :return:
        :rtype: None
        """
        messageLabel = TextSizeLabel(
            (.7, .7, .7),
            text=message,
            size_hint_x=.9,
            pos_hint={'x': 0}
        )
        self.scrollView.addTextSizeLabel(messageLabel, True)

    def update(self, username, messages):
        """
        Mise à jour de la conversation

        :param username: Le nouveau nom d'utilisateur du correspondant
        :type username: str
        :param messages: Les nouveaux messages
        :type messages: list
        :return:
        :rtype: None
        """
        # Mise à jour du titre
        self.addresseeUsername = username
        self.title.text = '@' + username

        # Mise à jour de la conversation
        self.scrollView.clear()
        for message in messages:
            if message[1]:
                self.displaySentMessage(message[0])
            else:
                self.displayReceivedMessage(message[0])

    def handleSendMessage(self, instance):
        """
        Gère le cas où l'utilisateur entre un nouveau message:
        déclenche l'événement <on_send_message>

        :param instance: Le TextInput
        :type instance: TextInput
        :return:
        :rtype: None
        """
        message = instance.text
        instance.text = ""
        if message:
            self.displaySentMessage(message)
            self.dispatch(
                "on_send_message", self.addresseeUsername, message)

    def handleClose(self, instance):
        """
        Gère le cas où l'utilisateur ferme la conversation: déclenche
        l'événement <on_close>

        :param instance: Le bouton de fermeture
        :type instance: IconButton
        :return:
        :rtype: None
        """
        self.dispatch("on_close")

    def on_send_message(self, username, message):
        """
        Événement <on_send_message>: passe le nom d'utilisateur du
        correspondant et le message au récepteur de l'événement

        :param username: Le nom d'utilisateur du correspondant
        :type username: str
        :param message: Le message
        :type message: str
        :return:
        :rtype: None
        """
        pass

    def on_close(self):
        """
        Événement <on_close>

        :return:
        :rtype: None
        """
        pass