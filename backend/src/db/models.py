import tortoise
from tortoise import models, fields

from src.utils import Password


class Image(models.Model):
    id = fields.IntField(pk=True)

    main = fields.BooleanField(default=False)

    image = fields.BinaryField(default=None, null=True)
    active = fields.BooleanField(default=True)

    created = fields.DatetimeField(auto_now_add=True)
    updated = fields.DatetimeField(auto_now=True)

    user = fields.ForeignKeyField(
        'models.User',
        related_name='user_images',
        null=True,
        default=None,
        on_delete=fields.CASCADE
    )
    post = fields.ForeignKeyField(
        'models.Post',
        related_name='post_images',
        null=True,
        default=None,
        on_delete=fields.CASCADE
    )
    comment = fields.ForeignKeyField(
        'models.Comment',
        related_name='comment_images',
        on_delete=fields.CASCADE,
        null=True,
        default=None,
    )

    def __str__(self):
        text = ['Image']
        if self.post is not None:
            text.append(f'Post#{self.post.pk}')
        if self.user is not None:
            text.append(f'User#{self.user.pk}')
        if self.comment is not None:
            text.append(f'Comment#{self.comment.pk}')
        return '::' + '::'.join(text) + '::'

    class Meta:
        ordering = ('main',)

    class PydanticMeta:
        exclude = (
            'image'
        )


class User(models.Model):
    id = fields.IntField(pk=True)

    username = fields.CharField(max_length=255, unique=True)
    password_hash = fields.CharField(max_length=255, validators=[])

    created = fields.DatetimeField(auto_now_add=True)
    updated = fields.DatetimeField(auto_now=True)

    active = fields.BooleanField(default=True)

    posts: fields.ReverseRelation['Post']
    user_comments: fields.ReverseRelation['Comment']
    user_images: fields.ReverseRelation['Image']

    def __str__(self):
        return f'User: {self.username}'

    @property
    def password(self) -> str:
        return self.password_hash

    @password.setter
    def password(self, new_password: str):
        self.password_hash = Password.hash(new_password)

    def verify_password(self, password: str):
        return Password.valid(password, self.password_hash)

    class PydanticMeta:
        exclude = (
            'password_hash',
        )


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
    post_images: fields.ReverseRelation['Image']

    def __str__(self):
        return f'{self.title}'

    class PydanticMeta:
        exclude = (
            'user.user_comments',
        )


class Comment(models.Model):
    id = fields.IntField(pk=True)

    text = fields.TextField()

    created = fields.DatetimeField(auto_now_add=True)
    updated = fields.DatetimeField(auto_now=True)

    post = fields.ForeignKeyField('models.Post', related_name='post_comments', on_delete=fields.CASCADE)
    user = fields.ForeignKeyField('models.User', related_name='user_comments', null=True, on_delete=fields.SET_NULL)
    reply_to_comment = fields.ForeignKeyField('models.Comment', default=None, null=True, on_delete=fields.SET_NULL)

    comment_images: fields.ReverseRelation['Image']

    def __str__(self):
        return f'Post: {self.post} From user: {self.user} To: {self.reply_to_comment.user}'

    class PydanticMeta:
        exclude = (
            'post.post_comments',
            'user.user_comments',
            'reply_to_comment',
            'comments'
        )


tortoise.Tortoise.init_models(["src.db.models"], "models")
