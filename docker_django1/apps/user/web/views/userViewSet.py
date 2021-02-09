import logging
from typing import Tuple

from docker_django1.apps.core.web.views.base import BaseView
from docker_django1.apps.user.serializers import UserSerializer

from docker_django1.apps.user.tasks import UserTaskTest
from docker_django1.apps.user.web.filters import UserFilter

logger = logging.getLogger(__file__)


class UserViewSet(BaseView):
    # filter_backends = (DjangoFilterBackend,)
    filterset_class = UserFilter
    serializer_class = UserSerializer
    order_args: Tuple = ('-created', 'email')

    def list(self, request, *args, **kwargs):
        # self.execute_simple_celery_task()
        return super(UserViewSet, self).list(request, *args, **kwargs)

    @staticmethod
    def execute_simple_celery_task():
        task = UserTaskTest.delay('email', email='test1@mail.com')
        logger.info(f'TASK.RESULT={task.result}')
