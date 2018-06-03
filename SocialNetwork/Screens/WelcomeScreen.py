from Widgets.CustomScreen import CustomScreen
from Widgets.CustomPopup import CustomPopup

from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

import re


class WelcomeScreen(CustomScreen):

    def __init__(self, **kwargs):
        """
        Écran de bienvenue contenant le champ de saisie de l'adresse IP du
        serveur à laquelle se connecter

        :param kwargs: Arguments clé/valeur de la classe parente
        """
        self.register_event_type("on_confirm_ip_address")
        super(WelcomeScreen, self).__init__(**kwargs)

        self.label = Label(
            text="Please enter the IP address of the server",
            color=(0, 0, 0, 1),
            size_hint=(.8, .08),
            pos_hint={'x': .1, 'y': .6}
        )

        self.textInput = TextInput(
            multiline=False,
            size_hint=(.8, .08),
            pos_hint={'x': .1, 'y': .5}
        )

        self.confirmButton = Button(
            text="OK",
            size_hint=(.8, .08),
            pos_hint={'x': .1, 'y': .4}
        )
        self.confirmButton.bind(on_release=self.handleSubmitAddress)

        self.popup = CustomPopup(
            "Error",
            "Please enter a valid IP address\n\nEx: 192.168.0.10")

        self.add_widget(self.label)
        self.add_widget(self.textInput)
        self.add_widget(self.confirmButton)

    def handleSubmitAddress(self, instance):
        """
        Permet de gérer la confirmation de l'addresse IP entrée par l'utilisateur:
        déclenceh l'événement <on_confirm_ip_address> si l'addresse IP entrée est
        valide

        :param instance: Le bouton de confirmation
        :type instance: Button
        :return:
        :rtype: None
        """
        if re.match("\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}", self.textInput.text):
            self.dispatch("on_confirm_ip_address", self.textInput.text)
        else:
            self.popup.open()

        self.textInput.text = ""

    def on_confirm_ip_address(self, address):
        """
        L'événement <on_confirm_ip_address>: passe l'addresse IP entrée par
        l'utilisateur au récepteur

        :param address: L'addresse IP entrée par l'utilisateur
        :type: str
        :return:
        :rtype: None
        """
        pass


