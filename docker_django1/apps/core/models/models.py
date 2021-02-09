from django.db import models
from django.db.models import QuerySet, Subquery
from django.utils import timezone


class SoftDeletionQuerySet(QuerySet):
    def delete(self):
        return super(SoftDeletionQuerySet, self).update(deleted=True)

    def hard_delete(self):
        return super(SoftDeletionQuerySet, self).delete()

    def alive(self):
        return self.filter(deleted=False)

    def dead(self):
        return self.exclude(deleted=False)


class BaseManager(models.Manager):
    """
    Manager to return only active (not deleted) objects
    """

    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop('alive_only', True)
        super().__init__(*args, **kwargs)

    def get_queryset(self):
        if self.alive_only:
            return SoftDeletionQuerySet(self.model).filter(deleted=False)
        return SoftDeletionQuerySet(self.model)

    def hard_delete(self):
        return self.get_queryset().hard_delete()


class BaseModel(models.Model):
    """
    Model that is not deleted by default, by only marked as deleted
    """

    created = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True,
        db_index=True,
        editable=False,
    )

    modified = models.DateTimeField(
        verbose_name='Дата изменения',
        auto_now=True,
        db_index=True,
        editable=False,
    )

    deleted = models.BooleanField(verbose_name='Удален', default=False, editable=False)

    # hide deleted records
    objects = BaseManager()  # type: ignore
    # all objects in db
    all_objects = BaseManager(alive_only=False)  # type: ignore

    def delete(self, using=None, keep_parents=False):
        self.deleted = True
        self.save()

    def hard_delete(self, using=None, keep_parents=False):
        super(BaseModel, self).delete(using, keep_parents)

    class Meta:
        abstract = True
        indexes = [
            models.Index(
                fields=[
                    'created',
                ],
                name='%(app_label)s_%(class)s_cd_idx',
            ),
            models.Index(
                fields=[
                    'modified',
                ],
                name='%(app_label)s_%(class)s_md_idx',
            ),
            models.Index(
                fields=[
                    'deleted',
                ],
                name='%(app_label)s_%(class)s_dt_idx',
            ),
        ]


class Array(Subquery):
    template = 'ARRAY(%(subquery)s)'
