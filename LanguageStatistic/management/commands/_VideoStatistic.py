"""VideoStatistic Module


"""
from __future__ import unicode_literals
from LanguageStatistic.models import Video,Subtitle,Language,LanguageStatistic
from django.template.defaultfilters import slugify
import datetime
from LanguageStatistic import utils
from LanguageStatistic.utils import ftime

trgt = {'Test' : 'T',
        'Live' : 'L',
        'Rockstar' : 'R' }

class VideoStatistic:

    #is this dub or subtitle statistic
    dub = False
    lang = {}
    StatisticTable = ""
    Percent = 0
    Left = ''
    LeftString = 0
    Total = ''
    
    missingVideos = []
    doneVideos = []
    allVideos = []
    
    def generateMissingVideoTable(self,lang):
        return self.generateTable(" - Missing",lang,True)
        
    def generateCompletedVideoTable(self,lang):
        return self.generateTable(" - Done",lang,False)
    
    def generateMenu(self,menuItems):
        subject = ''
        
        #videos = sorted(self.doneVideos + self.missingVideos, key=lambda v: v.SUBJECT)
        videos = self.allVideos
        #menuItems = []
        for v in videos:
            if (subject != v.SUBJECT):
                menuItems.append([slugify(v.SUBJECT),v.SUBJECT])
                subject = v.SUBJECT
                

        return menuItems
        
    # Generate summary table of video categories on the VideoList Page
    # lang link to english or translated video    
    def generateTable(self,status,lang,missing):
        lineCount = 0
        total = 0
        subject = ""
        topic = ""
        tutorial = ""
        videos = {}
        
        if missing:
            videos = self.missingVideos
        else:
            videos = self.doneVideos
    
        #print("calling generateVideosTable" + self.title + status + str(len(videos) ))
    
        html = '<h1>'+self.title+status+'</h1>'
        html += '<table id="keywords" class="sort" cellspacing="0" cellpadding="0">'
        html += "<thead><th class='lalign'>Subject</th><th class='lalign'>Title</th><th>Length</th><th>Subtitles<th></thead>"
    
        #print ( "length of videos : " + str(len(videos)))
        for v in videos:
        
            if (subject != v.SUBJECT):
                subject = v.SUBJECT
                idTag=' id="'+slugify(subject)+'"'
            else:
                idTag=''
            
            if (topic != v.TOPIC):
                topic = v.TOPIC
                    
            #every new Tutorial we output a title
            if (tutorial != v.TUTORIAL):
                tutorial = v.TUTORIAL
                #link = u"<a href='https://translate.khanacademy.org/{}/{}/{}/' >{}</a>".format(v.DOMAIN,v.SUBJECT,v.TOPIC,tutorial,tutorial)
                html += u"<tr><td class='lalign' {2}>{0}</td><td class='lalign'><b>{1}</b></td></tr>".format(subject,tutorial,idTag)
                    
            #Link to amara if video needs to be subtitled and amaraID exists
            amaraURL = "http://www.amara.org/"+self.lang.code+"/subtitles/editor/{0}/"+self.lang.code+"/"

            #Create URL for link to Youtube, if we have a translated version, take this else the English version
            if (v.isDubbed(self.lang)):
                url = "'http://www.youtube.com/watch?v=" + v.getYoutubeID(self.lang) +"'"
                #TODO find Language translation of title (eventually take from amara)
                #title = self.lang.code+": "+ v.TITLE;
                title = v.getTranslatedTitle()
                title = title if (title <> "") else v.TITLE
                cssClass = "dub"
            else:
                url = "'http://www.youtube.com/watch?v={}&hl={}'".format(v.ENGLISH,self.lang.code)
                cssClass = "sub"
                title = v.TITLE
        
            link = u"<a target='_blank' href={0} class='{2}'>{1}</a>".format(url,title,cssClass)
            
            
            cc = u"<a target='_blank' title='{0} of {1} subtitles by {2}' href={3}>{4:7.2f} %</a>".format(
                v.subtitleTranslatedCount(), v.subtitleCount(), v.subtitle.author, amaraURL.format(v.AMARA_ID), v.subtitlePercentDone()*100, cssClass )
            
            html += "<tr><td class='lalign'>"+v.SUBJECT+"</td><td class='lalign'>"+link+"</td><td>"+ftime(int(v.DURATION))+"</td><td>"+cc+"</td></tr>"
            lineCount +=1
            total += int(v.DURATION)

        html += "<tr class='total'><td class='lalign'>Total</td><td></td><td>"+ftime(total)+"</td></tr>"
        html += "</table>"
        return html
    
    
    # Format one single row in the Category Table
    def formatRow(self,dub,subject,subjectCount,subjectSecs,dubbedCount,dubbedSecs,subCount,subSecs,lineCount):
        if (dub):
            done = float(dubbedSecs) / subjectSecs * 100 if subjectSecs > 0 else 0
            dubbed = '<a target="_blank" href="./{3}SiteDoneVideos.html#{0}">{1} / {2}</a>'.format(subject,dubbedCount,ftime(dubbedSecs),self.target)
            subtitled = str(subCount) + " / " + ftime(subSecs)
        else:
            done = float(subSecs+dubbedSecs) / subjectSecs * 100  if subjectSecs > 0 else 0
            dubbed = str(dubbedCount) + " / " + ftime(dubbedSecs)
            subtitled = '<a target="_blank" href="./{3}SiteDoneVideos.html#{0}">{1} / {2}</a>'.format(subject,subCount,ftime(subSecs),self.target)
        
        link = '<a target="_blank" href="./{1}SiteMissingVideos.html#{0}">{0}</a>'.format(subject,self.target)
    
        oddeven = 'odd' if (lineCount % 2) == 0 else 'even'
        return "<tr class='{6}'><td class='lalign'>{0}</td><td>{1} / {2}</td><td>{3}</td><td>{4}</td><td>{5:7.2f} %</td></tr>".format(link, subjectCount, ftime(subjectSecs), dubbed, subtitled, done, oddeven )
    
    # Check the Status and return a HTML Table of all videos in the collection videos
    # dub is a boolean and indicates if the videos should be dubbed or just subtitled    
    def prepareStatistics(self):
    
        videos = self.videoList
    
        lineCount =0
        totalCount=0
        totalSecs=0
        totalDubbedCount=0
        totalDubbedSecs=0
        totalSubCount=0
        totalSubSecs=0    
        subjectCount=0
        subjectSecs=0
        subjectStrings=0
        dubbedCount=0
        dubbedSecs=0
        subCount=0
        subSecs=0                   
        subject=""
        left = 0.0
        missingCC=0
        totalStrings=0
    
        #print("verifyVideoStatus called " + self.title)
    
        if (self.dub):
            nameTag = 'missingVideos'
        else:
            nameTag = 'missingSubtitles'
            
        output = '<a name="'+nameTag+'"></a><h1>'+self.title+'</h1>'
        output += '<table id="keywords" class="sort" cellspacing="0" cellpadding="0">'
        output += "<thead><th class='lalign'></th><th><span>Total</span></th><th><span>Dubbed</span></th><th><span>Subtitles</span></th><th><span>% Done</span></th></thead>"
        
        # Iterate of all Videos in list of required videos
        for v in videos:
            #subject changed, we start a new subject
            if (subject != v.SUBJECT):
                totalCount += subjectCount
                totalSecs += subjectSecs
                totalStrings += subjectStrings
                totalDubbedCount += dubbedCount
                totalDubbedSecs += dubbedSecs
                totalSubCount += subCount
                totalSubSecs += subSecs    

                if (subjectCount != 0):
                    output += self.formatRow(self.dub,subject,subjectCount,subjectSecs,dubbedCount,dubbedSecs,subCount,subSecs,lineCount)
                    lineCount += 1
                
                subject=v.SUBJECT
                subjectCount=0
                subjectSecs=0
                subjectStrings=0
                dubbedCount=0
                dubbedSecs=0
                subCount=0
                subSecs=0                
            
            #Load the Amara Subtitle information
            v.loadSubtitle(self.lang)
            
            subjectCount += 1
            subjectSecs += int(v.DURATION)            
            subjectStrings += v.subtitleCount()
            
            #verify for every Video if Subtitles are available in our language
            #Check if CSV file shows a Dubbed Video for Language
            self.allVideos.append(v)
            if ( v.isDubbed(self.lang) ):
                dubbedCount += 1
                dubbedSecs += int(v.DURATION)
                self.doneVideos.append(v)
            else:
                if(v.subtitleComplete()):
                    subCount += 1
                    subSecs += int(v.DURATION)   
                    
                    if (self.dub):
                        self.missingVideos.append(v)
                    else:
                        self.doneVideos.append(v)
                else:                  
                    missingCC += v.subtitleCount()
                    self.missingVideos.append(v)

        
        #count the last subject
        totalCount += subjectCount
        totalSecs += subjectSecs
        totalStrings += subjectStrings
        
        totalDubbedCount += dubbedCount
        totalDubbedSecs += dubbedSecs
        totalSubCount += subCount
        totalSubSecs += subSecs 
    
        if (subjectSecs == 0 ):
            print("Error: " + subject)
    
        output += self.formatRow(self.dub,subject,subjectCount,subjectSecs,dubbedCount,dubbedSecs,subCount,subSecs,lineCount)
    
        if (self.dub):
            done = float(totalDubbedSecs) / totalSecs if totalSecs > 0 else 0
        else:
            done = float(totalDubbedSecs+totalSubSecs) / totalSecs if totalSecs > 0 else 0
            
        output += "<tr class='total'><td class='lalign'>{0}</td><td>{1} / {2}</td><td>{3} / {4}</td><td>{5} / {6}</td><td>{7:7.2f} %</td></tr>".format("Total", totalCount, ftime(totalSecs), totalDubbedCount, ftime(totalDubbedSecs), totalSubCount, ftime(totalSubSecs), done*100)
        output += "</table>"
            
        if (self.dub):
            left = (totalSecs-totalDubbedSecs)
            output += "<p>{0} left to be dubbed</p>".format(ftime(left))
        else:
            left = (totalSecs-totalDubbedSecs-totalSubSecs)
            output += "<p>{0} left to be subtitled</p>".format(ftime(left))          
    
        #print ( "length of done videos : " + str(len(self.doneVideos)))
        #print ( "length of missing videos : " + str(len(self.missingVideos)))
        
        import datetime
        today    = datetime.date.today()
        type  = 'D' if (self.dub) else 'S'
        try:
            stat= LanguageStatistic.objects.get(lang=self.lang.code,type=type,date=today)
        except LanguageStatistic.DoesNotExist:
            stat = LanguageStatistic(lang=self.lang.code,target=trgt[self.lang.target],type=type,date=today)        
        
        stat.total          = len(self.doneVideos)+len(self.missingVideos)
        stat.count          = len(self.doneVideos)
        stat.totalSecs      = totalSecs
        stat.countSecs      = totalSecs - left
                
        stat.totalStrings   = totalStrings
        stat.countStrings   = totalStrings - missingCC

        stat.calculateSpeed()

        stat.save()        
        
        #can be removed later
        self.TotalStrings = totalStrings
        self.Total = ftime(totalSecs)
        self.Percent = done
        self.Left = left
        self.LeftString = missingCC
        self.StatisticTable = output
    
    def getActivity(self):
        from django.db.models import Count
        from django.db.models import Sum
        
        today = datetime.date.today()
        thirty_days_ago = today - datetime.timedelta(days=30)
        
        ##subtitles = Subtitle.objects.filter(lang=self.lang.code).filter(created__gte=thirty_days_ago).filter(lines__gt=0)
        ##subtitles.values('author', ).annotate(total=Sum('lines')).
        ## I am too stupid for Djangos values stuff fallback to normal sql
        sql = "SELECT `author`, COUNT(amaraID) as videos, SUM(`lines`) as ccLines, SUM(DURATION) as time FROM `LanguageStatistic_subtitle`, LanguageStatistic_video WHERE LanguageStatistic_subtitle.amaraID = LanguageStatistic_video.AMARA_ID and lang='{}' and `lines`> 0 and created > '{}' and author <> '' group by author order by time DESC".format(self.lang.code,thirty_days_ago)

        import time
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute(sql)
        subtitles = cursor.fetchall()
        
        vTot = 0
        sTot = 0
        tTot = 0
        a = []
        for s in subtitles:
            vTot = vTot + s[1]
            tTot = tTot + s[2]
            sTot = sTot + s[1]
            a.append(s)

        a.append( ('Total', vTot,tTot,sTot))
        return a
        
    
    def __init__(self,dub):
        self.dub = dub
        self.missingVideos = []
        self.doneVideos = []
    
    #Changes the Language which means we also have to change the set of required videos
    #because each language can have differnt Target
    def setLang(self,lang):
        self.missingVideos = []
        self.doneVideos = []
        
        self.lang = lang
        self.target = lang.target
        
        if ( self.dub ):
            self.title = "Videos to be dubbed"
            self.videoList = self.getVideosDubbed(self.target)
        else:
            self.title = "Videos to be subtitled"
            self.videoList = self.getVideosSubtitled(self.target)       
        
    #return list of videos to be dubbed for specified target platform
    def getVideosDubbed(self,target):
        videos = Video.objects.filter(REQUIRED_FOR='Test platform (dubbed)')    
        return videos

    #return list of videos to be subtitled for specified target platform
    def getVideosSubtitled(self,target):

        videos = Video.objects.all()
        
        if ( target == "Test" ):
        
            videos = videos.filter(REQUIRED_FOR="Test platform")
        elif ( target == "Live" ):
        
            videos = videos.filter(REQUIRED_FOR="Test platform")
        #elif ( target == "Rockstar" ):
        #    return __videosTestSubtitled + __videosLive + __videosRockstar
        
        return videos