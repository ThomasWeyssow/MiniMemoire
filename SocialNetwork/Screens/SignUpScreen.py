from Network.Client import Client

from Widgets.CustomScreen import CustomScreen

from Widgets.SignUpFormWidget import SignUpFormWidget


class SignUpScreen(CustomScreen):

    def __init__(self, clientSocket, **kwargs):
        """
        Écran contenant le formulaire d'enregistrement à l'application

        :param clientSocket: Le socket permettant de communiquer avec le serveur
        :type clientSocket: Client
        :param kwargs: Arguments clé/valeur de la classe parente
        """
        self.register_event_type("on_back")
        super(SignUpScreen, self).__init__(**kwargs)

        self.clientSocket = clientSocket

        self.signUpForm = SignUpFormWidget(
            size_hint=(.8, .5),
            pos_hint={'x': .1, 'y': .25}
        )
        self.signUpForm.bind(on_sign_up=self.handleSignUp)
        self.signUpForm.bind(on_back=self.handleBack)

        self.add_widget(self.signUpForm)

    def handleSignUp(self, instance, username, password, firstName, lastName, email):
        """
        Permet de gérer le cas où l'utilisateur clique sur le bouton
        d'enregistrement à l'application: envoie les informations entrées par
        l'utilisateur pour vérification et stockage

        :param instance: Le formulaire d'enregistrement
        :type instance: SignUpFormWidget
        :param username: Le nom d'utilisateur entré par l'utilisateur
        :type username: str
        :param password: Le mot de passe entré par l'utilisateur
        :type password: str
        :param firstName: Le prénom entré par l'utilisateur
        :type firstName: str
        :param lastName: Le nom entré par l'utilisateur
        :type lastName: str
        :param email: L'e-mail entré par l'utilisateur
        :type email: str
        :return:
        :rtype: None
        """
        data = {
            "request": "signUp",
            "userData": {
                "username": username,
                "password": password,
                "firstName": firstName,
                "lastName": lastName,
                "email": email
            }
        }
        self.clientSocket.send(data)

    def handleBack(self, instance):
        """
        Permet de gérer le cas où l'utilisateur clique sur le bouton permettant de
        retourner à l'écran d'acceuil: déclanche l'événement <on_back>

        :param instance: Le formulaire d'enregistrement
        :type instance: SignUpFormWidget
        :return:
        :rtype: None
        """
        self.dispatch("on_back")

    def on_back(self):
        """
        L'événement <on_back>

        :return:
        :rtype: None
        """
        pass