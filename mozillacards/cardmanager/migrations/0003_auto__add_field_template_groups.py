# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Template.groups'
        db.add_column('cardmanager_template', 'groups', self.gf('django.db.models.fields.CharField')(default='', max_length=1000), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Template.groups'
        db.delete_column('cardmanager_template', 'groups')


    models = {
        'cardmanager.template': {
            'Meta': {'object_name': 'Template'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'groups': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1000'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'template_back': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'template_front': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['cardmanager']
