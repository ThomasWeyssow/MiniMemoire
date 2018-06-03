from kivy.uix.label import Label
from kivy.graphics import Color, Line


class AboutLabel(Label):

    def __init__(self, **kwargs):

        """
        Label stylisé comportant une ligne noire au-dessus et
        en-dessous

        :param kwargs: Arguments clé/valeur de la classe parente
        """
        super(AboutLabel, self).__init__(**kwargs)

        # Le canvas affichant les lignes
        with self.canvas:
            Color(0, 0, 0, 1)
            self.bottomLine = Line(
                points=[],
                width=1
            )
            self.topLine = Line(
                points=[],
                width=1
            )
        # Mise à jour du canvas quand le widget change de taille ou de position
        self.bind(size=self.updateCanvas, pos=self.updateCanvas)

    def updateCanvas(self, instance, values):
        """
        Mise à jour du canvas (sinon il n'apparait pas)

        :param instance: Le Label
        :type instance: Label
        :param values: Valeurs observables
        :type values: list
        :return:
        :rtype: None
        """
        # Les points de la ligne du dessous
        self.bottomLine.points = [
            self.x,
            self.y,
            self.width,
            self.y
        ]
        # Les points de la ligne du dessus
        self.topLine.points = [
            self.x,
            self.y + self.height,
            self.x + self.width,
            self.y + self.height
        ]