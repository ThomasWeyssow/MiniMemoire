from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from Widgets.AboutLabel import AboutLabel
from Widgets.CustomFloatLayout import CustomFloatLayout


class PrivacySettingWidget(CustomFloatLayout):

    def __init__(self, **kwargs):
        """
        Widget contenant les choix de la préférence de privacité:
        permet à l'utilisateur de changer sa préférence de privacité

        :param kwargs: Arguments clé/valeur de la classe parente
        """
        # TODO Positionner le checkbox sur le paramètre de l'utilisateur courant
        self.register_event_type("on_submit_privacy_setting")
        super(PrivacySettingWidget, self).__init__((.7, .7, .7), **kwargs)

        # Titre du widget
        self.title = AboutLabel(
            color=(0, 0, 0, 1),
            text="Who can view your personal informations?",
            size_hint=(1, .2),
            pos_hint={'x': 0, 'y': .75}
        )

        # Légende du choix <tout le monde>
        self.everybodyLabel = Label(
            color=(0, 0, 0, 1),
            text="Everybody",
            size_hint=(.3, .2),
            pos_hint={'x': .1, 'y': .52},
            halign="left",
            valign="middle",
        )
        self.everybodyLabel.bind(size=self.everybodyLabel.setter('text_size'))

        # CheckBox du choix <tout le monde>
        self.everybodyBox = CheckBox(
            color=(0, 0, 0, 1),
            group="choice",
            active=True,
            allow_no_selection=False,
            size_hint=(.2, .2),
            pos_hint={'x': .4, 'y': .52},
        )

        # Légende du choix <seulement les amis>
        self.friendsOnlyLabel = Label(
            color=(0, 0, 0, 1),
            text="Only friends",
            size_hint=(.3, .2),
            pos_hint={'x': .1, 'y': .28},
            halign="left",
            valign="middle",
        )
        self.friendsOnlyLabel.bind(size=self.friendsOnlyLabel.setter('text_size'))

        # CheckBox du choix <seulement les amis>
        self.friendsOnlyBox = CheckBox(
            color=(0, 0, 0, 1),
            group="choice",
            allow_no_selection=False,
            size_hint=(.2, .2),
            pos_hint={'x': .4, 'y': .28},
        )

        # Légende du choix <personne>
        self.nobodyLabel = Label(
            color=(0, 0, 0, 1),
            text="Nobody",
            size_hint=(.3, .2),
            pos_hint={'x': .1, 'y': .04},
            halign="left",
            valign="middle",
        )
        self.nobodyLabel.bind(size=self.nobodyLabel.setter('text_size'))

        # CheckBox du choix <personne>
        self.nobodyBox = CheckBox(
            color=(0, 0, 0, 1),
            group="choice",
            allow_no_selection=False,
            size_hint=(.2, .2),
            pos_hint={'x': .4, 'y': .04},
        )

        # Button d'envoi du paramètre de privacité choisi
        self.submitButton = Button(
            text="OK",
            size_hint=(.12, .2),
            pos_hint={'x': .82, 'y': .06}
        )
        self.submitButton.bind(on_release=self.handleSubmitChoice)

        self.add_widget(self.everybodyLabel)
        self.add_widget(self.everybodyBox)
        self.add_widget(self.friendsOnlyLabel)
        self.add_widget(self.friendsOnlyBox)
        self.add_widget(self.nobodyLabel)
        self.add_widget(self.nobodyBox)
        self.add_widget(self.title)
        self.add_widget(self.submitButton)

    def handleSubmitChoice(self, instance):
        """
        Gère le cas où l'utilisateur choisi un paramètre de privacité:
        déclenche l'événement <on_submit_privacy_setting>

        :param instance: Le bouton d'envoi du paramètre choisi
        :type instance: Button
        :return:
        :rtype: None
        """
        if self.everybodyBox.active:
            privacySetting = "everybody"
        elif self.friendsOnlyBox.active:
            privacySetting = "friendsOnly"
        else:
            privacySetting = "nobody"
        self.dispatch("on_submit_privacy_setting", privacySetting)

    def on_submit_privacy_setting(self, privacySetting):
        """
        Évenement <on_submit_privacy_setting>: passe le paramètre de
        privacité choisi au récepteur de l'événement

        :param privacySetting: Le paramètre de privacité choisi
        :return:
        :rtype: None
        """
        pass