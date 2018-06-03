from kivy.uix.screenmanager import ScreenManager
from kivy.graphics import Color, Rectangle


class CustomScreenManager(ScreenManager):

    def __init__(self, **kwargs):
        """
        ScreenManager avec une couleur de fond personnalisée

        :param kwargs: Arguments clé/valeur de la classe parente
        """
        super(CustomScreenManager, self).__init__(**kwargs)

        # Le canvas permet de changer la couleur de fond
        with self.canvas:
            Color(0.9, 0.9, 0.9, 1)
            self.rect = Rectangle(pos=self.pos, size=self.size)

        # Mise à jour du canvas quand le widget change de taille ou de position
        self.bind(pos=self.updateCanvas)
        self.bind(size=self.updateCanvas)

    def updateCanvas(self, instance, values):
        """
        Mis à jour du canvas

        :param instance: Le layout
        :type instance: CustomBoxLayout
        :param values: Valeurs observables
        :type values: list
        :return:
        :rtype: None
        """
        self.rect.pos = self.pos
        self.rect.size = self.size