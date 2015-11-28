# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_auto_20151127_1507'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='assistant',
            field=models.ForeignKey(related_name='assistant_courses', db_constraint=False, blank=True, to='coaches.Coach', null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='coach',
            field=models.ForeignKey(related_name='coach_courses', db_constraint=False, blank=True, to='coaches.Coach', null=True),
        ),
    ]
