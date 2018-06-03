from kivy.uix.label import Label
from Widgets.CustomFloatLayout import CustomFloatLayout
from Widgets.IconButton import IconButton


class UserInteractionWidget(CustomFloatLayout):

    def __init__(self, **kwargs):
        """
        Widget contenant le nom d'utilisateur et le nom de l'utilisateur ainsi
        que les boutons:
            - Ouverture du choix de préférence de privacité
            - Envoi d'une demande d'ami
            - Ouverture d'une conversation

        :param kwargs: Arguments clé/valeur de la classe parente
        """
        self.register_event_type("on_open_privacy_setting")
        self.register_event_type("on_send_friend_request")
        self.register_event_type("on_open_conversation")
        super(UserInteractionWidget, self).__init__((0.7, 0.7, 0.7), **kwargs)

        self.currentIsUser = True
        self.currentIsFriend = False
        self.currentHasPendingFriendRequest = False

        # ===================== Attributs graphiques ====================== #

        # -------------------- Label contenant le nom --------------------- #
        self.nameLabel = Label(
            size_hint=(.6, .12),
            pos_hint={'x': .4, 'y': .3},
            )
        self.nameLabel.bind(size=self.nameLabel.setter('text_size'))

        # ------------- Label contenant le nom d'utilisateur -------------- #
        self.usernameLabel = Label(
            size_hint=(.6, .12),
            pos_hint={'x': .4, 'y': .1},
            )
        self.usernameLabel.bind(size=self.usernameLabel.setter('text_size'))

        # ---- Bouton d'ouverture du choix de préférence de privacité ----- #
        self.privacySettingButton = IconButton(
            "./images/2_action_settings.png",
            pos_hint={'x': .8, 'y': .6},
            size_hint=(.11, .3)
            )
        self.privacySettingButton.bind(on_release=self.handlePrivacySettingButton)

        # --------------- Bouton d'envoi d'une demande d'ami -------------- #
        self.sendFriendRequestButton = IconButton(
            "./images/6_social_add_person.png",
            pos_hint={'x': .4, 'y': .6},
            size_hint=(.11, .3)
        )
        self.sendFriendRequestButton.bind(on_release=self.handleSendFriendRequestButton)

        # ------------- Bouton d'ouverture d'une conversation ------------- #
        self.conversationButton = IconButton(
            "./images/5_content_new_email.png",
            pos_hint={'x': .6, 'y': .6},
            size_hint=(.11, .3)
            )
        self.conversationButton.bind(on_release=self.handleOpenConversationButton)

        self.add_widget(self.privacySettingButton)
        self.add_widget(self.nameLabel)
        self.add_widget(self.usernameLabel)

    def addSendFriendRequestButton(self):
        """
        Permet d'afficher le bouton d'envoi de demande d'ami

        :return:
        :rtype: None
        """
        self.currentHasPendingFriendRequest = False
        self.add_widget(self.sendFriendRequestButton)

    def removeSendFriendRequestButton(self):
        """
        Permet de retirer le bouton d'envoi de demande d'ami

        :return:
        :rtype: None
        """
        self.currentHasPendingFriendRequest = True
        self.remove_widget(self.sendFriendRequestButton)

    def update(self, username, firstName, lastName, isUser, isFriend, friendRequestSent):
        """
        Mise à jour des labels et des boutons. Les boutons n'apparaissent que dans
        certaines situations:
            - Le bouton de choix de préférence de privacité n'apparait que si
              l'utilisateur est sur sa propre page de profil
            - Le bouton d'envoi d'une demande d'ami n'apparait que si les utilisateurs
              ne sont pas amis et qu'il n'existe pas de demande d'ami en cours
            - Le bouton d'ouverture d'une conversation n'apparait que si l'utilisateur
              est sur la page de profil d'un autre utilisateur

        :param username: Le nom d'utilisateur
        :type username: str
        :param firstName: Le prénom de l'utilisateur
        :type firstName: str
        :param lastName: Le nom de l'utilisateur
        :type lastName: str
        :param isUser: Indique si l'utilisateur est sur sa propre page de profil
        :type isUser: bool
        :param isFriend: Indique si l'utilisateur est ami avec l'autre utilisateur
        :type isFriend: bool
        :param friendRequestSent: Indique s'il existe une demande d'ami en cours
        :type friendRequestSent: bool
        :return:
        :rtype: None
        """
        self.nameLabel.text = "{:s} {:s}".format(firstName, lastName)
        self.usernameLabel.text = "@{:s}".format(username)

        # Suppression/ajout des boutons en fonction des situations
        if self.currentIsUser:
            if not isUser:
                self.remove_widget(self.privacySettingButton)
                self.add_widget(self.conversationButton)

                if not isFriend and not friendRequestSent:
                    self.add_widget(self.sendFriendRequestButton)
        else:
            if isUser:
                self.add_widget(self.privacySettingButton)
                self.remove_widget(self.conversationButton)

                if not self.currentIsFriend:
                    self.remove_widget(self.sendFriendRequestButton)
            else:
                if self.currentIsFriend or self.currentHasPendingFriendRequest:
                    if not isFriend and not friendRequestSent:
                        self.add_widget(self.sendFriendRequestButton)
                else:
                    if isFriend or friendRequestSent:
                        self.remove_widget(self.sendFriendRequestButton)

        self.currentIsUser = isUser
        self.currentIsFriend = isFriend
        self.currentHasPendingFriendRequest = friendRequestSent

    def handlePrivacySettingButton(self, instance):
        """
        Déclenche l'événement <on_open_privacy_setting>

        :param instance: Le bouton d'ouverture de choix de préférence de privacité
        :type instance: IconButton
        :return:
        :rtype: None
        """
        self.dispatch("on_open_privacy_setting")

    def handleSendFriendRequestButton(self, instance):
        """
        Déclenche l'événement <on_send_friend_request>

        :param instance: Le bouton d'envoi de demande d'ami
        :type instance: IconButton
        :return:
        :rtype: None
        """
        self.dispatch("on_send_friend_request", self.usernameLabel.text[1:])

    def handleOpenConversationButton(self, instance):
        """
        Déclenche l'événement <on_open_conversation>

        :param instance: Le bouton d'ouverture de conversation
        :type instance: IconButton
        :return:
        :rtype: None
        """
        self.dispatch("on_open_conversation")

    def on_open_privacy_setting(self):
        """
        L'événement <on_open_privacy_setting>

        :return:
        :rtype: None
        """
        pass

    def on_send_friend_request(self, username):
        """
        L'événement <on_send_friend_request>: passe le nom d'utilisateur
        du récepteur de la demande au récepteur de l'événement

        :param username: Le nom d'utilisateur de l'autre utilisateur
        :type username: str
        :return:
        :rtype: None
        """
        pass

    def on_open_conversation(self):
        """
        L'événement <on_open_conversation>

        :return:
        :rtype: None
        """
        pass