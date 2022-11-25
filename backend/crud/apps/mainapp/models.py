from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation


class User(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('Пользователь'))

    posts = GenericRelation('mainapp.Post')
    comments = GenericRelation('mainapp.Comment')
    images = GenericRelation('mainapp.Image')
    videos = GenericRelation('mainapp.Video')

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')


class Post(models.Model):
    title = models.CharField(_('Название'), max_length=255)
    text = models.TextField(_('Текст'))

    active = models.BooleanField(_('Активное'), default=True)

    created = models.DateTimeField(_('Дата создания'), auto_now_add=True)
    updated = models.DateTimeField(_('Дата последнего обновления'), auto_now=True)

    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='user_posts', null=True, blank=True)

    comments = GenericRelation('mainapp.Comment')
    images = GenericRelation('mainapp.Image')
    videos = GenericRelation('mainapp.Video')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = _('Пост')
        verbose_name_plural = _('Посты')


class Image(models.Model):
    main = models.BooleanField(_('Основное фото'), default=False)
    image = models.ImageField(_('Фото'), default=None)
    video_url = models.URLField(_('Ссылка на фото'), default=None, validators=[])

    active = models.BooleanField(_('Активное'), default=True)

    created = models.DateTimeField(_('Дата создания'), auto_now_add=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    @property
    def url(self):
        raise NotImplementedError

    class Meta:
        verbose_name = _('Картинка')
        verbose_name_plural = _('Картинки')


class Video(models.Model):
    main = models.BooleanField(_('Основное видео'), default=False)

    video = models.FileField(_('Видео'), default=None)
    video_url = models.URLField(_('Ссылка на видео'), default=None, validators=[])

    active = models.BooleanField(_('Активное'), default=True)

    created = models.DateTimeField(_('Дата создания'), auto_now_add=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    @property
    def url(self):
        raise NotImplementedError

    class Meta:
        verbose_name = _('Видео')
        verbose_name_plural = _('Видео')


class Comment(models.Model):
    text = models.TextField(_('Текст'))

    created = models.DateTimeField(_('Дата создания'), auto_now_add=True)
    updated = models.DateTimeField(_('Дата последнего обновления'), auto_now=True)

    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='user_comments', null=True, blank=True)

    # Only User & Post
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    images = GenericRelation('mainapp.Image')
    videos = GenericRelation('mainapp.Video')

    def __str__(self):
        # Если content_type == Comment, то будет ответ на комментарий
        # Иначе будет просто комментарий

        pass

    class Meta:
        verbose_name = _('Коммент')
        verbose_name_plural = _('Комменты')

