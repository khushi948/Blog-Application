from django.db import models
from post.models import t_Post
from django.utils.timezone import now
# Create your models here.

class SoftDelete(models.Manager):
    #excludes the deleted items from query set
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)

class t_Images(models.Model):
    images=models.ImageField(upload_to='Images/post_images/',default='')
    post_id=models.ForeignKey(t_Post,on_delete=models.CASCADE,default='1',related_name='images')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    deleted_at=models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return  f"Image {self.id}, {self.images}"
    
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
    