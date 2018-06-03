from kivy.uix.label import Label
from Widgets.CustomFloatLayout import CustomFloatLayout
from Widgets.ExtensibleScrollView import ExtensibleScrollView
from Widgets.TextSizeLabel import TextSizeLabel


class FriendsWidget(CustomFloatLayout):

    def __init__(self, **kwargs):
        """
        Widget contenant les amis et les demande d'ami en cours de
        l'utilisateur

        :param kwargs: Arguments clé/valeur de la classe parente
        """
        self.register_event_type("on_friend_request_response")
        super(FriendsWidget, self).__init__((.9, .9, .9), **kwargs)

        # Titre de la section contenant les demandes d'ami
        self.requestsScrollViewTitle = Label(
            text="Friend requests",
            size_hint=(1, .075),
            pos_hint={'x': 0, 'y': .925},
            color=(0, 0, 0, 1)
        )

        # ScrollView contenant les demandes d'ami
        self.requestsScrollView = ExtensibleScrollView(
            size_hint=(1, .425),
            pos_hint={'x': 0, 'y': .5}
        )
        self.requestsScrollView.bind(
            on_friend_request_response=self.handleFriendRequestResponse
        )

        # Titre de la section contenant les amis
        self.friendsScrollViewTitle = Label(
            text="Friends",
            size_hint=(1, .075),
            pos_hint={'x': 0, 'y': .425},
            color=(0, 0, 0, 1)
        )

        # ScrollView contenant les amis
        self.friendsScrollView = ExtensibleScrollView(
            size_hint=(1, .425),
            pos_hint={'x': 0, 'y': 0}
        )

        self.add_widget(self.requestsScrollView)
        self.add_widget(self.requestsScrollViewTitle)
        self.add_widget(self.friendsScrollView)
        self.add_widget(self.friendsScrollViewTitle)

    def addFriendRequest(self, username):
        """
        Permet d'ajouter une nouvelle demande d'ami

        :param username: Le nom d'utilisateur de l'émetteur de la demande
        :type username: str
        :return:
        :rtype: None
        """
        self.requestsScrollView.addFriendRequestWidget(username)

    def addFriend(self, username):
        """
        Permet d'ajouter un nouvel ami

        :param username: Le nom d'utilisateur du nouvel ami
        :type username: str
        :return:
        :rtype: None
        """
        friendLabel = TextSizeLabel(
            (.7, .7, .7),
            text=username
        )
        self.friendsScrollView.addTextSizeLabel(friendLabel)

    def update(self, isUserProfile, friends, friendRequests=None):
        """
        Réinitialisation du widget: les demandes d'amis ne sont pas
        affichées si l'utilisateur est sur la page de profil d'un
        autre utilisateur

        :param isUserProfile: Indique si l'utilisateur est sur sa page de profil
        :type isUserProfile: bool
        :param friends: Les nouveaux amis a afficher
        :type friends: list
        :param friendRequests: Les nouvelles demandes d'ami à afficher
        :type friendRequests: list
        :return:
        :rtype: None
        """
        self.friendsScrollView.clear()
        self.requestsScrollView.clear()
        for friend in friends:
            self.addFriend(friend)
        # TODO supprimer le scrollview des requêtes quand l'utilisateur n'est pas sur son profil
        if isUserProfile:
            for friendRequest in friendRequests:
                self.addFriendRequest(friendRequest)

    def handleFriendRequestResponse(self, instance, accepted, username):
        """
        Gère le cas où l'utilisateur répond à une demande d'ami en
        cours: déclenche l'événement <on_friend_request_response>

        :param instance: Le ScrollView contenant les demandes d'ami
        :type instance: ExtensibleScrollView
        :param accepted: Indique si la demande est acceptée
        :type accepted: bool
        :param username: Le nom d'utilisateur de l'émetteur de la demande
        :type username: str
        :return:
        :rtype: None
        """
        self.dispatch("on_friend_request_response", accepted, username)

    def on_friend_request_response(self, accepted, username):
        """
        Évenement <on_friend_request_response>: passe le booléen
        indiquant si la demande est acceptée et le nom d'utilisateur
        de l'émetteur de la demande au récepteur de l'événement

        :param accepted: Indique si la demande est acceptée
        :type accepted: bool
        :param username: Le nom d'utilisateur de l'émetteur de la demande
        :type username: str
        :return:
        :rtype: None
        """
        pass