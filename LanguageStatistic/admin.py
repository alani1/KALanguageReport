from django.contrib import admin
from LanguageStatistic.models import Video, Subtitle, LanguageStatistic, Language
# Register your models here.

langs = ('ENGLISH', 'DEUTSCH')

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    ordering = ['SERIAL']
    search_fields = ['TITLE', 'DOMAIN', 'SUBJECT', 'TOPIC', 'TUTORIAL', 'REQUIRED_FOR', 'AMARA_ID', 'ENGLISH', 'DEUTSCH']
    list_filter = ('amaraOK','DATE_ADDED','REQUIRED_FOR','DOMAIN', 'SUBJECT', 'TOPIC', 'TUTORIAL')
    list_display = ('DATE_ADDED', 'TITLE', 'DOMAIN', 'SUBJECT', 'TOPIC', 'TUTORIAL', 'REQUIRED_FOR')
    fieldsets = (
        (None, {
            'fields': (('SERIAL', 'TITLE'), ('DATE_CREATED', 'DATE_ADDED'),  ('DOMAIN', 'SUBJECT', 'TOPIC', 'TUTORIAL'), ('ENGLISH','AMARA_ID','amaraOK'), ('DEUTSCH', 'deTranslator') ),
         }),
         ('More Languages', {
            'classes': ('collapse',),
            'fields': ()
         })
         )
    
    #date_hierarchy = 'DATE_ADDED'
    pass

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = [ 'enabled', 'name', 'code', 'target', 'ename', 'master', 'cID']
    pass
    
@admin.register(Subtitle)
class SubtitleAdmin(admin.ModelAdmin):
    list_display = ( 'created', 'amaraID', 'lang', 'title', 'author',  'origLines', 'lines', 'completion', 'percentDone', 'infoData')
    search_fields = ( 'amaraID', 'title', 'author' )
    list_filter = ( 'completion', 'lang', 'author')
    pass

@admin.register(LanguageStatistic)
class LanguageStatisticAdmin(admin.ModelAdmin):
    ordering = ['-date','lang','type']
    list_display = ('date', 'lang', 'type','target', 'total', 'count', 'speed', 'totalSecs', 'countSecs', 'speedSecs','totalStrings','countStrings','speedStrings')
    list_filter = ('date','lang','type','target',)
    date_hierarchy = 'date'
    pass