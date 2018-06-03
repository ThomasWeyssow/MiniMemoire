from Models.Comment import Comment


class Publication:

    def __init__(self, username, identifier, publication, comments=None,
                 likes=0, shares=0):
        """
        Classe représentant une publication

        :param username: Le nom d'utilisateur de l'auteur de la publication
        :type username: str
        :param identifier: L'identifiant de la publication
        :type identifier: int
        :param publication: La publication
        :type publication: str
        """
        self.username = username
        self.identifier = identifier
        self.publication = publication
        self.comments = [] if not comments else comments
        self.likes = likes
        self.shares = shares

    def __repr__(self):
        """
        Permet de représenter textuellement une instance de la classe

        :return: La représentation textuelle
        :rtype: str
        """
        commentsRepresentation = ""
        for comment in self.comments:
            commentsRepresentation += comment.__repr__() + '\n'
        representation = "Author: {:s}\n" \
                         "ID: {:d}\n" \
                         "Text: {:s}\n" \
                         "Comments: \n{:s}" \
                         "Likes: {:d}\n" \
                         "Shares: {:d}\n"\
            .format(
                self.username,
                self.identifier,
                self.publication,
                commentsRepresentation,
                self.likes,
                self.shares
            )
        return representation

    def getUsername(self):
        """
        Getter de l'attribut username

        :return: Le nom d'utilisateur de l'auteur de la publication
        :rtype: str
        """
        return self.username

    def getID(self):
        """
        Getter de l'attribut identifier

        :return: L'identifiant de la publication
        :rtype: int
        """
        return self.identifier

    def getPublication(self):
        """
        Getter de l'attribut publication

        :return: La publication
        :rtype: str
        """
        return self.publication

    def getComments(self):
        """
        Getter de l'attribut comments

        :return: Les commentaires de la publication
        :rtype: list
        """
        return self.comments

    def getLikes(self):
        """
        Getter de l'attribut likes

        :return: Le nombre de likes
        :rtype: int
        """
        return self.likes

    def getShares(self):
        """
        Getter de l'attribut shares

        :return: Le nombre de partages
        :rtype: int
        """
        return self.shares

    def setUsername(self, username):
        """
        Setter de l'attribut username

        :param username: Le nouveau nom d'utilisateur de l'auteur
        :type username: str
        :return:
        :rtype: None
        """
        self.username = username

    def setID(self, identifier):
        """
        Setter de l'attribut identifier

        :param identifier: Le nouvel identifiant de la publication
        :type identifier: int
        :return:
        :rtype: None
        """
        self.identifier = identifier

    def setPublication(self, publication):
        """
        Setter de l'attribut publication

        :param publication: La nouvelle publication
        :type publication: str
        :return:
        :rtype: None
        """
        self.publication = publication

    def setComments(self, comments):
        """
        Setter de l'attribut comments

        :param comments: Les nouveaux commentaires de la publication
        :type comments: list
        :return:
        :rtype: None
        """
        self.comments = comments

    def setLikes(self, likes):
        """
        Setter de l'attribut likes

        :param likes: Le nouveau nombre de likes
        :type likes: int
        :return:
        :rtype: None
        """
        self.likes = likes

    def setShares(self, shares):
        """
        Setter de l'attribut shares

        :param shares: Le nouveau nombre de partages
        :type shares: int
        :return:
        :rtype: None
        """
        self.shares = shares

    def addComment(self, comment):
        """
        Permet d'ajouter un commentaire à la publication

        :param comment: Le nouveau commentaire
        :type comment: Comment
        :return:
        :rtype: None
        """
        self.comments += [comment]

    def removeComment(self, comment):
        """
        Permet de retirer un commentaire

        :param comment: Le commentaire à retirer
        :type comment: Comment
        :return:
        :rtype: None
        """
        self.comments.remove(comment)

    def addLike(self):
        """
        Permet d'ajouter un like au nombre de like

        :return:
        :rtype: None
        """
        self.likes += 1

    def removeLike(self):
        """
        Permet de retirer un like au nombre de likes

        :return:
        :rtype: None
        """
        self.likes -= 1

    def addShare(self):
        """
        Permet d'ajouter un partage au nombre de partages

        :return:
        :rtype: None
        """
        self.shares += 1

    def removeShare(self):
        """
        Permet de retirer un partage au nombre de partages

        :return:
        :rtype: None
        """
        self.shares -= 1