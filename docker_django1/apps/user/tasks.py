from celery import chord, group, Task
from celery.utils.log import get_task_logger
from django.conf import settings

from docker_django1.apps.user.models import User

logger = get_task_logger(__name__)

app = settings.CELERY_APP


class UserTaskTest(Task):
    def run(self, *args, **kwargs):
        users = User.objects.filter(**kwargs).order_by(*args)
        return users.values('email', 'last_name', 'first_name')


UserTaskTest = app.register_task(UserTaskTest())
