# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AccessLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(db_index=True)),
                ('bytes_sent', models.CharField(max_length=500)),
                ('referer', models.TextField()),
                ('request', models.TextField()),
                ('http_method', models.CharField(max_length=500)),
                ('http_version', models.CharField(max_length=500)),
                ('remote_host', models.CharField(max_length=500)),
                ('remote_login', models.CharField(max_length=500)),
                ('remote_user', models.CharField(max_length=500)),
                ('status', models.CharField(max_length=500)),
                ('user_agent', models.CharField(max_length=500)),
                ('request_time', models.CharField(max_length=500)),
                ('upstream_response_time', models.CharField(max_length=500)),
                ('pipe', models.CharField(max_length=500)),
            ],
            options={
                'ordering': ('-timestamp',),
            },
        ),
    ]
