from kivy.uix.textinput import TextInput

from Widgets.CustomScreen import CustomScreen
from MainWidgets.ProfileTabbedPanel import ProfileTabbedPanel
from Widgets.AboutLabel import AboutLabel

from MainWidgets.PrivacySettingWidget import PrivacySettingWidget
from MainWidgets.UserInteractionWidget import UserInteractionWidget
from MainWidgets.MenuBarWidget import MenuBarWidget
from MainWidgets.PublicationsWidget import PublicationsWidget
from MainWidgets.FriendsWidget import FriendsWidget
from MainWidgets.AboutWidget import AboutWidget
from MainWidgets.ActivityFeedWidget import ActivityFeedWidget
from MainWidgets.InboxWidget import InboxWidget
from MainWidgets.ConversationWidget import ConversationWidget
from MainWidgets.NotificationsWidget import NotificationsWidget
from MainWidgets.SearchResultsWidget import SearchResultsWidget

from Models.Conversation import Conversation
from Models.Publication import Publication
from Models.LoggedInUser import LoggedInUser
from Models.User import User
from Models.Comment import Comment

from Network.Client import Client


class ProfileScreen(CustomScreen):

    def __init__(self, client, dto, **kwargs):
        """
        Widget contenant la page de profil d'un utilisateur

        :param client: Socket permettant de communiquer avec le serveur
        :type client: Client
        :param kwargs: Arguments clé/valeur de la classe parente
        """
        self.register_event_type("on_sign_out")
        super(CustomScreen, self).__init__(**kwargs)

        self.client = client
        self.dto = dto

        self.searchResultsDisplayed = False
        self.InboxViewIsOpen = False
        self.conversationViewIsOpen = False
        self.notificationsViewIsOpen = False
        self.personalInfosAreHidden = False
        self.isUserProfile = True
        self.user = None
        self.otherUser = None

        # ===================== Attributs graphiques ====================== #

        # ------------------------- Barre de menu ------------------------- #
        # Contient les boutons:
        #     - Boite de messagerie
        #     - Retour/Déconnexion
        #     - Notifications
        self.menuBarWidget = MenuBarWidget(
            size_hint=(1, .05),
            pos_hint={'x': 0, 'y': .95}
        )
        self.menuBarWidget.bind(on_home=self.handleHomeButton)
        self.menuBarWidget.bind(on_open_conversations=self.openInboxView)
        self.menuBarWidget.bind(on_open_notifications=self.openNotificationsView)

        # ---------------------- Barre de recherche ----------------------- #
        self.searchBar = TextInput(
            hint_text="Type to search for someone...",
            size_hint=(1, .05),
            pos_hint={'x': 0, 'y': 1 - .05 - .05}
        )
        self.searchBar.bind(text=self.search)

        # ------------------- Résultat d'une recherche -------------------- #
        self.searchResultsWidget = SearchResultsWidget(
            size_hint=(1, .35 - .05 - .05),
            pos_hint={'x': 0, 'y': .65}
        )
        self.searchResultsWidget.bind(
            on_search_result_selected=self.handleSearchResultSelected)

        # ---------------------------- Profil ----------------------------- #
        # Contient les boutons:
        #     - Préférence de privacité
        #     - Envoi de message
        #     - Envoi de demande d'ami
        self.userInteractionWidget = UserInteractionWidget(
            size_hint=(1, .35 - .05 - .05),
            pos_hint={'x': 0, 'y': .65}
        )
        self.userInteractionWidget.bind(
            on_send_friend_request=self.sendFriendRequest)
        self.userInteractionWidget.bind(
            on_open_conversation=self.openConversationView)
        self.userInteractionWidget.bind(
            on_open_privacy_setting=self.openPrivacySettingView)

        # -------------------- Préférences de privacité -------------------- #
        self.privacySettingWidget = PrivacySettingWidget(
            size_hint=(1, .35 - .05 - .05),
            pos_hint={'x': 0, 'y': .65}
        )
        self.privacySettingWidget.bind(
            on_submit_privacy_setting=self.handlePrivacySettingChange)

        # -------------------------- Conversations ------------------------- #
        self.inboxWidget = InboxWidget(
            size_hint=(1, .95)
        )
        self.inboxWidget.bind(on_close=self.closeInboxView)
        self.inboxWidget.bind(on_open_conversation=self.openConversationView)

        # -------------------------- Conversation -------------------------- #
        self.conversationView = ConversationWidget()
        self.conversationView.bind(on_close=self.closeConversationView)
        self.conversationView.bind(on_send_message=self.sendMessage)

        # ------------------------- Notifications -------------------------- #
        self.notificationsWidget = NotificationsWidget(
            size_hint=(1, .95)
        )
        self.notificationsWidget.bind(on_close=self.closeNotificationsView)

        # --------------------- Espace de publication ---------------------- #
        self.publicationsWidget = PublicationsWidget()
        self.publicationsWidget.bind(on_publish=self.sendPublication)

        # ---------------------- Amis/Demandes d'ami ----------------------- #
        self.friendsWidget = FriendsWidget()
        self.friendsWidget.bind(
            on_friend_request_response=self.sendFriendRequestResponse)

        # ------------------- Informations personnelles -------------------- #
        self.aboutWidget = AboutWidget()

        # ------------------------ Fil d'actualité ------------------------- #
        self.activityFeedWidget = ActivityFeedWidget()
        self.activityFeedWidget.bind(on_add_comment=self.sendComment)

        # -----------------  Message de manque de permission --------------- #
        self.infosNotDisplayableLabel = AboutLabel(
            color=(0, 0, 0, 1),
            text="You don't have permissions to view this user infos",
            size_hint=(1, .65),
            pos_hint={'x': 0, 'y': 0}
        )

        # ----------------------- Paneau d'onglets ------------------------- #
        # Les onglets contiennent:
        #     - L'espace de publication
        #     - Les amis/demandes d'ami
        #     - Les informations personnelles
        #     - Le fil d'actualité
        self.tabbedPanel = ProfileTabbedPanel(
            self.publicationsWidget,
            self.friendsWidget,
            self.aboutWidget,
            self.activityFeedWidget,
            size_hint=(1, .65),
            pos_hint={'x': 0, 'y': 0}
        )

        self.add_widget(self.menuBarWidget)
        self.add_widget(self.searchBar)
        self.add_widget(self.userInteractionWidget)
        self.add_widget(self.tabbedPanel)

    def displayUserProfile(self, user=None):
        """
        Affiche la page de profil de l'utilisateur

        :param user: L'utilisateur
        :type user: LoggedInUser
        :return:
        :rtype: None
        """
        self.isUserProfile = True

        if user:
            # Enregistrement de l'utilisateur (lorsqu'il se connecte)
            self.user = user
            username = user.getUsername()
            self.menuBarWidget.updateNotificationButtonIcon(
                self.user.viewedNotifications())
            self.publicationsWidget.setUsername(username)
            self.activityFeedWidget.setUsername(username)
            self.inboxWidget.update(self.user.getConversations())

        # Si l'utilisateur revient du profil d'un autre utilisateur
        if self.otherUser:
            self.otherUser = None
            # transforme le bouton <Retour> en <Déconnexion>
            self.menuBarWidget.toggleHomeButtonIcon()

        # Mise à jour de la page de profil
        self.tabbedPanel.addActivityFeedTab()
        self.updateUserProfile()

    def displayOtherUserProfile(self, otherUser):
        """
        Affiche la page de profil d'un autre utilisateur

        :param otherUser: L'autre utilisateur
        :type otherUser: User
        :return:
        :rtype: None
        """
        otherUsername = otherUser.getUsername()

        # Si l'utilisateur vient de sa propre page de profil
        if not self.otherUser:
            # transforme le bouton <Déconnexion> en <Retour>
            self.menuBarWidget.toggleHomeButtonIcon()
            self.tabbedPanel.removeFeedTab()
            self.isUserProfile = False

        # Enregistrement de l'autre utilisateur
        self.otherUser = otherUser

        # Mise à jour de la page de profil
        isFriend = (otherUsername in self.user.getFriends())
        friendRequestSent = \
            (otherUsername in self.user.getReveivedFriendRequests()) or \
            (otherUsername in self.user.getSentFriendRequests())
        self.updateOtherUserProfile(isFriend, friendRequestSent)

    def updateUserProfile(self):
        """
        Permet de mettre à jour la pag de profil de l'utilisateur

        :return:
        :rtype: None
        """
        username = self.user.getUsername()
        firstName = self.user.getFirstName()
        lastName = self.user.getLastName()

        # Mise à jour
        self.userInteractionWidget.update(
            username, firstName, lastName, True, False, False)
        self.publicationsWidget.update(self.user.getPublications(), True)
        self.friendsWidget.update(
            True, self.user.getFriends(),
            self.user.getReveivedFriendRequests())
        self.aboutWidget.update(firstName, lastName, self.user.getEmail())
        self.activityFeedWidget.update(self.user.getActivityFeed())

        # Ré-affiche les informations personelles si elle ont été cachées
        if self.personalInfosAreHidden:
            self.remove_widget(self.infosNotDisplayableLabel)
            self.add_widget(self.tabbedPanel)
            self.personalInfosAreHidden = False

    def updateOtherUserProfile(self, isFriend, friendRequestSent):
        """
        Permet de mettre à jour la page de profil d'un autre utilisateur
        lorsque l'utilisateur la visite

        :param isFriend: Indique si l'autre utilisateur est un ami
        :type isFriend: bool
        :param friendRequestSent: Indique s'il existe une demande d'ami
        :type friendRequestSent: bool
        :return:
        :rtype: None
        """
        username = self.user.getUsername()
        otherUsername = self.otherUser.getUsername()
        firstName = self.otherUser.getFirstName()
        lastName = self.otherUser.getLastName()
        privacySetting = self.otherUser.getPrivacySetting()

        # Indique si les information personnelles peuvent être affichées
        infosCanBeDisplayed = True
        if (privacySetting == "nobody") or \
                (privacySetting == "friendsOnly" and
                 (username not in self.otherUser.getFriends())):
            infosCanBeDisplayed = False

        # Mise à jour des informations minimales sur l'autre utilisateur
        self.userInteractionWidget.update(
            otherUsername, firstName, lastName,
            False, isFriend, friendRequestSent)

        if infosCanBeDisplayed:
            # Suppression du message <manque de permissions>
            if self.personalInfosAreHidden:
                self.remove_widget(self.infosNotDisplayableLabel)
                self.add_widget(self.tabbedPanel)
                self.personalInfosAreHidden = False

            # Mise à jour des informations personnelles de l'autre utilisateur
            self.publicationsWidget.update(
                self.otherUser.getPublications(), False)
            self.friendsWidget.update(False, self.otherUser.getFriends())
            self.aboutWidget.update(
                firstName, lastName, self.otherUser.getEmail())

        # Ajout du message <manque de permissions>
        elif not self.personalInfosAreHidden:
            self.add_widget(self.infosNotDisplayableLabel)
            self.remove_widget(self.tabbedPanel)
            self.personalInfosAreHidden = True

    def search(self, instance, searchInput):
        """
        Permet d'effectuer la recherche d'un autre utilisateur

        :param instance: Le TextInput représentant la barre de recherche
        :type instance: TextInput
        :param searchInput: La recherche
        :type searchInput: str
        :return:
        :rtype: None
        """
        # Si la barre de recherche est vidée, suppression de l'affichage
        # des résultats
        if (len(searchInput) == 0) and self.searchResultsDisplayed:
            self.remove_widget(self.searchResultsWidget)
            self.searchResultsDisplayed = False

        # Ajout de l'affichage des résultats lorsque la barre de recherche
        # contient au moins un caractère
        elif (len(searchInput) == 1) and (not self.searchResultsDisplayed):
            self.add_widget(self.searchResultsWidget)
            self.searchResultsDisplayed = True

        searchInput = searchInput.split()

        # Si la barre de recherche contient plus de 2 mots, la recherche
        # n'est pas effectuée
        if len(searchInput) > 2:
            self.searchResultsWidget.clear()

        # Envoi des données de recherche au serveur (deux mots maximum)
        elif len(searchInput) == 1 or len(searchInput) == 2:
            data = {
                "request": "search",
                "username": self.user.getUsername(),
                "searchInput": searchInput
            }
            self.client.send(data)

    def displaySearchResults(self, searchResults):
        """
        Affichage des résultats d'une recherche d'un autre utilisateur

        :param searchResults: Les résultats de la recherche
        :type searchResults: list
        :return:
        :rtype: None
        """
        self.searchResultsWidget.clear()
        for searchResult in searchResults:
            self.searchResultsWidget.addSearchResult(
                searchResult["firstName"],
                searchResult["lastName"],
                searchResult["username"]
            )

    def handleSearchResultSelected(self, instance, otherUsername):
        """
        Gère le cas où l'utilisateur à sélectionné un résultat d'une
        recherche d'un autre utilisateur

        :param instance: Le widget contenant les résultats de la recherche
        :type instance: SearchResultsWidget
        :param otherUsername: Le nom d'utilisateur sélectionné
        :type otherUsername: str
        :return:
        :rtype: None
        """
        self.searchBar.text = ""
        self.searchResultsDisplayed = False
        self.remove_widget(self.searchResultsWidget)

        # Envoi de la requête correspondante au serveur
        username = self.user.getUsername()
        if username != otherUsername:
            data = {
                "request": "displayOtherUserProfile",
                "username": self.user.getUsername(),
                "otherUsername": otherUsername
            }
            self.client.send(data)

    def openPrivacySettingView(self, instance):
        """
        Affiche le widget contenant le choix de la préférence de privacité

        :param instance: Le widget UserInteractionView
        :type instance: UserInteractionWidget
        :return:
        :rtype: None
        """
        self.add_widget(self.privacySettingWidget)

    def handlePrivacySettingChange(self, instance, setting):
        """
        Envoie une requête de changement la préférence de privacité au serveur

        :param instance: Le widget PrivacySettingView
        :type instance: PrivacySettingWidget
        :param setting:  La nouvelle préférence de privacité
        :type setting: str
        :return:
        :rtype: None
        """
        # Envoi de la requête si la préférence à été changée
        if setting != self.user.getPrivacySetting():
            self.user.setPrivacySetting(setting)
            data = {
                "request": "changePrivacySetting",
                "username": self.user.getUsername(),
                "setting": setting
            }
            self.client.send(data)

        # Suppression du widget contenant le choix de la préférence
        self.remove_widget(self.privacySettingWidget)

    def openNotificationsView(self, instance):
        """
        Affiche le widget contenant les notifications

        :param instance: La barre de manu
        :type instance: MenuBarWidget
        :return:
        :rtype: None
        """
        if not self.notificationsViewIsOpen:

            # Fermeture de la boite de messagerie si elle est ouverte
            if self.InboxViewIsOpen:
                self.closeInboxView()

            # Mise à jour de l'icone des notifications
            if not self.user.viewedNotifications():
                self.menuBarWidget.toggleNotificationButtonIcon()
                self.user.toggleViewedNotifications()

            self.notificationsViewIsOpen = True
            self.add_widget(self.notificationsWidget)

            # Envoi le fait que l'utilisateur a vu ses notifications au serveur
            data = {
                "request": "notificationsRead",
                "username": self.user.getUsername()
            }
            self.client.send(data)

    def closeNotificationsView(self, instance=None):
        """
        Supprime le widget contenant les notifications

        :param instance: Le widget contenant les notifications
        :type instance: NotificationsWidget
        :return:
        :rtype: None
        """
        self.notificationsViewIsOpen = False
        self.remove_widget(self.notificationsWidget)

    def addNotification(self, notification):
        """
        Permet d'ajouter une notification

        :param notification: La notification à ajouter
        :type notification: str
        :return:
        :rtype: None
        """
        self.notificationsWidget.addNotification(notification)
        self.user.addNotification(notification)

        # Mise à jour de l'icone des notifications
        if (not self.notificationsViewIsOpen) and \
                (self.user.viewedNotifications()):
            self.menuBarWidget.toggleNotificationButtonIcon()
            self.user.toggleViewedNotifications()

    def openInboxView(self, instance):
        """
        Permet d'ouvrir le widget contenant la boite de messagerie

        :param instance: L'instance ayant appelé la méthode
        :type instance: MenuBarWidget
        :return:
        :rtype: None
        """
        if not self.InboxViewIsOpen:
            # Ferme le widget contenant les notifications s'il est ouvert
            if self.notificationsViewIsOpen:
                self.closeNotificationsView()
            self.InboxViewIsOpen = True
            self.add_widget(self.inboxWidget)

    def closeInboxView(self, instance=None):
        """
        Permet de fermer le widget contenant la boite de messagerie

        :param instance: L'instance ayant appelé la méthode
        :type instance: InboxWidget
        :return:
        :rtype: None
        """
        self.InboxViewIsOpen = False
        self.remove_widget(self.inboxWidget)

    def openConversationView(self, instance, username=None):
        """
        Affiche le widget contenant une conversation entre l'utilisateur
        et un correspondant

        :param instance: Le widget ayant appelé la méthode
        :param username: Le nom d'utilisateur du correspondant
        :type username: str
        :return:
        :rtype: None
        """
        # Si la conversation est ouverte depuis la boite de messagerie
        # le nom d'utilisateur du correspondant est passé en paramètre
        otherUsername = username if username else self.otherUser.getUsername()
        conversation = self.user.getConversationByUsername(otherUsername)

        # Création de la conversation si elle n'existe pas encore
        if not conversation:
            conversation = Conversation(
                self.user.getUsername(), otherUsername)
            self.user.addConversation(conversation)
            self.inboxWidget.addConversationButton(otherUsername)

        # Mise à jour de l'affichage ded la conversation
        self.conversationView.update(
            otherUsername, conversation.getMessages())

        self.conversationViewIsOpen = True
        self.add_widget(self.conversationView)

    def closeConversationView(self, instance):
        """
        Ferme le widget contenant la conversation

        :param instance: Le widget contenant la conversation
        :type instance: ConversationWidget
        :return:
        :rtype: None
        """
        self.conversationViewIsOpen = False
        self.remove_widget(self.conversationView)

    def sendFriendRequest(self, instance, otherUsername):
        """
        Permet d'envoyer une demande d'ami à un autre utilisateur

        :param instance: La widget contenant le bouton d'envoi de demande
        :type instance: UserInteractionWidget
        :param otherUsername: Le nom d'utilisateur du récepteur de la demande
        :type otherUsername: str
        :return:
        :rtype: None
        """
        # Mise à jour
        self.user.addSentFriendRequest(otherUsername)
        self.userInteractionWidget.removeSendFriendRequestButton()

        # Envoi de la requête au serveur
        data = {
            "request": "friendRequest",
            "username": self.user.getUsername(),
            "otherUsername": otherUsername
        }
        self.client.send(data)

    def receiveFriendRequest(self, otherUsername):
        """
        Gère le cas où l'utilisateur reçoit une demande d'ami

        :param otherUsername: Le nom d'utilisateur de l'émetteur de la demande
        :type otherUsername: str
        :return:
        :rtype: None
        """
        # Mise à jour
        self.user.addReceivedFriendRequest(otherUsername)
        if self.isUserProfile:
            self.friendsWidget.addFriendRequest(otherUsername)
        elif self.otherUser.getUsername() == otherUsername:
            self.userInteractionWidget.removeSendFriendRequestButton()

        notification = "{:s} sent you a friend request!".format(otherUsername)
        self.addNotification(notification)

    def sendFriendRequestResponse(self, instance, accepted, otherUsername):
        """
        Permet d'envoyer une réponse à une demande d'ami

        :param instance: Le widget contenant les demandes d'ami
        :type instance: FriendsWidget
        :param accepted: Indique si la demande est acceptée
        :type accepted: bool
        :param otherUsername: Le nom d'utilisateur de l'émetteur de la demande
        :type otherUsername: str
        :return:
        :rtype: None
        """
        # Mise à jour
        self.user.removeReceivedFriendRequest(otherUsername)
        if accepted:
            self.user.addFriend(otherUsername)
            self.friendsWidget.addFriend(otherUsername)

        # Envoi de la reqête correspondante au serveur
        data = {
            "request": "friendRequestResponse",
            "username": self.user.getUsername(),
            "otherUsername": otherUsername,
            "accepted": accepted
        }
        self.client.send(data)

    def receiveFriendRequestResponse(self, otherUsername, accepted):
        """
        Gère le cas où l'utilisateur à reçu une réponse à une de ses
        demandes d'ami

        :param otherUsername: Le nom d'utilisateur de l'émetteur de la réponse
        :type otherUsername: str
        :param accepted: Indique si la demande à été acceptée
        :type accepted: bool
        :return:
        :rtype: None
        """
        username = self.user.getUsername()
        # Mise à jour
        self.user.removeSentFriendRequest(otherUsername)

        if accepted:
            notification = "{:s} accepted your friend request!".format(
                otherUsername)

            # Mise à jour spécifique au cas où la demande à été acceptée
            self.user.addFriend(otherUsername)
            if self.isUserProfile:
                self.friendsWidget.addFriend(otherUsername)
            elif self.otherUser.getUsername() == otherUsername:
                self.friendsWidget.addFriend(username)

        else:
            notification = "{:s} refused your friend request!".format(
                otherUsername)

            # Mise à jour spécifique au cas où le demande à été refusée
            if self.isUserProfile or \
                    (self.otherUser.getUsername() == otherUsername):
                self.userInteractionWidget.addSendFriendRequestButton()

        self.addNotification(notification)

    def sendMessage(self, instance, otherUsername, message):
        """
        Permet d'envoyer un message à un autre utilisateur

        :param instance: Le widget contenant la conversation
        :type instance: ConversationWidget
        :param otherUsername: Le nom d'utilisateur du correspondant
        :type otherUsername: str
        :param message: Le message à envoyer
        :type message: str
        :return:
        :rtype: None
        """
        # Ajout du message à la conversation correspondante de l'utilisateur
        conversation = self.user.getConversationByUsername(otherUsername)
        conversation.addSentMessage(message)

        # Envoi de la requếte correspondante au serveur
        data = {
            "request": "sendMessage",
            "username": self.user.getUsername(),
            "otherUsername": otherUsername,
            "message": message
        }
        self.client.send(data)

    def receiveMessage(self, otherUsername, message):
        """
        Gère le cas où l'utilisateur à reçu un message

        :param otherUsername: Le nom d'utilisateur de l'émetteur du message
        :type otherUsername: str
        :param message: Le message
        :type message: str
        :return:
        :rtype: None
        """
        # Ajout du message à la conversation correspondante
        conversation = self.user.getConversationByUsername(otherUsername)
        # Création de la conversation si elle n'existe pas encore
        if not conversation:
            conversation = Conversation(
                self.user.getUsername(), otherUsername)
            self.user.addConversation(conversation)
            self.inboxWidget.addConversationButton(otherUsername)
        conversation.addReceivedMessage(message)

        # Mise à jour
        if self.conversationViewIsOpen and \
                self.conversationView.getAddresseeUsername() == otherUsername:
            self.conversationView.displayReceivedMessage(message)

        notification = "You received a message from {:s}!"\
            .format(otherUsername)
        self.addNotification(notification)

    def sendPublication(self, instance, publication):
        """
        Permet d'émettre une publication

        :param instance: Le widget contenant les publications
        :type instance: PublicationsWidget
        :param publication: La publication
        :type publication: Publication
        :return:
        :rtype: None
        """
        # Mise à jour
        self.user.addPublication(publication)

        # Envoi de la requete correspondante au serveur
        data = {
            "request": "publication",
            "publication": self.dto.serializePublication(publication)
        }
        self.client.send(data)

    def receiveFeed(self, feed):
        """
        Gère le cas ou l'utilisateur reçoit une publication sur son
        fil d'actualité

        :param feed: La publication
        :type feed: Publication
        :return:
        :rtype: None
        """
        otherUsername = feed.getUsername()

        # mise à jour
        self.user.addFeed(feed)
        if self.isUserProfile:
            self.activityFeedWidget.addFeed(feed)

        notification = "{:s} published something!".format(otherUsername)
        self.addNotification(notification)

    def sendComment(self, instance, comment):
        """
        Permet de commenter une publication

        :param instance: Le widget contenant le fil d'actualité
        :type instance: ActivityFeedWidget
        :param comment: Le commentaire
        :type comment: Comment
        :return:
        :rtype: None
        """
        # Mise à jour
        feed = self.user.getFeedByNameAndID(
            comment.getPublicationUsername(),
            comment.getPublicationID()
        )
        feed.addComment(comment)

        # Envoi de la requete correspondante au serveur
        data = {
            "request": "comment",
            "username": self.user.getUsername(),
            "otherUsername": feed.getUsername(),
            "comment": self.dto.serializeComment(comment)
        }
        self.client.send(data)

    def receivePublicationComment(self, comment):
        """
        Gère le cas où l'utilisateur reçoit un commentaire sur un de
        ses publications

        :param comment: Le commentaire
        :type comment: Comment
        :return:
        :rtype: None
        """
        publicationID = comment.getPublicationID()
        # Mise à jour
        self.user.getPublicationByID(publicationID).addComment(comment)
        if self.isUserProfile:
            self.publicationsWidget.addComment(comment)

        notification = "{:s} commented one of your publications!"\
            .format(comment.getUsername())
        self.addNotification(notification)

    def receiveActivityFeedComment(self, comment):
        """
        Gère le cas où l'utilisateur reçoit un commentaire sur une publication
        de son fil d'actualité

        :param comment: Le commentaire
        :type comment: Comment
        :return:
        :rtype: None
        """
        # Mise à jour
        self.user.getFeedByNameAndID(
            comment.getPublicationUsername(),
            comment.getPublicationID()
        ).addComment(comment)
        if self.isUserProfile:
            self.activityFeedWidget.addComment(comment)

    def handleHomeButton(self, instance):
        """
        Gère le cas où l'utilisateur revient sur son profil ou à l'écran
        de bienvenue de l'application (déclenche l'événement <on_sign_out>
        dans ce cas)

        :param instance: Le wigdet contenant le bouton retour/déconnexion
        :type instance: MenuBarWidget
        :return:
        :rtype: None
        """
        # Fermeture de la boite de messagerie et des notifications
        if self.InboxViewIsOpen:
            self.closeInboxView()
        if self.notificationsViewIsOpen:
            self.closeNotificationsView()

        # Retour
        if not self.isUserProfile:
            self.displayUserProfile()
        # Déconnexion
        else:
            self.user = None
            self.publicationsWidget.clear()
            self.dispatch("on_sign_out")

    def on_sign_out(self):
        """
        Événement <on_sign_out>

        :return:
        :rtype: None
        """
        pass