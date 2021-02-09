from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import Group

ADMINISTRATOR_GROUP = 'administrator'


class EmailUserManager(BaseUserManager):
    """
    A custom user manager to deal with emails as unique identifiers for auth
    instead of usernames. The default that's used is "UserManager"
    """

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('email_verified', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)

    def get_by_natural_key(self, username):
        """
        By default, Django does a case-sensitive check on usernames. This is Wrong™.
        Overriding this method fixes it.
        """
        return self.get(**{self.model.USERNAME_FIELD + '__iexact': username})


class AdministratorUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        """
        Creates and saves a Administrator with the given email and password.
        """
        if not email:
            raise ValueError('The Email must be set')

        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = False
        extra_fields['is_active'] = True
        extra_fields.setdefault('email_verified', True)

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()

        user.groups.add(Group.objects.get(name=ADMINISTRATOR_GROUP))

        return user
