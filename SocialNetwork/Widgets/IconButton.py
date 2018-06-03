from kivy.uix.button import Button


class IconButton(Button):

    def __init__(self, iconFile, **kwargs):
        """
        Button permettant d'y apposer un icone et de le changer par la suite

        :param iconFile: Le chemin vers le fichier contenant l'icone
        :param kwargs: Arguments clé/valeur de la classe parente
        """
        super(IconButton, self).__init__(**kwargs)
        self.background_color = (1, 1, 1, 1)
        self.background_normal = iconFile
        self.background_down = iconFile
        self.border = (0, 0, 0, 0)

    def setIcon(self, newIcon):
        """
        Permet de changer l'icone du bouton

        :param newIcon: Le chemin vers le fichier contenant le nouvel icone
        :type newIcon: str
        :return:
        :rtype: None
        """
        self.background_normal = newIcon
        self.background_down = newIcon

    def on_press(self):
        """
        Événement se produisant quand le bouton est appuyé: changement de
        la couleur de fond

        :return:
        :rtype: None
        """
        self.background_color = (0, 0, 1, 1)

    def on_release(self):
        """
        Événement se produisant quand le bouton est relâché: changement de
        la couleur de fond

        :return:
        :rtype: None
        """
        self.background_color = (1, 1, 1, 1)