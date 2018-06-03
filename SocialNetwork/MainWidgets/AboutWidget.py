from Widgets.AboutLabel import AboutLabel
from Widgets.CustomFloatLayout import CustomFloatLayout


class AboutWidget(CustomFloatLayout):

    def __init__(self, **kwargs):
        """
        Widget contenant les informations personnelles de l'utilisateur

        :param kwargs: Arguments clé/valeur de la classe parente
        """
        super(AboutWidget, self).__init__((.7, .7, .7), **kwargs)

        # Label contenant la légende du prénom
        self.firstNameLabel = AboutLabel(
            text="First Name:",
            color=(0, 0, .3, 1),
            size_hint=(.28, .33),
            pos_hint={'x': 0, 'y': .67},
            halign="left",
            valign="middle",
            padding=[20, 0]
        )
        self.firstNameLabel.bind(size=self.firstNameLabel.setter('text_size'))

        # Label contenant le prénom
        self.firstNameInfoLabel = AboutLabel(
            color=(0, 0, 0, 1),
            size_hint=(.72, .33),
            pos_hint={'x': .28, 'y': .67},
            halign="left",
            valign="middle",
            padding=[20, 0]
        )
        self.firstNameInfoLabel.bind(size=self.firstNameInfoLabel.setter('text_size'))

        # Label contenant la légende du nom
        self.lastNameLabel = AboutLabel(
            text="Last name:",
            color=(0, 0, .3, 1),
            size_hint=(.28, .33),
            pos_hint={'x': 0, 'y': .34},
            halign="left",
            valign="middle",
            padding=[20, 0]
        )
        self.lastNameLabel.bind(size=self.lastNameLabel.setter('text_size'))

        # Label contenant le nom
        self.lastNameInfoLabel = AboutLabel(
            color=(0, 0, 0, 1),
            size_hint=(.72, .33),
            pos_hint={'x': .28, 'y': .34},
            halign="left",
            valign="middle",
            padding=[20, 0]
        )
        self.lastNameInfoLabel.bind(size=self.lastNameInfoLabel.setter('text_size'))

        # Label contenant la légende de l'e-mail
        self.emailLabel = AboutLabel(
            text="E-mail:",
            color=(0, 0, .3, 1),
            size_hint=(.28, .34),
            pos_hint={'x': 0, 'y': 0},
            halign="left",
            valign="middle",
            padding=[20, 0]
        )
        self.emailLabel.bind(size=self.emailLabel.setter('text_size'))

        # Label contenant l'e-mail
        self.emailInfoLabel = AboutLabel(
            color=(0, 0, 0, 1),
            size_hint=(.72, .34),
            pos_hint={'x': .28, 'y': 0},
            halign="left",
            valign="middle",
            padding=[20, 0]
        )
        self.emailInfoLabel.bind(size=self.emailInfoLabel.setter('text_size'))

        self.add_widget(self.firstNameLabel)
        self.add_widget(self.firstNameInfoLabel)
        self.add_widget(self.lastNameLabel)
        self.add_widget(self.lastNameInfoLabel)
        self.add_widget(self.emailLabel)
        self.add_widget(self.emailInfoLabel)

    def update(self, firstName, lastName, email):
        """
        Permet de réinitialiser le contenu du widget

        :param firstName: Le nouveau prénom
        :type firstName: str
        :param lastName: Le nouveau nom
        :type lastName: str
        :param email: Le nouvel e-mail
        :type email: str
        :return:
        :rtype: None
        """
        self.firstNameInfoLabel.text = firstName
        self.lastNameInfoLabel.text = lastName
        self.emailInfoLabel.text = email