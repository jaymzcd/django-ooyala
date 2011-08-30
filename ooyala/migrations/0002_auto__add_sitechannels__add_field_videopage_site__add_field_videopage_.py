# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Removing unique constraint on 'VideoPage', fields ['url']
        db.delete_unique('ooyala_videopage', ['url'])

        # Adding model 'SiteChannels'
        db.create_table('ooyala_sitechannels', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'])),
        ))
        db.send_create_signal('ooyala', ['SiteChannels'])

        # Adding M2M table for field channel on 'SiteChannels'
        db.create_table('ooyala_sitechannels_channel', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('sitechannels', models.ForeignKey(orm['ooyala.sitechannels'], null=False)),
            ('ooyalachannellist', models.ForeignKey(orm['ooyala.ooyalachannellist'], null=False))
        ))
        db.create_unique('ooyala_sitechannels_channel', ['sitechannels_id', 'ooyalachannellist_id'])

        # Adding field 'VideoPage.site'
        db.add_column('ooyala_videopage', 'site', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['sites.Site']), keep_default=False)

        # Adding field 'VideoPage.updated_at'
        db.add_column('ooyala_videopage', 'updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=None, blank=True), keep_default=False)

        # Adding unique constraint on 'VideoPage', fields ['url', 'site']
        db.create_unique('ooyala_videopage', ['url', 'site_id'])

        # Deleting field 'OoyalaItem.tags'
        db.delete_column('ooyala_ooyalaitem', 'tags')

        # Adding field 'OoyalaItem.site'
        db.add_column('ooyala_ooyalaitem', 'site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'], null=True, blank=True), keep_default=False)

        # Adding M2M table for field sites on 'UrlVideoLink'
        db.create_table('ooyala_urlvideolink_sites', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('urlvideolink', models.ForeignKey(orm['ooyala.urlvideolink'], null=False)),
            ('site', models.ForeignKey(orm['sites.site'], null=False))
        ))
        db.create_unique('ooyala_urlvideolink_sites', ['urlvideolink_id', 'site_id'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'VideoPage', fields ['url', 'site']
        db.delete_unique('ooyala_videopage', ['url', 'site_id'])

        # Deleting model 'SiteChannels'
        db.delete_table('ooyala_sitechannels')

        # Removing M2M table for field channel on 'SiteChannels'
        db.delete_table('ooyala_sitechannels_channel')

        # Deleting field 'VideoPage.site'
        db.delete_column('ooyala_videopage', 'site_id')

        # Deleting field 'VideoPage.updated_at'
        db.delete_column('ooyala_videopage', 'updated_at')

        # Adding unique constraint on 'VideoPage', fields ['url']
        db.create_unique('ooyala_videopage', ['url'])

        # Adding field 'OoyalaItem.tags'
        db.add_column('ooyala_ooyalaitem', 'tags', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True), keep_default=False)

        # Deleting field 'OoyalaItem.site'
        db.delete_column('ooyala_ooyalaitem', 'site_id')

        # Removing M2M table for field sites on 'UrlVideoLink'
        db.delete_table('ooyala_urlvideolink_sites')


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
            'thumbnail': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {}),
            'width': ('django.db.models.fields.IntegerField', [], {})
        },
        'ooyala.sitechannels': {
            'Meta': {'object_name': 'SiteChannels'},
            'channel': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['ooyala.OoyalaChannelList']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"})
        },
        'ooyala.urlvideolink': {
            'Meta': {'object_name': 'UrlVideoLink'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ooyala.OoyalaItem']"}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['sites.Site']", 'symmetrical': 'False'}),
            'url': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'ooyala.videopage': {
            'Meta': {'unique_together': "(('site', 'url'),)", 'object_name': 'VideoPage'},
            'featured_item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'featured_item'", 'to': "orm['ooyala.OoyalaItem']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'items': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['ooyala.OoyalaItem']", 'symmetrical': 'False'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
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
