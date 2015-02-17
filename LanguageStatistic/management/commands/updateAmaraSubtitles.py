from __future__ import unicode_literals
import sys
import json
from datetime import datetime
from time import time
from Queue import Queue
from threading import Thread

from django.utils.timezone import make_aware, get_default_timezone
from django.utils import timezone
from django.core.management.base import BaseCommand, CommandError
from LanguageStatistic.models import Video, Subtitle, Language
from LanguageStatistic import utils
import operator
from django.db.models import Q

q = Queue()
languages = Language.objects.filter(enabled=True)
loadSubtitleStrings = False
loadSubtitleInfo    = True

class Command(BaseCommand):
    help = 'loads Subtitle information for all videos from Amara, very long running process'
    def handle(self, *args, **options):

        fstart = time()
        pool_size = int(2)
        
        [SubGetter() for i in range(pool_size)]

        updateAll = False
        amaraIDs = []
        for arg in args:
            if (arg == 'all'):
                updateAll = True
            else:
                amaraIDs.append(Q(AMARA_ID=arg))
                
        #Create a Queue of all Videos where we want to load subtitles
        videos = Video.objects.exclude(AMARA_ID__isnull=True)
        if (len(amaraIDs)>0):
            videos = videos.filter(reduce(operator.or_, amaraIDs))
                    
        #if (not updateAll):
        #    videos = videos.filter(amaraOK = False)
        
        print("Updating {} subtitles ...".format(videos.count()))
        [q.put(video) for video in videos]

        q.join()
        
        print( "finished after " + utils.ftime(time() - fstart) )

# Load Subtitles for one Videos for all enabled Languages
class SubGetter(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.conn = utils.get_conn()
        self.loadSubtitleStrings = loadSubtitleStrings
        self.loadSubtitleInfo = loadSubtitleInfo
        
        self.daemon = True
        self.start()

    # This is executed once for every video which has an AMARA_ID
    def run(self):
        while True:
            try:
                self.video = q.get()
                #double check AMARA_ID is not empty
                if (self.video.AMARA_ID <> ""):
                    #Load General Subtitle Data
                    doc = self.getAmaraSubtitleInfo()
                    # Update the Data for English
                    enObj = self.getAmaraSubtitles('en',doc)
                    # Update the Data for all enabled Languages
                    for lang in languages:
                        self.getAmaraSubtitles(lang.code,doc)
                        #Load the actual subtitle SRT File
                        #self.do_srt(amid, langid)
                        
                self.video.amaraOK = True
                self.video.save()
                q.task_done()
            except:
                print(sys.exc_info())

    def getAmaraSubtitleInfo(self):
    
        query = "https://www.amara.org/api2/partners/videos/{}/languages/"
        query = query.format(self.video.AMARA_ID)
        self.lines = 0
        self.origLines = 0
        self.infoData = {}
        
        #Load data from Amara API
        try:
            #print('query {}'.format(self.video.AMARA_ID))
            doc = utils.get_response_json(self.conn, query)
            return doc
        except:
            message = "JSON problem on loadInfo {} - {}"
            print(message.format(self.video.AMARA_ID, sys.exc_info()[0]))
            
    def getAmaraSubtitles(self, langid, doc):
        query = "/api2/partners/videos/{}/languages/{}/subtitles/?format=json"
        query = query.format(self.video.AMARA_ID,langid)
        infoData = ''
        lines = 0
        title = ''
        author = ''
        completion = False
        created = timezone.now()
        
        if ("objects" in doc):
            #iterate over all language objects
            
            for obj in doc["objects"]:           
                if ( obj["language_code"] == langid.lower() ):
                        
                    lines    = obj["subtitle_count"]
                    infoData = obj
                    completion = obj["subtitles_complete"]
                    title    = obj["title"]
                    # Author is the author of the last change
                    author   = obj["versions"][0]['author'] if (obj["num_versions"] > 0) else ''
                    
                    try:
                        created  = make_aware(datetime.strptime(obj["created"], "%Y-%m-%dT%H:%M:%S"), get_default_timezone())
                    except ValidationError:
                        created   = timezone.now()
        
        # load existing object or create new Subtitle Object
        try:
            cc = Subtitle.objects.get(amaraID=self.video.AMARA_ID,lang=langid)
        except Subtitle.DoesNotExist:
            cc = Subtitle(amaraID=self.video.AMARA_ID,lang=langid,completion=completion,percentDone=0)
        
        #update subtitle object
        cc.origLines=self.origLines
        cc.lines=lines
        cc.infoData=infoData
        cc.title = title
        cc.author = author
        cc.created = created
          
        if (self.loadSubtitleStrings):
            try:
                ddoc = utils.get_response_json(self.conn, query)
                #Count number of lines ignoring empty ones
                cc.lines = self.getLines(ddoc["subtitles"])
                cc.data = ddoc
                if (cc.title == '' ):
                    cc.title = ddoc['title']
            except:
                message = "JSON problem on loadCC {}/{} - {}"
                print(message.format(self.video.AMARA_ID, langid, sys.exc_info()[0]))

        if langid == 'en':
            self.origLines = cc.lines
            
        cc.origLines   = self.origLines
        if ( cc.origLines > 0 ):
            cc.percentDone = min(1,float(cc.lines) / float(cc.origLines))
        else:
            cc.percentDone = 0
            
        cc.completion  = True if (completion or (cc.origLines > 0 and cc.lines >= cc.origLines)) else False
        
        cc.save()
            
    def do_srt(self, amid, langid):
        query = "/api2/partners/videos/{}/languages/{}/subtitles/?format=srt"
        query = query.format(amid, langid)
        logger.debug("Query: {}".format(query))
        response = utils.get_response(self.conn, query)
        doc = {"_id": amid, "srt": response}
        self.db.video_subtitles_srt.insert(doc)
        filename = "{}{}-{}.srt".format(dir_pages_srt, amid, lang)
        utils.save_text_binary(filename, response.encode('utf8'))

    def getLines(self, subtitles):
        return sum([1 for item in subtitles if item["text"] != ""])


