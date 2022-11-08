import src
from src.db import models, manager


class RatingPostManager(manager.Manager, metaclass=src.Singleton):
    model = models.RatingPost
    collection_name = 'rating_post_collection'


class RatingCommentManager(manager.Manager, metaclass=src.Singleton):
    model = models.RatingComment
    collection_name = 'rating_comment_collection'


class RatingUserManager(manager.Manager, metaclass=src.Singleton):
    model = models.RatingUser
    collection_name = 'rating_user_collection'

