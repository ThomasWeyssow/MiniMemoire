from kivy.app import App

from Widgets.CustomPopup import CustomPopup
from Widgets.CustomScreenManager import CustomScreenManager

from Screens.ProfileScreen import ProfileScreen
from Screens.SignInScreen import SignInScreen
from Screens.SignUpScreen import SignUpScreen

from Network.DTO import DTO
from Network.Client import Client

from threading import Thread

from Screens.WelcomeScreen import WelcomeScreen


class SocialNetworkApp(App):

    def __init__(self, **kwargs):
        """
        Classe principale de l'application: gère les différents écrans et les
        données provenant du serveur

        :param kwargs: Arguments clé/valeur de la classe parente
        """

        super(SocialNetworkApp, self).__init__(**kwargs)

        self.client = None

        # Initialisation de l'objet permettant de sérialiser les données
        self.dto = DTO()

        # Initialisation du gestionnaire d'écrans
        self.screenManager = CustomScreenManager()

        self.ipScreen = WelcomeScreen(
            name="Welcome"
        )
        self.ipScreen.bind(on_confirm_ip_address=self.connectToServer)

        self.signInScreen = None
        self.signUpScreen = None
        self.profileScreen = None

        self.screenManager.add_widget(self.ipScreen)

    def build(self):
        """
        Méthode appelée lors du lancement de l'application

        :return: Le widget parent contenant tous les autres widgets
        :rtype: CustomScreenManager
        """
        return self.screenManager

    def on_stop(self):
        """
        Méthode appelée lors de la fermeture de l'application: fermeture du
        socket et terminaison du thread gérant la réception des données
        provenant du serveur

        :return:
        :rtype: None
        """
        if self.client:
            self.client.closeSocket()

    def connectToServer(self, instance, ipAddress):
        """
        Permet de gérer la connexion au serveur: lancement de la boucle de la
        partie client du modèle client-serveur et passage à l'écran de connexion
        à l'application

        :param instance: L'écran de bienvenue
        :type instance: WelcomeScreen
        :param ipAddress: L'addresse IP à laquelle se connecter
        :type ipAddress: str
        :return:
        :rtype: None
        """
        self.client = Client(ipAddress)
        self.client.bind(on_connection_lost=self.handleConnectionLost)
        self.client.bind(on_data_received=self.handleDataReceived)

        if self.client.isConnected():
            thread = Thread(target=self.client.start)
            thread.start()
            self.initializeScreens()
            self.displaySignInScreen()
        else:
            CustomPopup("Error", "Could not connect to the server").open()

    def initializeScreens(self):
        """
        Permet d'initialiser les écrans de l'application

        :return:
        :rtype: None
        """
        self.signInScreen = SignInScreen(
            self.client,
            name="Sign In"
        )
        self.signInScreen.bind(on_sign_up=self.displaySignUpScreen)

        self.signUpScreen = SignUpScreen(
            self.client,
            name="Sign Up"
        )
        self.signUpScreen.bind(on_back=self.displaySignInScreen)

        self.profileScreen = ProfileScreen(
            self.client,
            self.dto,
            name="Profile"
        )
        self.profileScreen.bind(on_sign_out=self.displaySignInScreen)

        self.screenManager.add_widget(self.signInScreen)
        self.screenManager.add_widget(self.signUpScreen)
        self.screenManager.add_widget(self.profileScreen)

    def handleConnectionError(self, instance):
        """
        Gestion d'une erreur de connexion avec le serveur: affichage d'un message
        d'erreur

        :param instance: L'instance ayant appelée la méthode
        :type instance: Client
        :return:
        :rtype: None
        """
        popup = CustomPopup("Error", "Could not connect to the server")
        popup.open()
        popup.bind(on_dismiss=self.stop)

    def handleConnectionLost(self, instance):
        """
        Gestion d'une perte de connexion avec le serveur: affichage d'un message
        d'erreur

        :param instance: L'instance ayant appelée la méthode
        :type instance: Client
        :return:
        :rtype: None
        """
        self.client = None

        popup = CustomPopup("Error", "Connection lost")
        popup.open()
        popup.bind(on_dismiss=self.stop)

    def displaySignUpScreen(self, instance):
        """
        Permet d'afficher l'écran d'enregistrement à l'application

        :param instance: L'instance ayant appelée la méthode
        :return:
        :rtype: None
        """
        self.screenManager.current = "Sign Up"

    def displaySignInScreen(self, instance=None):
        """
        Permet d'afficher l'écran de connexion à l'application (l'écran d'acceuil)

        :param instance: L'instance ayant appelée la méthode
        :return:
        :rtype: None
        """
        self.screenManager.current = "Sign In"

    def handleDataReceived(self, instance, data):
        """
        Permet de gérer la réception de données provenenant du serveur

        :param instance: L'instance ayant appelée la méthode
        :type instance: Client
        :param data: Les données reçues
        :type data: dict
        :return:
        :rtype: None
        """
        request = data["request"]

        if request == "signIn":
            self.handleSignInValidation(data["isValid"], data["userData"])

        elif request == "signUp":
            self.handleSignUpValidation(data["isValid"])

        elif request == "search":
            self.handleSearch(data["results"])

        elif request == "displayOtherUserProfile":
            self.handleOtherUserProfileDisplay(data["otherUserInfos"])

        elif request == "friendRequest":
            self.handleFriendRequest(data["username"])

        elif request == "friendRequestResponse":
            self.handleFriendRequestResponse(
                data["otherUsername"], data["accepted"])

        elif request == "feed":
            self.handleFeed(data["feed"])

        elif request == "sendMessage":
            self.handleMessageReceived(data["otherUsername"], data["message"])

        elif request == "comment":
            self.handlePublicationCommentReceived(data["comment"])

        elif request == "feedComment":
            self.handleFeedCommentReceived(data["comment"])

    def handleSignInValidation(self, userInfosAreValid, userData):
        """
        Permet de gérer la réception d'une validation de demande de connexion
        à l'application

        :param userInfosAreValid: Indique si les informations entrées sont valides
        :type userInfosAreValid: bool
        :param userData: Les données concernant l'utilisateur
        :type userData: dict
        :return:
        :rtype: None
        """
        # Si la demande est valide, affichage de l'écran de profil
        if userInfosAreValid:
            user = self.dto.unserializeLoggedInUser(userData)
            self.profileScreen.displayUserProfile(user)
            self.screenManager.current = "Profile"
        # Sinon, affichage d'un message d'erreur
        else:
            CustomPopup("Error", "Username/Password incorrect").open()

    def handleSignUpValidation(self, userInfosAreValid):
        """
        Permet de gérer la réception d'une validation d'une demande d'enregistrement
        à l'application

        :param userInfosAreValid: Indique si les informations entrées sont valides
        :type userInfosAreValid: bool
        :return:
        :rtype: None
        """
        # Affichage d'un message popup de bienvenue ou d'erreur
        if userInfosAreValid:
            popup = CustomPopup("Welcome", "You can now sign in")
        else:
            popup = CustomPopup("Error", "Username/Password already taken")

        # Retour à l'écran de bienvenue lorsque le popup est fermé
        popup.bind(on_dismiss=self.displaySignInScreen)
        popup.open()

    def handleSearch(self, results):
        """
        Permet de gérer la réception des résultats d'une recherche d'un autre
        utilisateur de la part du serveur

        :param results: Les résultats
        :type results: list
        :return:
        :rtype: None
        """
        self.profileScreen.displaySearchResults(results)

    def handleOtherUserProfileDisplay(self, otherUserInfos):
        """
        Permet de gérer la réception des données concernant un autre
        utilisateur provenant du serveur lors d'une demande d'affichage du
        profil de cet utilisateur par l'utilisateur connecté à l'application

        :param otherUserInfos: Les données concernant l'autre utilisateur
        :type otherUserInfos: dict
        :return:
        :rtype: None
        """
        otherUser = self.dto.unserializeUser(otherUserInfos)

        self.profileScreen.displayOtherUserProfile(otherUser)

    def handleFriendRequest(self, otherUsername):
        """
        Gestion de la récption d'une demande d'ami

        :param otherUsername: L'émetteur de la demande
        :type otherUsername: str
        :return:
        :rtype: None
        """
        self.profileScreen.receiveFriendRequest(otherUsername)

    def handleFriendRequestResponse(self, otherUsername, accepted):
        """
        Gestion de la réception d'une réponse à une demande d'ami

        :param otherUsername: L'émetteur de la réponse
        :type otherUsername: str
        :param accepted: Indique si la demande est acceptée ou non
        :type accepted: bool
        :return:
        :rtype: None
        """
        self.profileScreen.receiveFriendRequestResponse(otherUsername, accepted)

    def handleFeed(self, feedData):
        """
        Permet de gérer la réception d'une nouvelle publication dans le
        fil d'actualité de l'utilisateur

        :param feedData: Les données concernant la nouvelle publication
        :type feedData: dict
        :return:
        :rtype: None
        """
        feed = self.dto.unserializePublication(feedData)
        self.profileScreen.receiveFeed(feed)

    def handleMessageReceived(self, otherUsername, message):
        """
        Permet de gérer la réception d'un message envoyé par un autre utilisateur

        :param otherUsername: L'émetteur du message
        :type otherUsername: str
        :param message: Le message
        :type message: str
        :return:
        :rtype: None
        """
        self.profileScreen.receiveMessage(otherUsername, message)

    def handlePublicationCommentReceived(self, commentData):
        """
        Permet de gérer la réception d'un commentaire d'une publication

        :param commentData: Les données concernant le commentaire
        :type commentData: dict
        :return:
        :rtype: None
        """
        comment = self.dto.unSerialiseComment(commentData)
        self.profileScreen.receivePublicationComment(comment)

    def handleFeedCommentReceived(self, commentData):
        """
        Permet de gérer la réception d'un commentaire d'une publication dans
        le fil d'actualité

        :param commentData: Les données concernant le commentaire
        :type commentData: dict
        :return:
        :rtype: None
        """
        comment = self.dto.unSerialiseComment(commentData)
        self.profileScreen.receiveActivityFeedComment(comment)


if __name__ == '__main__':

    app = SocialNetworkApp()
    app.run()
