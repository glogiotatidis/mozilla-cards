# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Template'
        db.create_table('cardmanager_template', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('default', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('template_front', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('template_back', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal('cardmanager', ['Template'])


    def backwards(self, orm):
        
        # Deleting model 'Template'
        db.delete_table('cardmanager_template')


    models = {
        'cardmanager.template': {
            'Meta': {'object_name': 'Template'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'template_back': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'template_front': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['cardmanager']
