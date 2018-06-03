from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from MainWidgets.PublicationsWidget import PublicationsWidget
from MainWidgets.FriendsWidget import FriendsWidget
from MainWidgets.AboutWidget import AboutWidget
from MainWidgets.ActivityFeedWidget import ActivityFeedWidget


class ProfileTabbedPanel(TabbedPanel):

    def __init__(self, publicationsView, friendsView, aboutView,
                 activityFeedView, **kwargs):
        """
        Panneau d'onglets contenant (dans chaque onglet):
            - L'espace de publication
            - Les amis/demandes d'ami
            - Les informations personnelles de l'utilisateur
            - Le fil d'actualité

        :param publicationsView: Les publications
        :type publicationsView: PublicationsWidget
        :param friendsView: Les amis
        :type friendsView: FriendsWidget
        :param aboutView: Les information personnelles
        :type aboutView: AboutWidget
        :param activityFeedView: Le fil d'actualité
        :type activityFeedView: ActivityFeedWidget
        :param kwargs: Arguments clé/valeur de la classe parente
        """
        super(ProfileTabbedPanel, self).__init__(**kwargs)

        # La taille des onglets s'adapte à la taille disponible
        self._tab_layout.padding = [0, 0, 0, '-2dp']
        self.bind(size=self.resizeTabs)

        # L'onglet des publications (il faut utiliser l'onglet par défaut)
        self.default_tab_text = "Wall"
        self.default_tab_content = publicationsView

        # L'onglet des amis/demandes d'ami
        self.friendsViewTab = TabbedPanelItem(
            text="Friends",
            content=friendsView
        )

        # L'onglet des informations personnelles
        self.aboutViewTab = TabbedPanelItem(
            text="About",
            content=aboutView
        )

        # L'onglet du fil d'actualité
        self.activityFeedViewTab = TabbedPanelItem(
            text="Feed",
            content=activityFeedView
        )

        self.add_widget(self.friendsViewTab)
        self.add_widget(self.aboutViewTab)

    def resizeTabs(self, instance=None, values=None):
        """
        Permet d'adapter la taille des onglet à la taille disponible
        dans le widget

        :param instance: Le TabbedPanel
        :type instance: TabbedPanel
        :param values: Valeurs observables
        :type values: list
        :return:
        :rtype: None
        """
        self.tab_width = self.width / len(self.tab_list)
        self.tab_height = self.height / 12

    def addActivityFeedTab(self):
        """
        Permet d'ajouter l'onglet du fil d'actualité

        :return:
        :rtype: None
        """
        self.add_widget(self.activityFeedViewTab)
        self.resizeTabs()

    def removeFeedTab(self):
        """
        Permet d'enlever l'onglet du fil d'actualité

        :return:
        :rtype: None
        """
        self.remove_widget(self.activityFeedViewTab)
        self.resizeTabs()