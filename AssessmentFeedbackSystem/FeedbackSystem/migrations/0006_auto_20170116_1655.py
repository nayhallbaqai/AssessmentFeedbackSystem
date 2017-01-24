# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('FeedbackSystem', '0005_auto_20170116_1627'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]
