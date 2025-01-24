from django.contrib import admin
from .models import m_Category
from .models import t_Post
from .models import m_comment
# from .models import t_Images
# Register your models here.

admin.site.register(m_Category)
admin.site.register(t_Post)
admin.site.register(m_comment)
# admin.site.register(t_Images)