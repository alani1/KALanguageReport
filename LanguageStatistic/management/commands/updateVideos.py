from __future__ import unicode_literals
from django.core.management.base import BaseCommand, CommandError
from LanguageStatistic.models import Video
from LanguageStatistic.models import Subtitle
from LanguageStatistic.models import Language
from datetime import datetime
from time import time
import sys
import json
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2

class Command(BaseCommand):
    #args = '<poll_id poll_id ...>'
    help = 'Load the Khan Academy Masterlist into our Database'
    mode = ""
    
    def handle(self, *args, **options):
        fstart = time()
        
        self.isDubbedCount = 0
        self.isSubbedCount = 0
        self.isMissingCount = 0
        self.isDubbedNotUpdatedCount = 0
        
        self.lang = Language.objects.get(master="DEUTSCH")
        print(self.lang)
        
        #TODO
        #Verify Status of all Videos in Database with KA API
        #self.updateVideoDatabase()
        
        #Update Status for all Videos from Translations Portal
        self.mode = "updateVideoStatus"
        data = self.getAllVideoDataStatus()
        self.processChildren(data);
        
        print( str(self.isDubbedNotUpdatedCount) + " Dubbed Videos not sent to KA")
        print( str(self.isDubbedCount) + " Missing Dubbed Videos")
        print( str(self.isSubbedCount) + " Missing Subbed Videos")
        print( str(self.isMissingCount) + " Missing  Videos")

    def updateVideoDatabase(self):
    
        file = '/home/alani/KATopicTree.json'
        data=open(file).read()
        doc = json.loads(data, encoding="utf-8")        
        
        self.mode = "updateVideoDB"
        self.processChildren(doc)
        
    
    def updateVideoEntry(self,data):
    
        slug = data["slug"]
        videos = Video.objects.filter(TITLE_ID=slug)
        if (len(videos) == 0 ):
            #data = self.getVideoInfo(video)
            #print(data)
            print(slug + " Video not found")
            
            
    #deTranslator, amaraOK, showsExercise
    #SERIAL          creation_date ": "2015-05-13T17:00:23Z",
    #DATE_ADDED      date_added": "2012-08-31T01:17:21Z",
    #DATE_CREATED    
    #TITLE           title
    #LICENSE         duration
    #DOMAIN      e.g. Math from relative_url of topic
    #SUBJECT     ???  early-math
    #TOPIC       ???? cc-early-math-counting-topic
    #TUTORIAL    ???? cc-early-math-counting
    #TITLE_ID    ??? --> slug or readable_id"
    #DURATION            
    #URL                field : "ka_url"
    #AMARA_ID           equal to our Youtube-Englisch ID
    #REQUIRED_FOR       "Test platform" or "Live platform" or "Test platform (dubbed)"
    #TRANSCRIPT         ignore
    #ENGLISH             = models.CharField(max_length=16,blank=True)            
            
            current_revision_key
            
            
            self.isMissingCount += 1
        else: 
            a = 1
 
    def updateVideoStatus(self,slug,dubbed,subbed):
        
        videos = Video.objects.filter(TITLE_ID=slug)
        if (len(videos) == 0 ):
            #data = self.getVideoInfo(video)
            #print(data)
            #print(slug + " Video not found in DB")
            self.isMissingCount += 1
        else:
            video = videos[0]
            
            if (dubbed and not video.isDubbed(self.lang)):
                data = self.getVideoInfo(video)
                #print(data["translatedTitle"])
                print(slug + " Video is dubbed, should update our DB")
                deID = data["translatedYoutubeId"];
                self.isDubbedCount += 1
                video.DEUTSCH = deID
                video.save()
                
            if (not dubbed and video.isDubbed(self.lang)):
                self.isDubbedNotUpdatedCount += 1
                print(video.ENGLISH + "," + video.DEUTSCH + ", " + slug)
            
            if (subbed):
                video.loadSubtitle(self.lang)
                if (subbed and not video.subtitleComplete()):
                    self.isSubbedCount += 1
                    print(slug + " Video has subtitle, should update our DB")
                    if len(video.AMARA_ID) == 0:
                        video.AMARA_ID = video.ENGLISH
                        video.subtitle.amaraID = video.ENGLISH
                        video.save()
                        
                    cc = video.subtitle
                    cc.completion = True
                    cc.save()
                if (not subbed and video.subtitleComplete()):
                    print("Video is marked as subbed but actually not")
                    
            
        
    def processChildren(self,data):
        
        for child in data["children"]:
            slug = child["slug"]
            type = child["content_kind"]
            if (type == "Topic" or type == ""):
                #children = child["children"]
                self.processChildren(child);
            elif (type == "Video"):
                if (self.mode == "updateVideoDB" ):
                    self.updateVideoEntry(child)
                else:
                    self.updateVideoStatus(slug, child["dubbed"], child["subbed"])
        
 
    def doStuff(self):
        for v in videos:
            #v.getYoutubeID("de");
            print(v.TITLE_ID + " " + v.ENGLISH)
            data = self.getVideoInfo(v)
            deID = data["translatedYoutubeId"];
            print(data["translatedTitle"])
                
 
            
    def getVideoInfo(self,v):
        query = "https://www.khanacademy.org/api/internal/videos/{}?lang=de"
        query = query.format(v.ENGLISH)
        
        #Load data from KA
        try:
            response = urllib2.urlopen(query)
            data = response.read().decode('utf-8')
            response.close()
            doc = json.loads(data, encoding="utf-8")
            
            return doc
        except:
            message = "JSON problem on loadInfo {} - {}"
            print("loading" + query)
            print(message.format(v.ENGLISH, sys.exc_info()[0]))
            raise
            
    def getAllVideoDataStatus(self):
        query = "https://www.khanacademy.org/api/internal/translate_now?lang=de"
        
        #Load data from KA
        try:
            response = urllib2.urlopen(query)
            data = response.read().decode('utf-8')
            response.close()
            doc = json.loads(data, encoding="utf-8")
            
            return doc
        except:
            message = "JSON problem on loadInfo {} - {}"
            print("loading" + query)
            print(message.format(v.ENGLISH, sys.exc_info()[0]))
            raise    
    