# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Removing unique constraint on 'UrlVideoLink', fields ['url']
        db.delete_unique('ooyala_urlvideolink', ['url'])

        # Changing field 'VideoPage.site'
        db.alter_column('ooyala_videopage', 'site_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'], null=True))

        # Changing field 'SiteChannels.site'
        db.alter_column('ooyala_sitechannels', 'site_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'], null=True))


    def backwards(self, orm):
        
        # Changing field 'VideoPage.site'
        db.alter_column('ooyala_videopage', 'site_id', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['sites.Site']))

        # Adding unique constraint on 'UrlVideoLink', fields ['url']
        db.create_unique('ooyala_urlvideolink', ['url'])

        # Changing field 'SiteChannels.site'
        db.alter_column('ooyala_sitechannels', 'site_id', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['sites.Site']))


    models = {
        'ooyala.ooyalachannellist': {
            'Meta': {'object_name': 'OoyalaChannelList'},
            'channel': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'channel'", 'unique': 'True', 'to': "orm['ooyala.OoyalaItem']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'videos': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'videos'", 'symmetrical': 'False', 'to': "orm['ooyala.OoyalaItem']"})
        },
        'ooyala.ooyalaitem': {
            'Meta': {'ordering': "('title',)", 'object_name': 'OoyalaItem'},
            'content_type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'embed_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'flight_start_time': ('django.db.models.fields.DateTimeField', [], {}),
            'height': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'length': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']", 'null': 'True', 'blank': 'True'}),
            'size': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'stat': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '5', 'max_length': '10'}),
            'tags': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'thumbnail': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {}),
            'width': ('django.db.models.fields.IntegerField', [], {})
        },
        'ooyala.sitechannels': {
            'Meta': {'object_name': 'SiteChannels'},
            'channel': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['ooyala.OoyalaChannelList']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']", 'null': 'True', 'blank': 'True'})
        },
        'ooyala.urlvideolink': {
            'Meta': {'object_name': 'UrlVideoLink'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ooyala.OoyalaItem']"}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['sites.Site']", 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'ooyala.videopage': {
            'Meta': {'unique_together': "(('site', 'url'),)", 'object_name': 'VideoPage'},
            'featured_item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'featured_item'", 'to': "orm['ooyala.OoyalaItem']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'items': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['ooyala.OoyalaItem']", 'symmetrical': 'False'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']", 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['ooyala']
