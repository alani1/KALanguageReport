from django.contrib import admin
from LanguageStatistic.models import Video, Subtitle, LanguageStatistic, Language
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from utils import ftime

from datetime import date

# Register your models here.

langs = ('ENGLISH', 'DEUTSCH')

class KAAdmin(admin.ModelAdmin):
    class Media:
        js = (
            'jquery.multiple.select.js',
            'KAReportAdmin.js',
        )

class VideoResource(resources.ModelResource):
    class Meta:
        model = Video
        exclude = ('id','deTranslator', 'amaraOK', 'showsExercise' )

#create a YT Link to the video
def YT_LINK(obj):
    href = "https://www.youtube.com/watch?v=" + obj.DEUTSCH
    return '<a target="_blank" href="{0}">{1}</a>'.format(href, obj.DEUTSCH)
YT_LINK.short_description = 'DE Youtube'
YT_LINK.allow_tags = True

#Show the duration in nicely formated way
def Time(obj):
    return ftime(obj.DURATION)
    
@admin.register(Video)
#class VideoAdmin(admin.ModelAdmin):
class VideoAdmin(ImportExportModelAdmin):
    resource_class = VideoResource
    ordering = ['SERIAL']
    search_fields = ['TITLE', 'DOMAIN', 'SUBJECT', 'TOPIC', 'TUTORIAL', 'REQUIRED_FOR', 'AMARA_ID', 'ENGLISH', 'DEUTSCH' ]
    list_filter = ('showsExercise','deTranslator','DATE_ADDED','REQUIRED_FOR','DOMAIN', 'SUBJECT', 'TOPIC','TUTORIAL')
    
    
    list_display = ('DATE_ADDED', 'TITLE', 'DOMAIN', 'SUBJECT', 'TOPIC', 'TUTORIAL', Time, YT_LINK, 'deTranslator', 'showsExercise')
    list_display_links = ('DATE_ADDED', 'TITLE')
    fieldsets = (
        (None, {
            'fields': (('SERIAL', 'TITLE'), ('DATE_CREATED', 'DATE_ADDED'),  ('DOMAIN', 'SUBJECT', 'TOPIC', 'TUTORIAL'), ('ENGLISH','AMARA_ID','amaraOK', 'showsExercise'), ('URL'), ('DEUTSCH', 'deTranslator') ),
         }),
         ('More Languages', {
            'classes': ('collapse',),
            'fields': ()
         })
         )
         
    #change_list_template = "LanguageStatistic/adminChangeList.html"         
    class Media:
        js = (
            'jquery.multiple.select.js',
            'KAReportAdmin.js',
        )
     
    
    #date_hierarchy = 'DATE_ADDED'
    pass
    



@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = [ 'enabled', 'name', 'code', 'target', 'ename', 'master', 'cID']
    pass
    
@admin.register(Subtitle)
class SubtitleAdmin(KAAdmin):
    list_display = ( 'created', 'amaraID', 'lang', 'title', 'author',  'origLines', 'lines', 'completion', 'percentDone', 'infoData')
    search_fields = ( 'amaraID', 'title', 'author' )
    list_filter = ( 'completion', 'lang', 'author')    
    pass

@admin.register(LanguageStatistic)
class LanguageStatisticAdmin(KAAdmin):
    ordering = ['-date','lang','type']
    list_display = ('date', 'lang', 'type','target', 'total', 'count', 'speed', 'totalSecs', 'countSecs', 'speedSecs','totalStrings','countStrings','speedStrings')
    list_filter = ('date','lang','type','target',)
    date_hierarchy = 'date'
    pass