from Widgets.CustomBoxLayout import CustomBoxLayout
from Models.Publication import Publication
from Models.Comment import Comment
from Widgets.TextSizeLabel import TextSizeLabel


class PublicationWidget(CustomBoxLayout):

    def __init__(self, publication, **kwargs):
        """
        Widget contenant une publication ainsi que ses commentaires

        :param publication: La publication
        :type publication: Publication
        :param kwargs: Arguments clé/valeur de la classe parente
        """
        super(PublicationWidget, self).__init__((.5, .5, .5), **kwargs)

        self.publicationID = publication.getID()

        # Attributs graphiques
        self.orientation = 'vertical'
        self.spacing = 10
        self.padding = [10, 10]
        self.size_hint_y = None
        self.bind(minimum_height=self.setter('height'))

        # Le label contenant la publication
        self.publicationLabel = TextSizeLabel(
            (.7, .7, .7),
            text=publication.getPublication(),
        )
        self.add_widget(self.publicationLabel)

        # Ajout des commentaires présents initialement
        for comment in publication.getComments():
            self.addComment(comment)

    def getPublicationID(self):
        """
        Getter de l'attribut publicationID

        :return: L'identifiant de la publication contenue dans le widget
        :rtype: None
        """
        return self.publicationID

    def addComment(self, comment, index=0):
        """
        Permet d'ajouter un nouveau commentaire à la publication

        :param comment: Le nouveau commentaire
        :type comment: Comment
        :param index: L'index du widget
        :type index: int
        :return:
        :rtype: None
        """
        commentLabel = TextSizeLabel(
            (.7, .7, .7),
            text="@{:s}\n{:s}".format(comment.getUsername(), comment.getComment()),
            size_hint_x=.8,
            pos_hint={'x': .2}
        )
        self.add_widget(commentLabel, index)