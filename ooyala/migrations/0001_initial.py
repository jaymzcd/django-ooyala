# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'OoyalaItem'
        db.create_table('ooyala_ooyalaitem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('embed_code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=5, max_length=10)),
            ('content_type', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('length', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('size', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('flight_start_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('width', self.gf('django.db.models.fields.IntegerField')()),
            ('height', self.gf('django.db.models.fields.IntegerField')()),
            ('thumbnail', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('stat', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('tags', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('ooyala', ['OoyalaItem'])

        # Adding model 'OoyalaChannelList'
        db.create_table('ooyala_ooyalachannellist', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('channel', self.gf('django.db.models.fields.related.ForeignKey')(related_name='channel', unique=True, to=orm['ooyala.OoyalaItem'])),
        ))
        db.send_create_signal('ooyala', ['OoyalaChannelList'])

        # Adding M2M table for field videos on 'OoyalaChannelList'
        db.create_table('ooyala_ooyalachannellist_videos', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('ooyalachannellist', models.ForeignKey(orm['ooyala.ooyalachannellist'], null=False)),
            ('ooyalaitem', models.ForeignKey(orm['ooyala.ooyalaitem'], null=False))
        ))
        db.create_unique('ooyala_ooyalachannellist_videos', ['ooyalachannellist_id', 'ooyalaitem_id'])

        # Adding model 'UrlVideoLink'
        db.create_table('ooyala_urlvideolink', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ooyala.OoyalaItem'])),
        ))
        db.send_create_signal('ooyala', ['UrlVideoLink'])

        # Adding model 'VideoPage'
        db.create_table('ooyala_videopage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('featured_item', self.gf('django.db.models.fields.related.ForeignKey')(related_name='featured_item', to=orm['ooyala.OoyalaItem'])),
        ))
        db.send_create_signal('ooyala', ['VideoPage'])

        # Adding M2M table for field items on 'VideoPage'
        db.create_table('ooyala_videopage_items', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('videopage', models.ForeignKey(orm['ooyala.videopage'], null=False)),
            ('ooyalaitem', models.ForeignKey(orm['ooyala.ooyalaitem'], null=False))
        ))
        db.create_unique('ooyala_videopage_items', ['videopage_id', 'ooyalaitem_id'])


    def backwards(self, orm):
        
        # Deleting model 'OoyalaItem'
        db.delete_table('ooyala_ooyalaitem')

        # Deleting model 'OoyalaChannelList'
        db.delete_table('ooyala_ooyalachannellist')

        # Removing M2M table for field videos on 'OoyalaChannelList'
        db.delete_table('ooyala_ooyalachannellist_videos')

        # Deleting model 'UrlVideoLink'
        db.delete_table('ooyala_urlvideolink')

        # Deleting model 'VideoPage'
        db.delete_table('ooyala_videopage')

        # Removing M2M table for field items on 'VideoPage'
        db.delete_table('ooyala_videopage_items')


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
            'size': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'stat': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '5', 'max_length': '10'}),
            'tags': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'thumbnail': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {}),
            'width': ('django.db.models.fields.IntegerField', [], {})
        },
        'ooyala.urlvideolink': {
            'Meta': {'object_name': 'UrlVideoLink'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ooyala.OoyalaItem']"}),
            'url': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'ooyala.videopage': {
            'Meta': {'object_name': 'VideoPage'},
            'featured_item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'featured_item'", 'to': "orm['ooyala.OoyalaItem']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'items': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['ooyala.OoyalaItem']", 'symmetrical': 'False'}),
            'url': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        }
    }

    complete_apps = ['ooyala']
