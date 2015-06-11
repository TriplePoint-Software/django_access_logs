# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'AccessLog'
        db.create_table('access_logs_accesslog', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
            ('bytes_sent', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('referer', self.gf('django.db.models.fields.TextField')()),
            ('request', self.gf('django.db.models.fields.TextField')()),
            ('http_method', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('http_version', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('remote_host', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('remote_login', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('remote_user', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('user_agent', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('request_time', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('upstream_response_time', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('pipe', self.gf('django.db.models.fields.CharField')(max_length=500)),
        ))
        db.send_create_signal('access_logs', ['AccessLog'])


    def backwards(self, orm):
        # Deleting model 'AccessLog'
        db.delete_table('access_logs_accesslog')


    models = {
        'access_logs.accesslog': {
            'Meta': {'ordering': "('-timestamp',)", 'object_name': 'AccessLog'},
            'bytes_sent': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'http_method': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'http_version': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pipe': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'referer': ('django.db.models.fields.TextField', [], {}),
            'remote_host': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'remote_login': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'remote_user': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'request': ('django.db.models.fields.TextField', [], {}),
            'request_time': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'upstream_response_time': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'user_agent': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        }
    }

    complete_apps = ['access_logs']