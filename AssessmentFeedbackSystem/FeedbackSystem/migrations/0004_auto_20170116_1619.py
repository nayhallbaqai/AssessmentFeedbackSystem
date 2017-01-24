# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('FeedbackSystem', '0003_auto_20161219_1604'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='usedNum',
            field=models.BigIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='feedbacktostudent',
            name='comments',
            field=models.ForeignKey(to='FeedbackSystem.Comment'),
        ),
    ]
