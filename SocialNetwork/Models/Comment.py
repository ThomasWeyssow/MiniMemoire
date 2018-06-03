class Comment:

    def __init__(self, username, comment, publicationUsername, publicationID):
        """
        Classe représentant un commentaire

        :param username: Le nom d'utilisateur de l'auteur du commentaire
        :type username: str
        :param comment: Le commentaire
        :type comment: str
        :param publicationUsername: l'auteur de la publication associée
        :type publicationUsername: str
        :param publicationID: L'identifiant de la publication correspondante
        :type publicationID: int
        """
        self.username = username
        self.comment = comment
        self.publicationUsername = publicationUsername
        self.publicationID = publicationID

    def __repr__(self):
        """
        Permet de représenter textuellement une instance de la classe

        :return: La représentation textuelle
        :rtype: str
        """
        representation = "    Author: {:s}\n" \
                         "    Text: {:s}\n" \
                         "    Publication author: {:s}\n" \
                         "    Publication ID: {:d}"\
            .format(
                self.username,
                self.comment,
                self.publicationUsername,
                self.publicationID
            )
        return representation

    def getUsername(self):
        """
        Getter de l'attribut username

        :return: Le nom d'utilisateur de l'auteur du commentaire
        :rtype: str
        """
        return self.username

    def getComment(self):
        """
        Getter de l'attribut comment

        :return: Le commentaire
        :rtype: str
        """
        return self.comment

    def getPublicationUsername(self):
        """
        Getter de l'attribut publicationUsername

        :return: Le nom d'utilisateur de l'auteur de la publication
        :rtype: str
        """
        return self.publicationUsername

    def getPublicationID(self):
        """
        Getter de l'attribut publicationID

        :return: L'identifiant de la publication correspondante
        :rtype: int
        """
        return self.publicationID

    def setUsername(self, username):
        """
        Setter de l'attribut username

        :param username: Le nouveau nom d'utilisateur de l'auteur
        :type username: str
        :return:
        :rtype: None
        """
        self.username = username

    def setComment(self, comment):
        """
        Setter de l'attribut comment

        :param comment: Le nouveau commentaire
        :type comment: str
        :return:
        :rtype: None
        """
        self.comment = comment

    def setPublicationUsername(self, publicationUsername):
        """
        Setter de l'attribut publicationUsername

        :param publicationUsername: L'auteur de la publication
        :type publicationUsername: str
        :return:
        :rtype: None
        """
        self.publicationUsername = publicationUsername

    def setPublicationID(self, publicationID):
        """
        Setter de l'attribut publicationID

        :param publicationID: Le nouvel identifiant de la publication
        :type publicationID: int
        :return:
        :rtype: None
        """
        self.publicationID = publicationID