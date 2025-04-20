from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.timezone import now
from django.db import models
from .managers import m_UserManager
from django.contrib.auth.hashers import make_password, check_password
class m_User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=20, unique=True)
    email = models.CharField(max_length=30, unique=True)
    phone_no = models.CharField(max_length=10)
    password = models.CharField(max_length=255)
    is_admin = models.BooleanField(null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=now)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = m_UserManager()

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith('$'):
            self.set_password(self.password)
        super().save(*args, **kwargs)

    def soft_delete(self):
        self.deleted_at = now()
        self.save()

    def __str__(self):
        return self.username
