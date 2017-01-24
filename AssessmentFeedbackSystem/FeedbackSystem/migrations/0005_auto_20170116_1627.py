# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('FeedbackSystem', '0004_auto_20170116_1619'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='title',
            field=models.CharField(max_length=50),
        ),
    ]
