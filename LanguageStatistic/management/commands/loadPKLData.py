from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from LanguageStatistic.models import LanguageStatistic,Language
from LanguageStatistic import utils
import sys
import pickle
import os.path
import time
import datetime
from datetime import datetime

trgt = {'Test' : 'T',
        'Live' : 'L',
        'Rockstar' : 'R' }

# Management Command to import Data from PKL files, this was used for the migration to mysql db and django
# and can be deleted in the future
class Command(BaseCommand):
    #args = ''
    help = 'Import Language Statistic history from PKL files to MySQL DB (Django Models)'
    
    def handle(self, *args, **options):
        #find out correct path to .pklfiles
        path = '/home/alani/KA/'
        #load languages array from DB file
        languages = Language.objects.filter(enabled=True)
        
        #for each language load pkl file, create LanguageStatistic
        for lang in languages:
            if ( len(args) == 0 or lang.ename in args):
                print(lang.name)
                self.loadPKLData(lang)
        
    def loadPKLData(self,lang):
        import datetime
        today = datetime.date.today()    
        localDirectory  = settings.LOCALDIRECTORY
        #Load Data from pickle File
        data = []
        pklFilename = localDirectory+"burnDownData-"+lang.code+".pkl"
        if os.path.exists(pklFilename):
            pkl_file = open(pklFilename, 'rb')
            data = pickle.load(pkl_file)
            pkl_file.close()         
            #find entry with same date (delete)
            found=False
            delete = 0
            for d in data:
                if (d[0] == str(today)):
                    found=True
                    delete = d

            if found:
                data.remove(delete)    
            #                                      Words/Seconds             Strings
            for row in data:  #date,            Total/Left/Speed        Total/Left/Speed
               print(row)
               date = row[0]
               crowdinLeftWords   = row[1]
               subVideoLeftString = row[2]
               dubVideoLeftString = row[3]
               subVideoLeftSeconds = row[4]
               dubVideoLeftSeconds = row[5]
               crowdinPercent  = row[6]
               subVideoPercent = row[7]
               dubVideoPercent = row[8]

               self.createStatObject(date,lang, 'C', crowdinLeftWords, crowdinPercent, crowdinLeftWords / 33 )     
               self.createStatObject(date,lang, 'S', subVideoLeftSeconds, subVideoPercent,  subVideoLeftString )
               self.createStatObject(date,lang, 'D', dubVideoLeftSeconds, dubVideoPercent,  dubVideoLeftString )

    def createStatObject(self, date, lang, type, leftSecs, percent, leftString):
        if ( date > '2014-12-08' ):
            #print('Percent'+percent)
            dt = created  = datetime.strptime(date, "%Y-%m-%d")
            try:   
                ls = LanguageStatistic.objects.get(date=dt,lang=lang.code,target=trgt[lang.target],type=type)            
                print("LS Object found, updating")
            except LanguageStatistic.DoesNotExist:
                ls = LanguageStatistic(date=dt,lang=lang.code,target=trgt[lang.target],type=type)
                ls.total            = 0
                ls.count            = 0
            
            if (percent < 1 ):
                ls.totalSecs        = leftSecs / (1-percent)
                
            ls.countSecs        = ls.totalSecs - leftSecs
            
            if (percent < 1 ):
                ls.totalStrings     = leftString / (1-percent)
            ls.leftStrings      = leftString
            
            ls.calculateSpeed()
            
            
            
            ls.save()