from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password

class m_UserManager(BaseUserManager):
    """
    Custom manager for m_User.
    """

    def create_user(self, username, email, password=None, **extra_fields):
        """
        Create and return a regular user with an email and password.
        """
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)  # Normalize the email
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)  # Hash the password before saving
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        """
        Create and return a superuser with an email, username, and password.
        """
        extra_fields.setdefault('is_admin', True)
        return self.create_user(username, email, password, **extra_fields)

    def get_by_natural_key(self, username):
        """
        Allows the authentication system to lookup users by their username.
        """
        return self.get(username=username)
