from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle


class CustomBoxLayout(BoxLayout):

    def __init__(self, colors, **kwargs):
        """
        BoxLayout permettant de changer la couleur de fond

        :param colors: La couleur de fond en rgb
        :type colors: tuple
        :param kwargs: Arguments clé/valeur de la classe parente
        """
        super(CustomBoxLayout, self).__init__(**kwargs)

        # Le canvas permet de changer la couleur de fond
        with self.canvas:
            Color(colors[0], colors[1], colors[2], 1)
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