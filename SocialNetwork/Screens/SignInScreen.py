from Network.Client import Client

from Widgets.CustomScreen import CustomScreen

from Widgets.SignInFormWidget import SignInFormWidget


class SignInScreen(CustomScreen):

    def __init__(self, clientSocket, **kwargs):
        """
        Écran contenant le formulaire de connexion à l'application

        :param clientSocket: Le socket permettant de communiquer avec le serveur
        :type clientSocket: Client
        :param kwargs: Arguments clé/valeur de la classe parente
        """
        self.register_event_type("on_sign_up")
        super(SignInScreen, self).__init__(**kwargs)

        self.clientSocket = clientSocket

        self.signInForm = SignInFormWidget(
            size_hint=(.8, .5),
            pos_hint={'x': .1, 'y': .25}
        )
        self.signInForm.bind(on_sign_in=self.handleSignIn)
        self.signInForm.bind(on_sign_up=self.signUp)

        self.add_widget(self.signInForm)

    def handleSignIn(self, instance, username, password):
        """
        Permet de gérer le cas où l'utilisateur clique sur le bouton de connexion:
        envoie le nom d'utilisateur et le mot de passe entrés par l'utilisateur
        au serveur pour vérification

        :param instance: Le formulaire de connexion
        :type instance: SignInFormWidget
        :param username: Le nom d'utilisateur entré par l'utilisateur
        :type username: str
        :param password: Le mot de passe entré par l'utilisateur
        :type password: str
        :return:
        :rtype: None
        """
        data = {
            "request": "signIn",
            "username": username,
            "password": password
        }
        self.clientSocket.send(data)

    def signUp(self, instance):
        """
        Permet de gérer le cas où l'utilisateur clique sur le bouton
        d'enregistrement à l'application: déclenche l'événement <on_sign_up>

        :param instance: Le formulaire de connexion
        :type instance: SignInFormWidget
        :return:
        :rtype: None
        """
        self.dispatch("on_sign_up")

    def on_sign_up(self):
        """
        L'événement <on_sign_up>

        :return:
        :rtype: None
        """
        pass