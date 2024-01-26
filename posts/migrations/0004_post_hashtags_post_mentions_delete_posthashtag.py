# Generated by Django 5.0 on 2024-01-26 09:32

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_hashtag_posthashtag_report'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='hashtags',
            field=models.ManyToManyField(related_name='posts', to='posts.hashtag'),
        ),
        migrations.AddField(
            model_name='post',
            name='mentions',
            field=models.ManyToManyField(related_name='mentions', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='PostHashtag',
        ),
    ]
