from Widgets.CustomFloatLayout import CustomFloatLayout
from Widgets.ExtensibleScrollView import ExtensibleScrollView


class SearchResultsWidget(CustomFloatLayout):

    def __init__(self, **kwargs):
        """
        Widget contenant les résultats d'une recherche et permettant
        à l'utilisateur d'afficher le profil d'un autre utilisateur en
        cliquant sur le résultat correspondant

        :param kwargs: Arguments clé/valeur de la classe parente
        """
        self.register_event_type("on_search_result_selected")
        super(SearchResultsWidget, self).__init__((.5, .5, .5), **kwargs)

        # Le ScrollView contenant les boutons contenant un résultat
        self.scrollView = ExtensibleScrollView(
            size_hint=(1, 1),
            pos_hint={'x': 0, 'y': 0}
        )
        self.scrollView.bind(
            on_open_search_result=self.handleSearchResultSelected)
        self.add_widget(self.scrollView)

    def addSearchResult(self, firstName, lastName, username):
        """
        Permet d'ajouter un résultat d'une recherche

        :param firstName: Le prénom de l'autre utilisateur
        :type firstName: str
        :param lastName: Le nom de l'autre utilisateur
        :type lastName: str
        :param username: le nom d'utilisateur de l'autre utilisateur
        :type username: str
        :return:
        :rtype: None
        """
        self.scrollView.addOpenSearchResultButton(firstName, lastName, username)

    def clear(self):
        """
        Permet de réinitialiser le widget

        :return:
        :rtype: None
        """
        self.scrollView.clear()

    def handleSearchResultSelected(self, instance, username):
        """
        Gère le cas où l'utilisateur clique sur l'un des résultat de
        la recherche: déclenche l'événement <on_search_result_selected>

        :param instance: Le ScrollView
        :type instance: ExtensibleScrollView
        :param username: Le nom d'utilisateur correspondant au résultat
        :type username: str
        :return:
        :rtype: None
        """
        self.dispatch("on_search_result_selected", username)

    def on_search_result_selected(self, username):
        """
        Événement <on_search_result_selected>: passe le nom d'utilisateur
        correspondant au résultat sélectionné au récepteur de l'événement

        :param username: Le nom d'utilisateur correspondant au résultat
        :type username: str
        :return: 
        :rtype: None
        """
        pass