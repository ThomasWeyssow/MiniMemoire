from kivy.uix.textinput import TextInput
from Widgets.PublicationWidget import PublicationWidget
from Models.Comment import Comment
from Models.Publication import Publication


class FeedWidget(PublicationWidget):

    def __init__(self, username, publication, **kwargs):
        """
        Widget contenant une publication, ses commentaires ainsi qu'un
        TextInput permettant d'y ajouter un commentaire

        :param publication: La publication
        :type publication: Publication
        :param kwargs: Arguments clé/valeur de la classe parente
        """
        self.register_event_type("on_add_comment")
        super(FeedWidget, self).__init__(publication, **kwargs)

        self.username = username
        self.publication = publication

        self.publicationLabel.text = "@{:s}\n{:s}".format(
            publication.getUsername(), publication.getPublication()
        )

        # Le TextInput permettant d'ajouter un commentaire
        self.commentInput = TextInput(
            hint_text="Comment...",
            size_hint_y=None,
            multiline=False,
            height=40,
            size_hint_x=.8,
            pos_hint={'x': .2}
        )
        self.commentInput.bind(on_text_validate=self.handleNewComment)

        self.add_widget(self.commentInput)

    def getPublication(self):
        """
        Getter de l'attribut publication

        :return: La publication contenue dans le widget
        :rtype: Publication
        """
        return self.publication

    def handleNewComment(self, instance):
        """
        Gère le cas où l'utilisateur entre un nouveau commentaire: affiche
        le commentaire et déclenche l'événement <on_add_comment>

        :param instance: Le TextInput
        :type instance: TextInput
        :return:
        :rtype: None
        """
        comment = Comment(
            self.username,
            instance.text,
            self.publication.getUsername(),
            self.publication.getID()
        )
        self.addComment(comment, 1)

        instance.text = ""

        # Déclenchement de l'événement
        self.dispatch("on_add_comment", comment)

    def on_add_comment(self, comment):
        """
        L'événement <on_add_comment>: passe le nouveau commentaire au
        récepteur

        :param comment: Le nouveau commentaire
        :type comment: Comment
        :return:
        :rtype: None
        """
        pass