# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('FeedbackSystem', '0007_auto_20170122_1338'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='admin',
        ),
        migrations.AlterField(
            model_name='course',
            name='tutors',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
