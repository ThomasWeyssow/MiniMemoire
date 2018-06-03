from Widgets.CustomFloatLayout import CustomFloatLayout

from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button


class SignInFormWidget(CustomFloatLayout):

    def __init__(self, **kwargs):
        """
        Widget contenant le formulaire de connexion à l'application

        :param kwargs: Arguments clé/valeur de la classe parente
        """
        self.register_event_type("on_sign_in")
        self.register_event_type("on_sign_up")
        super(SignInFormWidget, self).__init__((0.7, 0.7, 0.7), **kwargs)

        # ===================== Attributs graphiques ====================== #

        # -------------------------- Les Labels --------------------------- #

        self.usernameLabel = Label(
            text="Username",
            size_hint=(.25, .1),
            pos_hint={'x': .1, 'y': .77}
        )

        self.passwordLabel = Label(
            text="Password",
            size_hint=(.25, .1),
            pos_hint={'x': .1, 'y': .59}
        )

        # ------------------------ Les TextInputs ------------------------- #

        self.usernameTextInput = TextInput(
            multiline=False,
            size_hint=(.55, .1),
            pos_hint={'x': .35, 'y': .77}
        )

        self.passwordTextInput = TextInput(
            multiline=False,
            password=True,
            size_hint=(.55, .1),
            pos_hint={'x': .35, 'y': .59}
        )

        # -------------------------- Les Buttons -------------------------- #

        self.signInButton = Button(
            text="Sign in",
            size_hint=(.8, .15),
            pos_hint={'x': .1, 'y': .31}
        )
        self.signInButton.bind(on_release=self.handleSignIn)

        self.signUpButton = Button(
            text="Sign up",
            size_hint=(.8, .15),
            pos_hint={'x': .1, 'y': .08}
        )
        self.signUpButton.bind(on_release=self.handleSignUp)

        self.add_widget(self.usernameLabel)
        self.add_widget(self.passwordLabel)
        self.add_widget(self.usernameTextInput)
        self.add_widget(self.passwordTextInput)
        self.add_widget(self.signInButton)
        self.add_widget(self.signUpButton)

    def clearInputs(self):
        """
        Permet de vider les TextInputs

        :return:
        :rtype: None
        """
        self.usernameTextInput.text = ""
        self.passwordTextInput.text = ""

    def handleSignIn(self, instance):
        """
        Permet de gérer le cas où l'utilisateur clique sur le boutton
        permettant de se connecter à l'application: déclenche un
        événement <on_sign_in> en lui passant le nom d'utilisateur et le
        mot de passe entrés par l'utilisateur

        :param instance: Le bouton
        :type instance: Button
        :return:
        :rtype: None
        """
        self.dispatch(
            "on_sign_in",
            self.usernameTextInput.text,
            self.passwordTextInput.text
        )
        self.clearInputs()

    def handleSignUp(self, instance):
        """
        Permet de gérer le cas où l'utilisateur clique sur le bouton
        permettant de s'enregistrer ç l'application: déclenche un
        événement <on_sign_up>

        :param instance: Le bouton
        :type instance: Button
        :return:
        :rtype: None
        """
        self.dispatch("on_sign_up")
        self.clearInputs()

    def on_sign_in(self, username, password):
        """
        Événement <on_sign_in>

        :param username: Le nom d'utilisateur entré par l'utilisateur
        :type username: str
        :param password: Le mot de passe entré par lutilisateur
        :type password: str
        :return:
        :rtype: None
        """
        pass

    def on_sign_up(self):
        """
        Événement <on_sign_up>

        :return:
        :rtype: None
        """
        pass