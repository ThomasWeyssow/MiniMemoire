from kivy.uix.label import Label
from Widgets.CustomFloatLayout import CustomFloatLayout
from Widgets.IconButton import IconButton
from Widgets.ExtensibleScrollView import ExtensibleScrollView
from Widgets.TextSizeLabel import TextSizeLabel


class NotificationsWidget(CustomFloatLayout):

    def __init__(self, **kwargs):
        """
        Widgets contenant les notifications

        :param kwargs: Arguments clé/valeur de la classe parente
        """
        self.register_event_type("on_close")
        super(NotificationsWidget, self).__init__((.9, .9, .9), **kwargs)

        # Le titre du widget
        self.title = Label(
            text="Notifications",
            color=(0, 0, 0, 1),
            size_hint=(1, .07),
            pos_hint={'x': 0, 'y': .93}
        )

        # Le bouton de fermeture
        self.closeButton = IconButton(
            "./images/1_navigation_cancel.png",
            size_hint=(.08, .07),
            pos_hint={'x': .9, 'y': .93}
        )
        self.closeButton.bind(on_release=self.close)

        # Le ScrollView contenant les notifications
        self.scrollView = ExtensibleScrollView(
            size_hint=(1, .93),
            pos_hint={'x': 0, 'y': 0}
        )

        self.add_widget(self.title)
        self.add_widget(self.closeButton)
        self.add_widget(self.scrollView)

    def addNotification(self, notification):
        """
        Permet d'ajouter une notification

        :param notification: La nouvelle notification
        :type notification: str
        :return:
        :rtype: None
        """
        notificationLabel = TextSizeLabel(
            (.7, .7, .7),
            text=notification
        )
        self.scrollView.addTextSizeLabel(notificationLabel)

    def update(self, notifications):
        """
        Réinitialisation du widget

        :param notifications: Les nouvelles notifications
        :return:
        :rtype: None
        """
        self.scrollView.clear()
        for notification in notifications:
            self.addNotification(notification)

    def close(self, instance):
        """
        Gère le cas où l'utilisateur ferme le widget: déclenche
        l'événement <on_close>

        :param instance: Le bouton de fermeture
        :type instance: IconButton
        :return:
        :rtype: None
        """
        self.dispatch("on_close")

    def on_close(self):
        """
        Événement <on_close>

        :return:
        :rtype: None
        """
        pass