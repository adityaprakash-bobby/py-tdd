# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-06-06 19:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='token',
            name='email',
            field=models.EmailField(default='a@b.com', max_length=254),
            preserve_default=False,
        ),
    ]
