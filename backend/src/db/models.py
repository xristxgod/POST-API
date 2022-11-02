import tortoise
from tortoise import models, fields

from src.utils import Password


class PostImage(models.Model):
    id = fields.IntField(pk=True)

    main = fields.BooleanField(default=False)

    image = fields.BinaryField(default=None, null=True)
    active = fields.BooleanField(default=True)

    created = fields.DatetimeField(auto_now_add=True)

    post = fields.ForeignKeyField('models.Post', related_name='images', on_delete=fields.CASCADE)


class User(models.Model):
    id = fields.IntField(pk=True)

    avatar = fields.BinaryField(default=None, null=True)

    username = fields.CharField(max_length=255, unique=True)
    password_hash = fields.CharField(max_length=255, validators=[])

    created = fields.DatetimeField(auto_now_add=True)
    updated = fields.DatetimeField(auto_now=True)

    active = fields.BooleanField(default=True)

    posts: fields.ReverseRelation['Post']
    user_comments: fields.ReverseRelation['Comment']

    @property
    def password(self) -> str:
        return self.password_hash

    @password.setter
    def password(self, new_password: str):
        self.password_hash = Password.hash(new_password)

    def verify_password(self, password: str):
        return Password.valid(password, self.password_hash)

    class PydanticMeta:
        exclude = ['password_hash', 'avatar']


class Post(models.Model):
    id = fields.IntField(pk=True)

    title = fields.CharField(max_length=255)
    text = fields.TextField()

    video_link = fields.CharField(max_length=500, default=None, null=True, validators=[])

    created = fields.DatetimeField(auto_now_add=True)
    updated = fields.DatetimeField(auto_now=True)

    active = fields.BooleanField(default=True)

    user = fields.ForeignKeyField('models.User', related_name='posts', on_delete=fields.CASCADE)

    post_comments: fields.ReverseRelation['Comment']
    images: fields.ReverseRelation['PostImage']

    class PydanticMeta:
        exclude = ['images']


class Comment(models.Model):
    id = fields.IntField(pk=True)

    text = fields.TextField()

    created = fields.DatetimeField(auto_now_add=True)
    updated = fields.DatetimeField(auto_now=True)

    post = fields.ForeignKeyField('models.Post', related_name='post_comments', on_delete=fields.CASCADE)
    user = fields.ForeignKeyField('models.User', related_name='user_comments', null=True, on_delete=fields.SET_NULL)
    sub_comment = fields.ForeignKeyField('models.Comment', null=True, on_delete=fields.SET_NULL)


tortoise.Tortoise.init_models(["src.db.models"], "models")
