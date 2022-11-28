import os
import datetime
import binascii

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Token(models.Model):
    key = models.CharField(_('Токен'), max_length=50, primary_key=True)
    customer_id = models.CharField(_('ID пользователя'), max_length=20, db_index=True)
    created = models.DateTimeField(_('Дата создания'))

    LIFETIME = datetime.timedelta(hours=24*30)
    _customer = None

    def __str__(self):
        return self.pk

    @property
    def expires(self):
        return self.created + self.LIFETIME

    @property
    def is_expired(self):
        return timezone.now() > self.expires

    @classmethod
    def expired_qs(cls):
        return cls.objects.filter(created__lt=timezone.now() - cls.LIFETIME)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.pk = self.generate_key()
            self.created = timezone.now()
        super(Token, self).save(*args, **kwargs)

    @classmethod
    def generate_key(cls):
        return binascii.hexlify(os.urandom(20)).decode()

    @property
    def customer(self):
        from apps.mainapp.models import User

        if not self._customer:
            self._customer = User.objects.filter(
                pk=self.customer_id
            ).first()

        return self._customer

    class Meta:
        verbose_name = _('Токен')
        verbose_name_plural = _('Токены')
