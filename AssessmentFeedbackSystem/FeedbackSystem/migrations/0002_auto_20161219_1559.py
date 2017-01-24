# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('FeedbackSystem', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='slug',
            field=models.SlugField(null=True),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='title',
            field=models.CharField(unique=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='comment',
            name='isGeneral',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='feedbacktostudent',
            name='comments',
            field=models.ForeignKey(blank=True, to='FeedbackSystem.Comment', null=True),
        ),
    ]
