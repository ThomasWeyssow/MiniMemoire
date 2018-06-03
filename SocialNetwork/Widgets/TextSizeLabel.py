from kivy.uix.label import Label
from kivy.graphics import Rectangle, Color


class TextSizeLabel(Label):

    def __init__(self, backgroundColor, **kwargs):
        """
        Label qui s'adapte verticalement à la taille du texte et permettant
        d'y apposer une couleur de fond

        :param text: Le texte
        :type text: str
        :param backgroundColor: La couleur de fond en rgb
        :type backgroundColor: tuple
        :param kwargs: Arguments clé/valeur de la classe parente
        """
        super(TextSizeLabel, self).__init__(**kwargs)

        # Attributs graphiques
        self.color = (0, 0, 0, 1)
        self.size_hint_y = None
        self.padding = [10, 5]

        # Forme et couleur du canvas
        with self.canvas.before:
            Color(
                backgroundColor[0],
                backgroundColor[1],
                backgroundColor[2],
                )
            self.rect = Rectangle(size=self.size, pos=self.pos)
        # Mise à jour du canvas quand le widget change de taille ou de position
        self.bind(pos=self.updateCanvas)
        self.bind(size=self.updateCanvas)

        # Mise à jour de la taille du widget en fonction de la taille du texte
        self.bind(width=lambda s, w: s.setter('text_size')(s, (w, None)))
        self.bind(texture_size=self.setter('size'))

    def updateCanvas(self, instance, values):
        """
        Mise à jour du canvas (sinon il n'apparait pas)

        :param instance: Le TextSizeLabel
        :type instance: TextSizeLabel
        :param values: Valeurs observables
        :type values: list
        :return:
        :rtype: None
        """
        self.rect.pos = self.pos
        self.rect.size = self.size