from Widgets.CustomFloatLayout import CustomFloatLayout

from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button


class SignUpFormWidget(CustomFloatLayout):

    def __init__(self, **kwargs):
        """
        Widget contenant le formulaire d'enregistrement à l'application

        :param kwargs: Arguments clé/valeur de la classe parente
        """

        self.register_event_type("on_sign_up")
        self.register_event_type("on_back")
        super(SignUpFormWidget, self).__init__((0.7, 0.7, 0.7), **kwargs)

        # ===================== Attributs graphiques ====================== #

        # -------------------------- Les Labels --------------------------- #

        self.usernameLabel = Label(
            text="Username",
            size_hint=(.25, .14),
            pos_hint={'x': .1, 'y': .84}
        )

        self.passwordLabel = Label(
            text="Password",
            size_hint=(.25, .14),
            pos_hint={'x': .1, 'y': .7}
        )

        self.firstNameLabel = Label(
            text="First name",
            size_hint=(.25, .14),
            pos_hint={'x': .1, 'y': .56}
        )

        self.lastNameLabel = Label(
            text="Last name",
            size_hint=(.25, .14),
            pos_hint={'x': .1, 'y': .42}
        )

        self.emailLabel = Label(
            text="E-mail",
            size_hint=(.25, .14),
            pos_hint={'x': .1, 'y': .28}
        )

        # ------------------------ Les TextInputs ------------------------- #

        self.usernameTextInput = TextInput(
            multiline=False,
            size_hint=(.55, .1),
            pos_hint={'x': .35, 'y': .86}
        )

        self.passwordTextInput = TextInput(
            multiline=False,
            password=True,
            size_hint=(.55, .1),
            pos_hint={'x': .35, 'y': .72}
        )

        self.firstNameTextInput = TextInput(
            multiline=False,
            size_hint=(.55, .1),
            pos_hint={'x': .35, 'y': .58}
        )

        self.lastNameTextInput = TextInput(
            multiline=False,
            size_hint=(.55, .1),
            pos_hint={'x': .35, 'y': .44}
        )

        self.emailTextInput = TextInput(
            multiline=False,
            size_hint=(.55, .1),
            pos_hint={'x': .35, 'y': .3}
        )

        # -------------------------- Les Buttons -------------------------- #

        self.signUpButton = Button(
            text="Sign up",
            size_hint=(.8, .1),
            pos_hint={'x': .1, 'y': .16}
        )
        self.signUpButton.bind(on_release=self.handleSignUpButton)

        self.backButton = Button(
            text="Back",
            size_hint=(.8, .1),
            pos_hint={'x': .1, 'y': .04}
        )
        self.backButton.bind(on_release=self.handleBackButton)

        self.add_widget(self.usernameLabel)
        self.add_widget(self.passwordLabel)
        self.add_widget(self.firstNameLabel)
        self.add_widget(self.lastNameLabel)
        self.add_widget(self.emailLabel)
        self.add_widget(self.usernameTextInput)
        self.add_widget(self.passwordTextInput)
        self.add_widget(self.firstNameTextInput)
        self.add_widget(self.lastNameTextInput)
        self.add_widget(self.emailTextInput)
        self.add_widget(self.signUpButton)
        self.add_widget(self.backButton)

    def clearInputs(self):
        """
        Permet de vider les TextInputs

        :return:
        :rtype: None
        """
        self.usernameTextInput.text = ""
        self.passwordTextInput.text = ""
        self.firstNameTextInput.text = ""
        self.lastNameTextInput.text = ""
        self.emailTextInput.text = ""

    def handleSignUpButton(self, instance):
        """
        Permet de gérer le cas où l'utilisateur clique sur le bouton permettant de
        s'enregistrer: déclenche l'événement <on_sign_up> en lui passant les
        informations entrées qpar l'utilisateur

        :param instance: Le bouton
        :type instance: Button
        :return:
        :rtype: None
        """
        self.dispatch(
            "on_sign_up",
            self.usernameTextInput.text,
            self.passwordTextInput.text,
            self.firstNameTextInput.text,
            self.lastNameTextInput.text,
            self.emailTextInput.text
        )
        self.clearInputs()

    def handleBackButton(self, instance):
        """
        Permet de gérer le cas où l'utilisateur clique sur le bouton permettant de
        retourner à l'écran d'acceuil: déclenche l'événement <on_back>

        :param instance: Le bouton
        :type instance: Button
        :return:
        :rtype: None
        """
        self.dispatch("on_back")
        self.clearInputs()

    def on_sign_up(self, username, password, firstName, lastName, email):
        """
        L'événement <on_sign_up>

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
        pass

    def on_back(self):
        """
        L'événement <on_back>

        :return:
        :rtype: None
        """
        pass