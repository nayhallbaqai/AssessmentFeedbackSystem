# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('FeedbackSystem', '0006_auto_20170116_1655'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='admin',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='tutors',
            field=models.ManyToManyField(related_name='as_tutor', to=settings.AUTH_USER_MODEL),
        ),
    ]
