from django.db import models
from user.models import m_User
from django.utils.timezone import now
# from django.contrib.auth.models import AbstractUser
# Create your models here.

class SoftDelete(models.Manager):
    #excludes the deleted items from query set
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)
    

class m_Category(models.Model):
    name=models.CharField(max_length=50)
    created_at=models.DateTimeField(auto_now_add=True)
    deleted_at=models.DateTimeField(null=True, blank=True)


    objects = SoftDelete()  # Show only active records
    all_objects = models.Manager()  # Includes both deleted and active records

    def __str__(self):
        return self.name
    
    def soft_delete(self):
        self.deleted_at = now()
        self.save()

    @property
    def is_deleted(self):
        #checks if it is deleted or not
        return self.deleted_at is not None

    
class t_Post(models.Model):
    user_id=models.ForeignKey(m_User,on_delete=models.CASCADE)
    category_id=models.ForeignKey(m_Category,on_delete=models.CASCADE)
    title=models.CharField(max_length=100)
    description=models.TextField()
    likes=models.IntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    deleted_at=models.DateTimeField(null=True, blank=True)

    objects = SoftDelete()  # Show only active records
    all_objects = models.Manager()  # Includes both deleted and active records

    def __str__(self):
        return self.title
    
    def soft_delete(self):
        #marks the timestamp when deleted
        self.deleted_at = now()
        self.save()

    @property
    def is_deleted(self):
        #checks if it is deleted or not
        return self.deleted_at is not None



    # def set_password(self, raw_password):
    #     """
    #     Hashes the password and saves it.
    #     """
    #     from django.contrib.auth.hashers import make_password
    #     self.password = make_password(raw_password)


# class t_Images(models.Model):
#     images=models.ImageField(upload_to='post/images/',default='')
#     post_id=models.ForeignKey(t_Post,on_delete=models.CASCADE,default='1',related_name='images')
#     created_at=models.DateTimeField(auto_now_add=True)
#     updated_at=models.DateTimeField(auto_now_add=True)
#     deleted_at=models.DateTimeField(null=True, blank=True)
#     def __str__(self):
#         return  f"Image {self.id}, {self.images}"
    
#     objects = SoftDelete()  # Show only active records
#     all_objects = models.Manager()  # Includes both deleted and active records

#     def soft_delete(self):
#         #marks the timestamp when deleted
#         self.deleted_at = now()
#         self.save()

#     @property
#     def is_deleted(self):
#         #checks if it is deleted or not
#         return self.deleted_at is not None
    

class m_comment(models.Model):
    post_id=models.ForeignKey(t_Post,on_delete=models.CASCADE)
    user_id=models.ForeignKey(m_User,on_delete=models.CASCADE)
    message=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    deleted_at=models.DateTimeField(null=True, blank=True)

    objects = SoftDelete()  # Show only active records
    all_objects = models.Manager()  # Includes both deleted and active records

    def soft_delete(self):
        #marks the timestamp when deleted
        self.deleted_at = now()
        self.save()

    @property
    def is_deleted(self):
        #checks if it is deleted or not
        return self.deleted_at is not None




