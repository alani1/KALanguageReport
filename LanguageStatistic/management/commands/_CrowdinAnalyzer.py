#import library to do http requests
from __future__ import unicode_literals   
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2

import json
import re
import math
import time
import csv

from LanguageStatistic.models import Video,Subtitle,Language,LanguageStatistic
from LanguageStatistic import utils

trgt = {'Test' : 'T',
        'Live' : 'L',
        'Rockstar' : 'R' }
        
class CrowdinAnalyzer:
    
    velocityString = ""
    StatisticTable = ""
    Percent = 0
    Left = 0
    lang = ''

    targetCategories = []
    crowdinFiles = []
    crowdinInitialized = False

    def __init__(self):
        self.live = []
        
        #open CSV File for CrowdinFiles
        #create dictionaries for test, live and rockStar with all the file names
        #ifile  = open(LocalConfig.localDirectory+'KA-CrowdinFiles.csv')
        doc = utils.get_google_csv('1iwyXMXwshJIJq1aYlWw8wlnKscg3adURBeDXeeQiaZM', '')
        #print(doc)
        #{'directory','file','target','status'}
        doc = [s for idx, s in enumerate(doc.splitlines())]
        reader = csv.DictReader(doc)        
        for row in reader:
            self.crowdinFiles.append(row)
        
        #print(self.crowdinFiles)    
        self.crowdinInitialized = False

    def setLang(self,lang):
        self.lang = lang
        self.setTargetPlatform(lang.target)
        
    def setTargetPlatform(self,target):
        self.target = target
        
    #combine create a dicitionary filename->crowdinID
    def initCrowdinFiles(self,data):
        #empty the crowdinData
        self.crowdinData = {}
        
        for fileId in data:
            crowdinId = fileId[3:]
            #print(data[fileId])
            self.crowdinData[data[fileId]['name']] = data[fileId]
            
        self.crowdinInitialized = True
    
    def inTargetSet(self,potFileTarget):
        
        if potFileTarget == 'Test':
            return True
        elif potFileTarget == 'Live' and self.target <> 'Test':
            return True
        elif potFileTarget == 'Rockstar' and self.target == 'Rockstar':
            return True
        else:
            return False
    
    def prepareStatistics(self,testSite):
        lineCount=0
        #download the file:
        
        response = urllib2.urlopen('https://crowdin.com/project/khanacademy/'+self.lang.code)
    
        #convert to string:
        #data = file.read()
        data = response.read().decode('utf-8')
        #close file because we dont need it anymore:
        response.close()

        #between those two markers we find a json string array
        #PROJECT_FILES
        #DOWNLOAD_PERMISSIONS
        start = data.find('PROJECT_FILES = ') + 16
        end = data.find('DOWNLOAD_PERMISSIONS')-2

        jData = '['+data[start:end]+']'
        project_files = json.loads(jData)
        #if (not self.crowdinInitialized):
        self.initCrowdinFiles(project_files[0])

        totWords = 0
        totLeft = 0
        totApproved = 0

        output = ""
        
        # Iterate over all categories required for current target
        #for cat in self.beta:
        for potFile in self.crowdinFiles:
                  
            if ( self.inTargetSet(potFile['Requirement']) ):
            
                if potFile['Filename'] in self.crowdinData:
                    c = self.crowdinData[potFile['Filename']]
                else:
                    print("Error : " + potFile['Filename'] + " does not exist")
                    continue
                
                fileID = c['id']
                count = int(c['total_count'])
                translated =  int(c['translated'])
                approved = int(c['approved'])
                
                #print( "{3} - total : {0}, translated : {1}, approved: {2}".format(count,translated,approved, c['name']))
                left = count - translated
                totWords = totWords + count
                if( left > 0 ):
                    totLeft = totLeft + left
                    totApproved = totApproved + approved
                    
                    #what is editor_url ???
                    if 'editor_url' in c:
                        url = '<a href="https://crowdin.com/translate{0}" target="_blank">{1}</a>'.format(c['editor_url'],c['name'])
                    else:
                        url = '<a href="https://crowdin.com/translate/khanacademy/{0}/enus-{1}" target="_blank">{2}</a>'.format(fileID,self.lang.code,c['name'])
                        
                    oddeven = 'odd' if (lineCount % 2) == 0 else 'even'
                    output += "<tr class='{0}'><td class='lalign'>{1}</td><td>{2:0.2f} %</td><td>{3}</td><td>{4:0.2f} %</td></tr>".format(oddeven,url,100-(float(left)/count*100),left,float(approved)/count*100)
                    lineCount += 1

        output += "<tr class='total'><td class='lalign'>Total</td><td>{0:0.2f}%</td><td>{1}</td></tr>".format(100-float(totLeft)/totWords*100,totLeft,totApproved)
        output += "</table>"
        output += "<p>{0:0.2f}% done, {1} words left of {2} required to qualify for Test Platform <p/>".format(100-float(totLeft)/totWords*100, totLeft, totWords)
    
        self.UserStatisticTable = self.prepareUserActivity(totLeft)
        
        import datetime
        today = datetime.date.today()
        type  ='C'
        try:
            stat= LanguageStatistic.objects.get(lang=self.lang.code,date=today,type=type)
        except LanguageStatistic.DoesNotExist:
            stat = LanguageStatistic(lang=self.lang.code,target=trgt[self.lang.target],type=type,date=today)        
        
        stat.total          = totWords
        stat.count          = totWords - totLeft
        stat.totalSecs      = totWords
        stat.countSecs      = totWords - totLeft
        stat.totalStrings   = stat.totalSecs / 33
        stat.countStrings   = stat.countSecs / 33

        stat.calculateSpeed()
        
        #Compare calculated Speed to Crowdin Activity and set to lower of the two
        if (stat.speedStrings <> 0):
            stat.speedStrings = min(stat.speedStrings,self.speed)
        else:
            stat.speed          = self.speed * 33
            stat.speedSecs      = self.speed * 33        
            stat.speedStrings   = self.speed
        
            

        stat.save()
        
        self.TotalStrings = totWords
        self.Percent = 1-float(totLeft)/totWords
        self.Left = totLeft 
        self.StatisticTable =  output

    def prepareUserActivity(self,left):
        
        #Now loading the activities
        activityURL = "https://crowdin.com/project_actions/activity_stream?project_id=10880&language_id="+str(self.lang.cID)+"&show_activity="
        file2 = urllib2.urlopen(activityURL)
        activityData = file2.read().decode('utf-8')
        file2.close()

        users = {}
        userObj = {'name':'none','phrase_commented':0,'phrase_suggested':0,'suggestion_deleted':0,'suggestion_voted':0,'suggestion_approved':0,'suggestion_disapproved':0,
        'join_group':0,'pretranslate_suggestion':0,'suggestion_replaced':0,'last':0, 'new_thread':0, 'suggestion_uploaded':0, 'uploaded_suggestion_approved':0}

        activities = json.loads(activityData)      
        
        for act in activities['activity']:      
            uid = act['user_id']
            count = act['count']
            atype = act['type']  #phrase_commented,phrase_suggested,suggestion_deleted,suggestion_voted,suggestion_approved
            msg = act['message'] #here extract the username inside of the <a..>element
            strt = msg.find('>')
            end = msg.find('<',1)

            #if ( self.lang['LeaderBoard'] == '' or ( self.lang['LeaderBoard'] != '' and act['timestamp'] > ts ) ):
            users.setdefault(uid, userObj.copy())
            users[uid]['name'] = msg[strt+1:end]
            users[uid][atype] = users[uid][atype] + int(count)  

        for u in users:
            a = users[u] 
            a['total'] = a['phrase_commented']+a['phrase_suggested']+a['suggestion_deleted']+a['suggestion_voted']

    
        #sorted_list = [x for x in users.iteritems()]    
        sorted_list = [x for x in iter(users.items())] 
        sorted_list.sort(key=lambda x: x[1]['total'])
        sorted_list.reverse()

        output  = '<table id="keywords" class="sort" cellspacing="0" cellpadding="0">'
        output += "<thead><th class='lalign'>Name</th><th>Suggested</th><th>Commented</th><th>Deleted</th><th>Voted</th></thead>"

        suggested = 0
        commented = 0
        deleted = 0
        voted = 0
        lineCount = 0
        for u in sorted_list:
            a = u[1]
            suggested = suggested + a['phrase_suggested']
            commented = commented +a['phrase_commented']
            deleted = deleted +a['suggestion_deleted']
            voted = voted +a['suggestion_voted']
            speed = math.floor(suggested - deleted / 30)
            oddeven = 'odd' if (lineCount % 2) == 0 else 'even'
            link = '<a href="https://crowdin.com/profile/{0}" target="_blank">{0}</a>'.format(a['name']) 
            output += "<tr class='{5}'><td class='lalign'>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td><td>{4}</td></tr>\n".format(link,a['phrase_suggested'],a['phrase_commented'],a['suggestion_deleted'],a['suggestion_voted'], oddeven)
            lineCount +=1

        output += "<tr class='total'><td class='lalign'>Total</td><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td></tr>".format(suggested,commented,deleted,voted)
        output += '</table>'
    
        # arbitraty assumption that every string consists of 27-33 words
        if( suggested-deleted > 0 ):
            month = float(left)/((suggested-deleted)*33)
            days = month * 30
    
            from datetime import timedelta, datetime
            #from dateutil.relativedelta import relativedelta
            i = datetime.today() + timedelta(days=days)
            eta = "{0}.{1}.{2}".format(i.day, i.month, i.year)
        else:
            eta = "never"
            month = 99
            
        self.speed = suggested
        self.eta = eta
        self.velocityString = "<p>At the current speed {0} it will take {1:0.2f} month to complete CrowdinStrings. ETA {2}</p>".format(suggested, month,eta)
        output += self.velocityString
    
        return output      