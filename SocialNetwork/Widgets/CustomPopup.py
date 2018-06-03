from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button


class CustomPopup(Popup):

    def __init__(self, title, message, **kwargs):
        """
        Popup personnalisé permettant d'y apposer un titre et un message

        :param title: Le titre
        :type title: str
        :param message: Le message
        :type message: str
        :param kwargs: Arguments clé/valeur de la classe parente
        """
        super(CustomPopup, self).__init__(**kwargs)

        self.message = message
        self.title = title
        self.auto_dismiss = False
        self.size_hint = (.75, .5)

        layout = BoxLayout(
            orientation="vertical"
        )

        # Le Label contenant le message
        messageLabel = Label(
            text=self.message
        )

        # Le bouton de fermeture
        button = Button(
            text="Close",
            size_hint=(1, .2)
        )
        button.bind(on_release=self.dismiss)

        layout.add_widget(messageLabel)
        layout.add_widget(button)
        self.add_widget(layout)