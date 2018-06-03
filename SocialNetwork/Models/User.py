from Models.Publication import Publication


class User:

    def __init__(self, username, firstName, lastName, privacySetting,
                 email=None, publications=None, friends=None):
        """
        Classe représentant un utilisateur

        :param username: Le nom d'utilisateur
        :type username: str
        :param firstName: Le prénom de l'utilisateur
        :type firstName: str
        :param lastName: Le nom de l'utilisateur
        :type lastName: str
        :param privacySetting: La préférence de privacité de l'utilisateur
        :type privacySetting: str
        """
        self.username = username
        self.firstName = firstName
        self.lastName = lastName
        self.privacySetting = privacySetting
        self.email = email
        self.publications = [] if not publications else publications
        self.friends = [] if not friends else friends

    def getUsername(self):
        """
        Getter de l'attribut username

        :return: Le nom d'utilisateur de l'utilisateur
        :rtype: str
        """
        return self.username

    def getFirstName(self):
        """
        Getter de l'attribut firstName

        :return: Le prénom de l'utilisateur
        :rtype: str
        """
        return self.firstName

    def getLastName(self):
        """
        Getter de l'attribut lastName

        :return: Le nom de l'utilisateur
        :rtype: str
        """
        return self.lastName

    def getPrivacySetting(self):
        """
        Getter de l'attribut privacySettings

        :return: La préférence de privacité de l'utilisateur
        :rtype: str
        """
        return self.privacySetting

    def getEmail(self):
        """
        Getter de l'attribut email

        :return: L'e-mail de l'utilisateur
        :rtype: str
        """
        return self.email

    def getPublications(self):
        """
        Getter de l'attribut publications

        :return:  Les publications de l'utilisateur
        :rtype: list
        """
        return self.publications

    def getFriends(self):
        """
        Getter de l'attribut friends

        :return:  Les amis de l'utilisateur
        :rtype: list
        """
        return self.friends

    def setUsername(self, username):
        """
        Setter de l'attribut username

        :param username: Le nouveau nom d'utilisateur
        :type username: str
        :return:
        :rtype: None
        """
        self.username = username

    def setFirstName(self, firstName):
        """
        Setter de l'attribut firstName

        :param firstName: Le nouveau prénom
        :type firstName: str
        :return:
        :rtype: None
        """
        self.firstName = firstName

    def setLastName(self, lastName):
        """
        Setter de l'attribut lastName

        :param lastName: Le nouveau nom
        :type lastName: str
        :return:
        :rtype: None
        """
        self.lastName = lastName

    def setPrivacySetting(self, privacySetting):
        """
        Setter de l'attribut privacySetting

        :param privacySetting: Le nouveau paramètre de privacité
        :type privacySetting: str
        :return:
        :rtype: None
        """
        self.privacySetting = privacySetting

    def setEmail(self, email):
        """
        Setter de l'attribut email

        :param email: Le nouvel e-mail
        :type email: str
        :return:
        :rtype: None
        """
        self.email = email

    def setPublications(self, publications):
        """
        Setter de l'attribut publications

        :param publications: Les nouvelles publications
        :type publications: list
        :return:
        :rtype: None
        """
        self.publications = publications

    def setFriends(self, friends):
        """
        Setter de l'attribut friends

        :param friends: Les nouveaux amis
        :type friends: list
        :return:
        :rtype: None
        """
        self.friends = friends

    def addFriend(self, username):
        """
        Permet d'ajouter un utilisateur à la liste d'amis de l'utilisateur

        :param username: Le nom d'utilisateur de l'ami à ajouter
        :type username: str
        :return:
        :rtype: None
        """
        self.friends += [username]

    def removeFriend(self, username):
        """
        Permet de retirer un utilisateur de la liste d'ami de l'utilisateur

        :param username: Le nom d'utilisateur de l'ami à retirer
        :type username: str
        :return:
        :rtype: None
        """
        self.friends.remove(username)

    def addPublication(self, publication):
        """
        Permet d'ajouter une publication à la liste de publications de
        l'utilisateur

        :param publication: La publication à ajouter
        :type publication: Publication
        :return:
        :rtype: None
        """
        self.publications += [publication]

    def removePublication(self, publication):
        """
        Permet de retirer une publication de la liste de publications de
        l'utilisateur

        :param publication: La publication à retirer
        :type publication: Publication
        :return:
        :rtype: None
        """
        self.publications.remove(publication)

    def getPublicationByID(self, identifier):
        """
        Permet de récupérer une publication sur base son identifiant

        :param identifier: L'identifiant de la publication
        :type identifier: int
        :return: La publication si elle existe, None sinon
        :rtype: Publication
        """
        result = None
        found = False
        index = 0
        while (not found) and (index < len(self.publications)):
            publication = self.publications[index]
            if publication.getID() == identifier:
                result = publication
                found = True
            index += 1
        return result