# Generated by Django 5.1.5 on 2025-01-24 09:19

from django.conf import settings
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
       
    
    ]

    operations = [
        migrations.CreateModel(
            name='t_Images',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('images', models.ImageField(default='', upload_to='Images/post_images/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('post_id', models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, related_name='images', to='post.t_post')),
            ],
        ),
    ]
