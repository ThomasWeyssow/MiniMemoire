from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle


class CustomFloatLayout(FloatLayout):

    def __init__(self, colors, **kwargs):
        """
        FloatLayout permettant de changer la couleur de fond

        :param colors: La couleur de fond en rgb
        :type colors: tuple
        :param kwargs: Arguments clé/valeur de la classe parente
        """
        super(CustomFloatLayout, self).__init__(**kwargs)

        # Le canvas permet de changer la couleur de fond
        with self.canvas:
            Color(colors[0], colors[1], colors[2], 1)
            self.rect = Rectangle(pos=self.pos, size=self.size)

        # Mise à jour du canvas quand le widget change de taille ou de position
        self.bind(pos=self.updateCanvas)
        self.bind(size=self.updateCanvas)

    def updateCanvas(self, instance, values):
        """
        Mise à jour du canvas

        :param instance: Le layout
        :type instance: CustomFloatLayout
        :param values: Valeurs observables
        :type values: list
        :return:
        :rtype: None
        """
        self.rect.pos = self.pos
        self.rect.size = self.size