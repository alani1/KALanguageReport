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
from datetime import datetime
from time import time

class Command(BaseCommand):
    #args = '<poll_id poll_id ...>'
    help = 'Load the Khan Academy Masterlist into our Database'
    
    def handle(self, *args, **options):
        fstart = time()
        #logger = utils.get_logger("spreadsheet")
        #dir_data = config["paths"]["dir_data"]
        
        #ID of Google Doc for Masterlist, update every month when new Masterlist is published
        key = "1ir94UxXHbxd78pgfGgCiotEN44NDKGNceHlWPk66D8Q"
        key = "135EvaTE4u0cdiNJvdxXQLNmw1zPzjUqyfSIhmvrJf8M"
        gid = 0
        doc = self.load_doc(key, gid)
        #Below line could be used to load a file which corrects mapping errors
        #errors = utils.load_json("{}{}".format(dir_data, "mapping-errors.json"))
        
        #delete all videos
        #Video.objects.all().delete()
        updatedVideoCount = 0
        newVideoCount = 0
        
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
                    
            except Video.DoesNotExist:
                newVideoCount = newVideoCount + 1
                print("New Video created for " + videoData["TITLE_ID"])
                v = Video(**videoData)
                
            v.save()

        print( "%s Videos updated".format(updatedVideoCount))
        print( "%s new Videos added".format(newVideoCount))
        print( "finished after " + ftime( fstart - time()) )

    def load_doc(self, key, gid):
        doc = utils.get_google_csv(key, gid)
        #ignore the first x lines
        doc = [s for idx, s in enumerate(doc.splitlines()) if idx >= 1]
        #print(doc)
        reader = csv.DictReader(doc)
            
        return reader

    def fixVideoData(self,video):
            ytid_en = video["ENGLISH"]
            #if ytid_en in errors["ids"]:
            #    video["ytid_en"] = errors["ids"][ytid_en]["ytid"]
            #video["_id"] = video["ytid_en"]
            #print(video)
            video["DATE_CREATED"] = datetime.strptime(video.pop("DATE CREATED"), "%m/%d/%Y").date()
            video["DATE_ADDED"] = datetime.strptime(video.pop("DATE ADDED"), "%m/%d/%Y").date()
            video["SERIAL"] = int(video["SERIAL"])
            video["AMARA_ID"] = video.pop("AMARA ID")
            video["TUTORIAL"] = video["TUTORIAL"]
            video["DURATION"] = int(video["DURATION"]) if video["DURATION"] <> '' else 0
            video["TITLE_ID"] = video.pop("TITLE ID")
            #video["TRANSCRIPT"] = video.pop("TRANSCRIPT?")
            video["BAHASA_INDONESIA"] = video.pop("BAHASA INDONESIA")
            video["REQUIRED_FOR"] = video.pop("REQUIRED FOR")
            video["PORTUGAL_PORTUGUES"] = video.pop("PORTUGAL PORTUGUES") 
            video["TRANSCRIPT"] = 'Y' if video["TRANSCRIPT"] == 'Y' else 'N'
