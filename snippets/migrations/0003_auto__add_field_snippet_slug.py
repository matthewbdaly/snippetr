# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Snippet.slug'
        db.add_column(u'snippets_snippet', 'slug',
                      self.gf('django.db.models.fields.SlugField')(default='blah', unique=True, max_length=40),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Snippet.slug'
        db.delete_column(u'snippets_snippet', 'slug')


    models = {
        u'snippets.snippet': {
            'Meta': {'object_name': 'Snippet'},
            'content': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 3, 0, 0)'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '40'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['snippets']