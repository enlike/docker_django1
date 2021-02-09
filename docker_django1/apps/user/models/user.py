import uuid

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords

from docker_django1.apps.core.models.models import BaseModel
from docker_django1.apps.core.models.operations.customIndex import (
    UpperGistIndex,
    UpperIndex,
)
from docker_django1.apps.core.utils.common import short_fio
from docker_django1.apps.user.managers.user import EmailUserManager


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    email = models.EmailField(max_length=256, verbose_name='Email', unique=True)

    email_verified = models.BooleanField(
        default=False,
        verbose_name='Email подтвержден',
    )

    first_name = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name='Имя',
    )

    last_name = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name='Фамилия',
    )

    middle_name = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name='Отчество',
    )

    is_staff = models.BooleanField(  # also used to mark test users in prod
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )

    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    history = HistoricalRecords(
        excluded_fields=['modified'],
        inherit=True,
    )

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'

    objects = EmailUserManager()

    class Meta:
        verbose_name = 'Данные для логина'
        verbose_name_plural = 'Данные для логина'
        indexes = [
            UpperGistIndex(
                fields=[
                    'last_name',
                    'first_name',
                    'middle_name',
                ],
                name='%(app_label)s_lfm_gist_up_idx',
                opclasses=[
                    'gist_trgm_ops',
                    'gist_trgm_ops',
                    'gist_trgm_ops',
                ],
            ),
            UpperIndex(
                fields=[
                    'last_name',
                    'first_name',
                    'middle_name',
                ],
                name='%(app_label)s_lfm_up_idx',
                opclasses=[
                    'varchar_pattern_ops',
                    'varchar_pattern_ops',
                    'varchar_pattern_ops',
                ],
            ),
            UpperGistIndex(
                fields=['email'],
                opclasses=[
                    'gist_trgm_ops',
                ],
                name='%(app_label)s_email_gist_up_idx',
            ),
            UpperIndex(
                fields=['email'],
                opclasses=[
                    'varchar_pattern_ops',
                ],
                name='%(app_label)s_email_up_idx',
            ),
            models.Index(
                fields=[
                    'last_name',
                    'first_name',
                    'middle_name',
                ],
                name='%(app_label)s_lfm_idx',
            ),
        ]

    def delete(self, using=None, keep_parents=False):
        self.hard_delete(using, keep_parents)

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def __str__(self):
        if self.get_full_name():
            return f'{self.get_full_name()} ({self.email})'
        else:
            return self.email

    def get_full_name(self):
        return (
            ' '.join([self.last_name, self.first_name, self.middle_name])
            if self.last_name and self.first_name and self.middle_name
            else ''
        )

    def get_short_name(self):
        return (
            ' '.join([self.last_name, self.first_name])
            if self.last_name and self.first_name
            else ''
        )

    def get_alternative_name(self):
        return (
            ' '.join([self.first_name, self.middle_name])
            if self.first_name and self.middle_name
            else ''
        )

    def get_abbreviation_name(self):
        return (
            short_fio(self.first_name, self.last_name, self.middle_name)
            if self.first_name and self.last_name and self.middle_name
            else ''
        )
