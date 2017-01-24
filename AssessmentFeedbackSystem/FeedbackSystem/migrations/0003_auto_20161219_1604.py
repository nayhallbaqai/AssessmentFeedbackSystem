# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('FeedbackSystem', '0002_auto_20161219_1559'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='slug',
            field=models.SlugField(),
        ),
    ]
