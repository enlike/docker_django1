from json import JSONEncoder
import functools
import logging
import time
from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.http import QueryDict
from django.utils import timezone
from typing import List
from uuid import UUID

logger = logging.getLogger(__file__)


class UUIDEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return obj.hex
        return JSONEncoder.default(self, obj)


def add_queryparams_to_url(redirect_url, data):
    """Добавить queryparams в django-admin"""
    q_dict = QueryDict(mutable=True)
    q_dict.update(data)
    redirect_url += '?' + q_dict.urlencode()
    return redirect_url


def func_exec_time(*args, **kwargs):
    """
    Декоратор для отображения времени выполнения функции
    Принимает аргументы и пары ключ-значение

    Просто оборачиваете нужную функцию, у которой нужно узнать время на выполненине.
    Example:
        @func_exec_time()
        def somefunc():
    """
    log_func = logger.info if kwargs.get('loud') else logger.debug

    def _func_exec_time(func):
        @functools.wraps(func)
        def wrapper_timer(*args, **kwargs):
            start_time = time.perf_counter()
            value = func(*args, **kwargs)
            run_time = time.perf_counter() - start_time
            log_func(
                f"{func.__module__} : Функция {func.__name__!r} была выполнена за {run_time:.4f} секунд"
            )
            return value

        return wrapper_timer

    return _func_exec_time


def hours_with_morphology(duration: int) -> str:
    """
    The number of hours, taking into account morphology
    """
    if str(duration)[-1] == '1' and duration != 11:
        return f'{duration} час'
    elif str(duration)[-1] in ['2', '3', '4'] and duration not in [12, 13, 14]:
        return f'{duration} часа'
    else:
        return f'{duration} часов'


def emails_splitter(emails_str: str, raise_exception: bool = False) -> List[str]:
    """
    Split emails from string to set of normalized values
    """
    emails_str = emails_str.strip()
    if not emails_str:
        return list()

    if ',' in emails_str:
        emails = emails_str.split(',')
    else:
        emails = emails_str.split()

    result = [BaseUserManager.normalize_email(email.strip()) for email in emails]
    for email in result:
        try:
            EmailValidator(f'email "{email}" is incorrect')(email)
        except ValidationError as e:
            if raise_exception:
                raise e
            else:
                logger.error('email %s is incorrect', email)

    return result


def short_fio(first_name: str, last_name: str, middle_name: str) -> str:
    short_first_name = f'{first_name[0].upper()}.' if first_name else ''
    short_middle_name = f'{middle_name[0].upper()}.' if middle_name else ''
    return f'{last_name} ' + short_first_name + short_middle_name


def last_year() -> int:
    return timezone.now().year - 1


def name_processing(value: str) -> str:
    """Заменить Ёё на Ее"""
    if not isinstance(value, str) and not value:
        return value
    return value.strip().replace('Ё', "Е").replace('ё', 'е')
