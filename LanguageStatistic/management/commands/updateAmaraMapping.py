import httplib
import urllib
import json

from time import time
from Queue import Queue
from threading import Thread

from django.core.management.base import BaseCommand, CommandError
from LanguageStatistic.models import Video, Subtitle
from LanguageStatistic import utils

q = Queue()

class MappingGetter(Thread):
    def __init__(self, errors):
        Thread.__init__(self)
        self.errors = errors
        self.conn = utils.get_conn()
        self.daemon = True
        self.start()
        
    def run(self):
        while True:
            ytid = q.get()
            self.lookupAmaraID(ytid)
            q.task_done()
            
    def lookupAmaraID(self, ytid):
        amid = None
        yt = "http://www.youtube.com/watch?v=" + ytid
        query = "/api2/partners/videos/?{}"
        query = query.format(urllib.urlencode({'video_url': yt}))
        #print("loading " + query)
        doc = utils.get_response_json(self.conn, query)
        #print(doc)
        try:
            amid = doc["objects"][0]["id"]
        except:
            if ytid in self.errors["mappings"]:
                amid = self.errors["mappings"][ytid]["amid"]
                print("ERROR CORRECTED - ytid: %s, amid: %s", ytid, amid)
            else:
                print("ERROR - ytid: {}".format(ytid))
        #if there is an amaraID update the database        
        if amid:
            #Store AmaraID in Video Object
            video  = Video.objects.get(ENGLISH = ytid)
            video.AMARA_ID = amid
            video.save()
            #Store the subtitle info in Subtitles
            

class Command(BaseCommand):
    #args = '<poll_id poll_id ...>'
    #help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        tstart = time()
        self.stdout.write('Update Mapping to AmaraIDs "%s"')
        
        #define # of threads
        pool_size = int(10)
        
        #errors = utils.load_json("{}{}".format(dir_data, filename))
        errors = { 'mappings': {} }
        
        #load all videos with a youtube_id
        #videos = db.video_list.find({}, {"youtube_id": True })
        videos = Video.objects.exclude(ENGLISH__isnull=True).exclude(ENGLISH__exact='')
        
        [MappingGetter(errors) for i in range(pool_size)]
        
        for video in videos:
            q.put(video.ENGLISH)
            #if not db.video_mappings.find_one({"_id": ytid}):
            
        q.join()
        #logger.info(utils.check_time("mapping", tstart))
        