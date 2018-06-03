from Widgets.CustomFloatLayout import CustomFloatLayout
from Widgets.IconButton import IconButton


class MenuBarWidget(CustomFloatLayout):

    def __init__(self, **kwargs):
        """
        Widget contenant la barre de menu de l'application. La barre de
        menu contient les boutons suivants:
            - Boite de messagerie;
            - Retour/Déconnexion;
            - Notifications

        :param kwargs: Arguments clé/valeur de la classe parente
        """
        self.register_event_type("on_home")
        self.register_event_type("on_open_conversations")
        self.register_event_type("on_open_notifications")
        super(MenuBarWidget, self).__init__((0.8, 0.8, 0.8), **kwargs)

        self.currentIsUserProfile = True
        self.notificationsViewed = False

        # ===================== Attributs graphiques ====================== #

        # --------- Bouton d'ouverture de la boite de messagerie ---------- #
        self.conversationsButton = IconButton(
            "./images/5_content_email.png",
            pos_hint={'x': .08, 'y': 0},
            size_hint=(.08, 1)
            )
        self.conversationsButton.bind(on_release=self.handleConversationsButton)

        # ----------------- Bouton de retour/déconnexion ----------------- #
        self.homeButton = IconButton(
            "./images/5_content_undo.png",
            pos_hint={'x': .44, 'y': 0},
            size_hint=(.08, 1)
            )
        self.homeButton.bind(on_release=self.handleHomeButton)

        # ------------- Bouton d'ouverture des notifications ------------- #
        self.notificationButton = IconButton(
            "./images/5_content_event.png",
            pos_hint={'x': .84, 'y': 0},
            size_hint=(.08, 1)
            )
        self.notificationButton.bind(on_release=self.handleNotificationsButton)

        self.add_widget(self.conversationsButton)
        self.add_widget(self.homeButton)
        self.add_widget(self.notificationButton)

    def updateNotificationButtonIcon(self, notificationsViewed):
        """
        Permet de mettre à jour l'icone du bouton d'ouverture des notifications

        :param notificationsViewed: Indique si l'utilisateur a vu les notifications
        :type notificationsViewed: bool
        :return:
        :rtype: None
        """
        if notificationsViewed:
            self.notificationButton.setIcon("./images/5_content_event.png")
        else:
            self.notificationButton.setIcon("./images/5_content_event_triggered.png")
        self.notificationsViewed = notificationsViewed

    def toggleNotificationButtonIcon(self):
        """
        Permet de switcher entre les icones du bouton d'ouverture des notifications

        :return:
        :rtype: None
        """
        if self.notificationsViewed:
            self.notificationButton.setIcon("./images/5_content_event_triggered.png")
        else:
            self.notificationButton.setIcon("./images/5_content_event.png")
        self.notificationsViewed = not self.notificationsViewed

    def toggleHomeButtonIcon(self):
        """
        Permet de switcher entre les icones du bouton de retour/déconnexion

        :return:
        :rtype: None
        """
        if self.currentIsUserProfile:
            self.homeButton.setIcon("./images/13_Home.png")
        else:
            self.homeButton.setIcon("./images/5_content_undo.png")
        self.currentIsUserProfile = not self.currentIsUserProfile

    def handleHomeButton(self, instance):
        """
        Déclenche l'événement <on_home>

        :param instance: Le bouton de retour/déconnexion
        :type instance: IconButton
        :return:
        :rtype: None
        """
        self.dispatch("on_home")

    def handleConversationsButton(self, instance):
        """
        Déclenche l'événement <on_open_conversations>

        :param instance: Le bouton d'ouverture de la boite de messagerie
        :type instance: IconButton
        :return:
        :rtype: None
        """
        self.dispatch("on_open_conversations")

    def handleNotificationsButton(self, instance):
        """
        Déclenche l'événement <on_open_notifications>

        :param instance: Le bouton d'ouverture des notifications
        :type instance: IconButton
        :return:
        :rtype: None
        """
        self.dispatch("on_open_notifications")

    def on_home(self):
        """
        L'événement <on_home>

        :return:
        :rtype: None
        """
        pass

    def on_open_conversations(self):
        """
        L'événement <on_open_conversations>

        :return:
        :rtype: None
        """
        pass

    def on_open_notifications(self):
        """
        L'événement <on_open_notifications>

        :return:
        :rtype: None
        """
        pass