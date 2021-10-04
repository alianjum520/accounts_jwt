from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from rest_framework_simplejwt.tokens import RefreshToken


class User(AbstractUser):

    """
    This model extends the built in user model of Django by using Abstract User
    Some fields are overrides and some new fields are added
    """

    username = models.CharField(max_length = 50, blank = True, null = True, unique = True)
    email = models.EmailField(_('email address'), unique = True)
    time_stamp = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']


    def __str__(self):

        """
        This function is used to return the email in string  format
        (Built-in Dunder Methods)
        """
        return "{}".format(self.email)


    def tokens(self):

        """
        This is used to create a jwt token for the user Custom tokens
        """
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
