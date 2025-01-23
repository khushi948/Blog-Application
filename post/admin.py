from django.contrib import admin
from .models import m_Category
from .models import t_Post
from .models import t_Image
# Register your models here.

admin.site.register(m_Category)
admin.site.register(t_Post)
admin.site.register(t_Image)