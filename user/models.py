from django.db import models
from django.utils.timezone import now

from django.contrib.auth.hashers import make_password,check_password
# Create your models here.
from .managers import m_UserManager

class SoftDelete(models.Manager):
    #excludes the deleted items from query set
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)
    


class m_User(models.Model):
    username=models.CharField(max_length=20,unique=True)
    email=models.CharField(max_length=30,unique=True)
    phone_no=models.CharField(max_length=10)
    password=models.CharField(max_length=255)
    is_admin=models.BooleanField(null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=now)
    updated_at=models.DateTimeField(auto_now=True) 
    deleted_at=models.DateTimeField(null=True, blank=True)

    objects = m_UserManager()  # Show only active records
    all_objects = models.Manager()  # Includes both deleted and active records

    REQUIRED_FIELDS = ['email']  # Fields required when creating a superuser
    USERNAME_FIELD = 'username'  # Field used for login


    
    def set_password(self, raw_password):
        """
        Hashes the password and saves it.
        """
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """
        Compares the raw password with the hashed password.
        """
        return check_password(raw_password, self.password)
    def save(self, *args, **kwargs):
        # Automatically hash the password before saving
        if self.password and not self.password.startswith('$'):  # Check if password is plain text
            self.set_password(self.password)  # Hash the password if it's plain text
        super(m_User, self).save(*args, **kwargs)  # Call the parent save method


    def soft_delete(self):
        #marks the timestamp when deleted
        self.deleted_at = now()
        self.save()

    @property
    def is_deleted(self):
        #checks if it is deleted or not
        return self.deleted_at is not None
    @property
    def is_authenticated(self):
        """
        Always return True for authenticated users.
        """
        return True

    @property
    def is_anonymous(self):
        """
        Always return False for authenticated users.
        """
        return False
    def has_perm(self, perm, obj=None):
       return self.is_admin

    def has_module_perms(self, app_label):
       return self.is_admin

    def __str__(self):
        return self.username
"""hfrom django.contrib.auth.hashers import make_password
from user.models import m_User

# Loop through all users and rehash their passwords
for user in m_User.objects.all():
    if not user.password.startswith('$'):  # Check if password is plain text
        user.set_password(user.password)  # Hash the password
        user.save()  # Save the user with the hashed password
        print(f"Password for {user.username} has been hashed.")  """
    