from __future__ import unicode_literals
from django.core.management.base import BaseCommand, CommandError
from django.utils.timezone import make_aware, get_default_timezone
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.mail import send_mail

from LanguageStatistic.models import Video
from LanguageStatistic import utils
from LanguageStatistic.utils import ftime


import os
import csv
import json
import httplib
from datetime import datetime
from time import time

class Command(BaseCommand):
    #args = '<poll_id poll_id ...>'
    help = 'Load the Khan Academy Masterlist into our Database'
    
    def handle(self, *args, **options):
        fstart = time()

        doc = self.load_doc()
        #Below line could be used to load a file which corrects mapping errors
        #errors = utils.load_json("{}{}".format(dir_data, "mapping-errors.json"))
        
        #delete all videos
        #Video.objects.all().delete()
        updatedVideoCount = 0
        newVideoCount = 0
        deleteVideoCount = 0
        
        for videoData in doc:
            #Fix the data from one video
            self.fixVideoData(videoData)
            
            try:               
                v = Video.objects.get(TITLE_ID=videoData["TITLE_ID"])
                
                #UPDATE each field
                for key in videoData:
                    oldValue = getattr(v,key)
                    newValue = videoData[key]
                    if (key=='DATE_ADDED' and newValue>oldValue):
                        updatedVideoCount = updatedVideoCount + 1
                        # Send an email to notify the deTranslator about the update
                        u = User.objects.get(username=v.deTranslator)
                        updateSubject = "KhanAcademy Video {} was updated".format(v.TITLE_ID,newValue,oldValue)
                        updateStr = "KhanAcademy Video {} was updated on {} last version from {}".format(v.TITLE_ID,newValue,oldValue)
                        print(updateStr)
                        print("Sending an email to {}".format(u.email))
                        send_mail(updateSubject, updateStr, 'alain.schaefer@gmail.com',[u.email], fail_silently=False)
                        setattr(v,key,newValue)
                    if (key=='DEUTSCH' and (oldValue <> '' and newValue <> oldValue) ):
                        print("For Video {} the German Version was not updated from {} to {}".format(v.TITLE_ID,oldValue,newValue))
                    else:
                        setattr(v,key,newValue)
            
            #if video not found, create a new one
            except Video.DoesNotExist:
                newVideoCount = newVideoCount + 1
                print("New Video created for " + videoData["TITLE_ID"])
                v = Video(**videoData)
                
            v.save()

        print( "{0} Videos updated".format(updatedVideoCount))
        print( "{0} new Videos added".format(newVideoCount))
        print( "{0} new Videos deleted".format(deleteVideoCount))
        print( "finished after " + ftime( time() - fstart ) )

    def load_doc(self):
    
        query = "/translations/videos/de_all_videos.csv" 
        conn  = httplib.HTTPSConnection("www.khanacademy.org")
        doc   = utils.get_response(conn, query, False)
        
        #ignore the first x lines
        doc = [s for idx, s in enumerate(doc.splitlines()) if idx >= 0]
        #print(doc)
        reader = csv.DictReader(doc)
            
        return reader

    def fixVideoData(self,video):

            #print video
            video["DATE_ADDED"] = datetime.strptime(video.pop("en_date_added"), "%Y-%m-%d").date()
            
            video["DOMAIN"] = video.pop("Domain")
            video["SUBJECT"] = video.pop("Subject")
            video["TOPIC"] = video.pop("Topic")
            video["TUTORIAL"] = video.pop("Tutorial")
            
            video["TRANSCRIPT"] = 'Y' if video.pop("Transcript") == 'Y' else 'N'
            video["ENGLISH"] = video.pop("en")
            video["DEUTSCH"] = video.pop("de")
            video["TITLE"] = video.pop("title")
            video["TITLE_ID"] = video.pop("slug")
            
            video["DURATION"] = int(video["duration"]) if video["duration"] <> '' else 0
            video.pop("duration")
            video["REQUIRED_FOR"] = 'Live platform' if (video['LIVE'] == 'sub or dub' or video['LIVE'] == 'dub') else ''
            video["REQUIRED_FOR"] = 'Test platform (dubbed)' if video['TEST'] == 'dub' else video["REQUIRED_FOR"]
            video["REQUIRED_FOR"] = 'Test platform' if video['TEST'] == 'sub or dub' else video["REQUIRED_FOR"]
            video["SERIAL"] = 0

            video.pop("TEST")
            video.pop("LIVE")
            video.pop("de_date_added")
            