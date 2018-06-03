from kivy.uix.textinput import TextInput
from Widgets.CustomFloatLayout import CustomFloatLayout
from Widgets.ExtensibleScrollView import ExtensibleScrollView
from Widgets.PublicationWidget import PublicationWidget
from Models.Publication import Publication
from Models.Comment import Comment


class PublicationsWidget(CustomFloatLayout):

    def __init__(self, **kwargs):
        """
        Widget contenant l'espace de publication

        :param kwargs: Les kwargs (utilisés par la classe parente)
        """
        self.register_event_type("on_publish")
        super(PublicationsWidget, self).__init__((.9, .9, .9), **kwargs)

        self.currentIsUserProfile = False
        self.username = None
        self.publicationWidgets = []

        # TextInput permettant à l'utilisateur de publier
        self.textInput = TextInput(
            hint_text="What's on your mind?",
            multiline=False,
            size_hint=(1, .07),
            pos_hint={'x': 0, 'y': .93}
        )
        self.textInput.bind(on_text_validate=self.handleNewPublication)

        # ScrollView contenant les publications
        self.scrollView = ExtensibleScrollView(
            size_hint=(1, .93),
            pos_hint={'x': 0, 'y': 0}
        )

        self.add_widget(self.scrollView)

    def setUsername(self, username):
        """
        Setter de l'attribut username

        :param username: Le nouveau nom d'utilisateur
        :type username: str
        :return:
        :rtype: None
        """
        self.username = username

    def getPublicationWidgetByID(self, identifier):
        """
        Permet de récupérer le widget contenant une publication sur
        base de l'identifiant de la publication

        :param identifier: L'identifiant de la publication
        :type identifier: int
        :return: Le widget contenant la publication
        :rtype: PublicationWidget
        """
        publicationWidget = None
        found = False
        index = 0
        while not found and index < len(self.publicationWidgets):
            publicationWidget = self.publicationWidgets[index]
            if publicationWidget.getPublicationID() == identifier:
                found = True
            index += 1
        return publicationWidget

    def addPublication(self, publication):
        """
        Permet d'ajouter une publication

        :param publication: La publication a ajouter
        :type publication: Publication
        :return:
        :rtype None
        """
        publicationWidget = PublicationWidget(publication)
        self.publicationWidgets += [publicationWidget]
        self.scrollView.addPublicationWidget(publicationWidget)

    def addComment(self, comment):
        """
        Permet d'ajouter un commentaire à une publication sur base
        de l'identifiant de la publication

        :param publicationID: L'identifiant de la publication
        :type publicationID: int
        :param comment: Le commentaire à ajouter
        :type comment: Comment
        :return:
        :rtype: None
        """
        self.getPublicationWidgetByID(comment.getPublicationID())\
            .addComment(comment)

    def handleNewPublication(self, instance):
        """
        Gère le cas où l'utilisateur entre une nouvelle publication:
        affiche la publication et déclenche l'événement <on_publish>

        :param instance: Le TextInput
        :return:
        :rtype: None
        """
        userInput = instance.text
        if userInput:
            # Création de la nouvelle publication
            publication = Publication(
                self.username, len(self.publicationWidgets), userInput)
            self.addPublication(publication)
            instance.text = ""

            # Déclenchement de l'événement
            self.dispatch("on_publish", publication)

    def update(self, publications, isUserProfile):
        """
        Mise à jour de l'espace de publication lorsque l'utilisateur
        consulte le profil d'un autre utilisateur ou lorsqu'il revient
        sur son propre profil

        :param publications: Les nouvelles publications à afficher
        :type publications: list
        :param isUserProfile: Indique s'il s'agit du profil de l'utilisateur
        :type isUserProfile: bool
        :return:
        :rtype: None
        """
        self.publications = publications

        # TODO mettre quelque chose a la place du label quand on l'enleve
        # Suppression du TextInput si l'utilifateur quitte son profil
        if self.currentIsUserProfile:
            self.clear()
        # Ajout du TextInput si l'utilisateur revient sur son profil
        elif isUserProfile:
            self.add_widget(self.textInput)
            self.currentIsUserProfile = True

        # Mise à jour de l'affichage des nouvelles publication
        self.publicationWidgets = []
        self.scrollView.clear()
        for publication in publications:
            self.addPublication(publication)

    def clear(self):
        """
        Réinitialise le widget

        :return:
        :rtype: None
        """
        self.remove_widget(self.textInput)
        self.currentIsUserProfile = False

    def on_publish(self, publication):
        """
        L'événement <on_publish>: passe la nouvelle publication au
        récepteur

        :param publication: La nouvelle publication
        :type publication: Publication
        :return:
        :rtype: None
        """
        pass