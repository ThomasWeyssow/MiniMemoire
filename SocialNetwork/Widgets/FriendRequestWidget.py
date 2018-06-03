from Widgets.CustomBoxLayout import CustomBoxLayout
from Widgets.IconButton import IconButton
from Widgets.TextSizeLabel import TextSizeLabel


class FriendRequestWidget(CustomBoxLayout):

    def __init__(self, username, **kwargs):
        """
        Widget contenant une demande d'ami ainsi que deux boutons
        permettants de l'accepter ou de la refuser

        :param username: Le nom d'utilisateur de l'émetteur de la demande
        :type username: str
        :param kwargs: Arguments clé/valeur de la classe parente
        """

        self.register_event_type("on_choice")
        super(FriendRequestWidget, self).__init__((.5, .5, .5), **kwargs)

        self.username = username

        # Attributs graphiques
        self.size_hint_y = None
        self.spacing = 10
        self.bind(minimum_height=self.setter('height'))

        # Label contenant le nom d'utilisateur de l'émetteur de la demande
        usernameLabel = TextSizeLabel(
            (.7, .7, .7),
            text=username,
            size_hint_x=.7
        )

        # Bouton permettant d'accepter la demande
        acceptButton = IconButton(
            "./images/1_navigation_accept.png",
            size_hint=(.06, 1)
            )
        acceptButton.bind(on_release=self.handleAccept)

        # Bouton permettant de refuser la demande
        refuseButton = IconButton(
            "./images/1_navigation_cancel.png",
            size_hint=(.06, 1)
            )
        refuseButton.bind(on_release=self.handleRefuse)

        self.add_widget(usernameLabel)
        self.add_widget(acceptButton)
        self.add_widget(refuseButton)

    def handleAccept(self, instance):
        """
        Gère le cas où l'utilisateur accepte la demande: déclenche
        l'événement <on_choice> en lui passant les paramètres
        correspondants

        :param instance: Le bouton d'acceptation
        :type instance: IconButton
        :return:
        :rtype: None
        """
        self.dispatch("on_choice", True, self.username)

    def handleRefuse(self, instance):
        """
        Gère le cas où l'utilisateur refuse la demande: déclenche
        l'événement <on_choice> en lui passant les paramètres
        correspondants

        :param instance: Le bouton de refus
        :type instance: IconButton
        :return:
        :rtype: None
        """
        self.dispatch("on_choice", False, self.username)

    def on_choice(self, requestAccepted, username):
        """
        Événement <on_choice>: passe un booléen indiquant l'état de
        la demande (acceptée ou refusée) et le nom d'utilisateur de
        l'émetteur de la demande au récepteur de l'événement

        :param requestAccepted: Indique si la demande est acceptée
        :type requestAccepted: bool
        :param username: Le nom d'utilisateru de l'émetteur de la demande
        :type username: str
        :return:
        :rtype: None
        """
        pass