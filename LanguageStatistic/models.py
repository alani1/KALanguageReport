from django.db import models
from django.contrib.auth.models import User

from jsonfield import JSONField
from django.utils import timezone

class Language(models.Model):
    def __unicode__(self):              # __unicode__ on Python 2
        return self.name
        
    TARGET = (
        ('Test', 'Testsite'),
        ('Live', 'Livesite'),
        ('Rockstar', 'Rockstar'),
    )

    enabled = models.BooleanField(default=False)
    code    = models.CharField(max_length=5)
    name    = models.CharField(max_length=32)
    ename   = models.CharField(max_length=32)
    master  = models.CharField(max_length=32)
    target = models.CharField(max_length=8, choices=TARGET)
    cID     = models.IntegerField()
    
    data = {}       #only used for statistical data storage in views

# Create your models here.
class LanguageStatistic(models.Model):
    def __unicode__(self):              # __unicode__ on Python 2
        return "{} / {} / {} / {} / {} / {} / {} / {} / {} / {}".format(self.date,self.lang,self.type,self.target, self.total, self.count, self.speed, self.totalSecs, self.countSecs, self.speedSecs)
        
    TYPE = (
        ('C', 'Crowdin'),
        ('D', 'Dubbed'),
        ('S', 'Subtitled'),
    )
    TARGET = (
        ('T', 'Test'),
        ('L', 'Live'),
        ('R', 'Rockstar'),
    )
    lang = models.CharField(max_length=5)
    date = models.DateField('date')
    type = models.CharField(max_length=1, choices=TYPE)
    target = models.CharField(max_length=1, choices=TARGET)
    total = models.IntegerField(default=0)
    count = models.IntegerField(default=0)
    speed = models.IntegerField(default=0)
    totalSecs = models.IntegerField(default=0)  #Seconds or Words
    countSecs  = models.IntegerField(default=0)  #Seconds or Words
    speedSecs = models.IntegerField(default=0)  #Speed in Seconds or Words / last 30 days
    totalStrings  = models.IntegerField(default=0)  #Strings
    countStrings   = models.IntegerField(default=0)  #Strings
    speedStrings  = models.IntegerField(default=0)  #Speed in Strings / last 30 days
    
    def calculateSpeed(self):
        import datetime
        #from datetime import datetime, timedelta
        #print(self.date)
        monthAgo = self.date - datetime.timedelta(days=30)
        #print(monthAgo)
        try:   
            oldStat = LanguageStatistic.objects.get(lang=self.lang,type=self.type,date=monthAgo)
            self.speed          = self.count - oldStat.count
            self.speedSecs      = self.countSecs - oldStat.countSecs        
            self.speedStrings   = self.countStrings - oldStat.countStrings
        except LanguageStatistic.DoesNotExist:
            self.speed          = 0
            self.speedSecs      = 0        
            self.speedStrings   = 0
            
    def getLeft(self):
        return self.total-self.count
        
    def getLeftString(self):
        return self.totalStrings - self.countStrings
        
    def getPercent(self):
        if (self.totalSecs > 0):
            return self.countSecs/self.totalSecs
        else:
            return 1
    
class Subtitle(models.Model):
    def __unicode__(self):              # __unicode__ on Python 2
        return u"{}:{}/{}/{}/{}/{}".format(self.title,self.amaraID,self.lang,self.percentDone,self.lines, self.author)

    created             = models.DateTimeField(default=timezone.now())
    amaraID             = models.CharField(db_index=True,max_length=16)
    lang                = models.CharField(db_index=True,max_length=5) # can be de_CH
    title               = models.CharField(max_length=256)
    author              = models.CharField(max_length=32)
    origLines           = models.IntegerField()
    lines               = models.IntegerField()
    completion          = models.BooleanField(default=False)
    percentDone         = models.FloatField()
    data                = JSONField()
    infoData            = JSONField()

    def isComplete(self):
        """ Considers a subtitle as complete if amara has subtitles_complete and subtitles_count > 0.75 of english """
        if (self.completion and self.percentDone > 0.75):
            return True
        else:
            return False

    def hasSubtitle(self):
        return self.isComplete()
            
    def Count(self):
        return self.lines
        
    def OrigCount(self):
        return self.origLines

DEFAULT_TRANSLATOR_ID = 1        
class Video(models.Model):
    def __str__(self):              # __unicode__ on Python 2
        return self.TITLE

    # Check if the video has been dubbed for language lang    
    def isDubbed(self,lang):
        if ( len(getattr(self,lang.master)) > 0 ):
            return True
        else:
            return False
    
    def loadSubtitle(self,lang):
        try:
            self.subtitle = Subtitle.objects.get(amaraID=self.AMARA_ID,lang=lang.code)
        except Subtitle.DoesNotExist:
            self.subtitle = Subtitle(origLines=0,lines=0,percentDone=0)

    def getTranslatedTitle(self):
        title = self.subtitle.title
        return title if (title <> "") else self.TITLE
     
    def subtitleComplete(self):
        return self.subtitle.isComplete()
        
    def subtitleCount(self):
        return self.subtitle.OrigCount()
        
    def subtitleTranslatedCount(self):
        return self.subtitle.Count()
        
    def subtitlePercentDone(self):
        return self.subtitle.percentDone
        
    def getYoutubeID(self,lang):
        return getattr(self,lang.master)
    
    def getAuthor(self,lang):
        if(lang.code == "de"):
            if (str(self.deTranslator) == 'admin'):
                if(self.isDubbed(lang)):
                    return 'unknown'
                else:
                    return self.subtitle.author
            else:
                return self.deTranslator
        else:
            if (self.isDubbed(lang)):
                return "unknown"
            else:
                return self.subtitle.author
        
    subtitle = {}
    
    deTranslator        = models.ForeignKey(User,default=DEFAULT_TRANSLATOR_ID)
    amaraOK             = models.BooleanField(default=False)
    showsExercise       = models.BooleanField(default=False)
    SERIAL              = models.IntegerField()
    DATE_ADDED          = models.DateField('Updated')
    DATE_CREATED        = models.DateField('Date')
    TITLE               = models.CharField(max_length=128)
    LICENSE             = models.CharField(max_length=32)
    DOMAIN              = models.CharField(max_length=32)
    SUBJECT             = models.CharField(max_length=64)
    TOPIC               = models.CharField(max_length=256)
    TUTORIAL            = models.CharField(max_length=256)
    TITLE_ID            = models.CharField(max_length=256)
    DURATION            = models.IntegerField()
    URL                 = models.CharField(max_length=256)
    AMARA_ID            = models.CharField(db_index=True,max_length=16,blank=True)
    REQUIRED_FOR        = models.CharField(db_index=True,max_length=32)
    TRANSCRIPT          = models.CharField(max_length=1)
    ENGLISH             = models.CharField(max_length=16,blank=True)
    ARABIC              = models.CharField(max_length=16,blank=True)
    ARMENIAN            = models.CharField(max_length=16,blank=True)
    BAHASA_INDONESIA    = models.CharField(max_length=16,blank=True)
    BANGLA              = models.CharField(max_length=16,blank=True)
    BULGARIAN           = models.CharField(max_length=16,blank=True)
    CHINESE             = models.CharField(max_length=16,blank=True)
    CZECH               = models.CharField(max_length=16,blank=True)
    DANISH              = models.CharField(max_length=16,blank=True)
    DARI                = models.CharField(max_length=16,blank=True,default='')    
    DEUTSCH             = models.CharField(max_length=16,blank=True)
    ESPANOL             = models.CharField(max_length=16,blank=True)
    FARSI               = models.CharField(max_length=16,blank=True)
    FRANCAIS            = models.CharField(max_length=16,blank=True)
    GREEK               = models.CharField(max_length=16,blank=True)
    HEBREW              = models.CharField(max_length=16,blank=True)
    ITALIANO            = models.CharField(max_length=16,blank=True)
    JAPANESE            = models.CharField(max_length=16,blank=True)
    KISWAHILI           = models.CharField(max_length=16,blank=True)
    KOREAN              = models.CharField(max_length=16,blank=True)
    MONGOLIAN           = models.CharField(max_length=16,blank=True)
    NEDERLANDS          = models.CharField(max_length=16,blank=True)
    NEPALI              = models.CharField(max_length=16,blank=True)
    NORSK               = models.CharField(max_length=16,blank=True)
    POLISH              = models.CharField(max_length=16,blank=True)
    PORTUGUES           = models.CharField(max_length=16,blank=True)
    PORTUGAL_PORTUGUES  = models.CharField(max_length=16,blank=True)
    PUNJABI             = models.CharField(max_length=16,blank=True)
    RUSSIAN             = models.CharField(max_length=16,blank=True)
    SERBIAN             = models.CharField(max_length=16,blank=True)
    SINDHI              = models.CharField(max_length=16,blank=True)
    SINHALA             = models.CharField(max_length=16,blank=True)
    TAMIL               = models.CharField(max_length=16,blank=True)
    TELUGU              = models.CharField(max_length=16,blank=True)
    THAI                = models.CharField(max_length=16,blank=True)
    TURKCE              = models.CharField(max_length=16,blank=True)
    UKRAINIAN           = models.CharField(max_length=16,blank=True)
    URDU                = models.CharField(max_length=16,blank=True)
    XHOSA               = models.CharField(max_length=16,blank=True)
    ZULU                = models.CharField(max_length=64,blank=True)
                 