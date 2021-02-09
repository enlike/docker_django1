import logging

from rest_framework import status
from rest_framework.exceptions import (
    NotAuthenticated,
    AuthenticationFailed,
    ValidationError,
)
from rest_framework.views import exception_handler

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    Populate exception response object with `error_code` duplicated from HTTP status code
    and localized `message` intended to be shown to user by mobile client app.

    :type exc: Exception
    :param context: request context - {'view': View, 'args': args, 'kwargs': kwargs, 'request': Request}
    :return: response object with custom error data
    """
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    # Now add the HTTP status code to the response.
    if response is not None:
        if isinstance(exc, (NotAuthenticated, AuthenticationFailed)):
            response.status_code = status.HTTP_401_UNAUTHORIZED
        elif isinstance(exc, ValidationError):
            # log validation errors with lesser level
            logger.warning(exc)
        else:
            logger.exception(exc)

        if isinstance(response.data, list):
            response.data = {'errors': response.data}

        response.data['error_code'] = response.status_code
        if 'non_field_errors' in response.data:
            response.data['detail'] = '; '.join(response.data['non_field_errors'])
            del response.data['non_field_errors']

    return response
