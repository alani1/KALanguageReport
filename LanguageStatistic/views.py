from __future__ import unicode_literals
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.views.decorators.cache import cache_control

from LanguageStatistic.models import Video,Subtitle,Language,LanguageStatistic
from LanguageStatistic.utils import ftime

import datetime
import time

try:
    import urllib.request as urllib2
except ImportError:
    import urllib2

import httplib  
import json

def index(request):
    # View to show the List and overview of all Languages
    
    languageList = Language.objects.order_by('target')
    languageList.filter(enabled=True)
            
    langData = []        
            
    for lang in languageList:
        today = datetime.date.today()
        statDataList = LanguageStatistic.objects.all().filter(lang=lang.code).filter(date=today)

        lang.data = {}
        percent = 0
        for d in statDataList:
            lang.data[d.type] = {}
            
            if ( d.type == 'C' ):
                percent = percent + (float(d.countSecs) / d.totalSecs)
               
                lang.data[d.type]['left'] = "{:,}".format((d.totalSecs - d.countSecs))
                lang.data[d.type]['speed'] = d.speedStrings
                
                month = float(d.totalStrings - d.countStrings) / d.speedStrings
                days = month * 30
                i = datetime.datetime.today() + datetime.timedelta(days=days)
                lang.data[d.type]['eta'] = "{0}.{1}.{2}".format(i.day, i.month, i.year)                
                
            else:
                percent = percent + (float(d.countSecs) / d.totalSecs)
                lang.data[d.type]['left'] = ftime(d.totalSecs - d.countSecs)
                lang.data[d.type]['speed'] = d.speed
            
        percent = percent / 3
        lang.data['progress'] = '<div class="html5-progress-bar"><span>{0:0.2f}</span>%<progress value="{0:0.2f}" max="100"></progress></div>'.format(percent*100)
            
        
    template = loader.get_template('LanguageStatistic/index.html')
    context = RequestContext(request, {
        'title':"Khanacdemy Translation Summary",
        'base': "http://www.kadeutsch.org/report/",
        'targets': ('Test', 'Live', 'Rockstar' ),
        'languageList': languageList,
        
    })    
    
    return HttpResponse(template.render(context))
    
def ExerciseList(request,slug):
    #Generate List of all exercise groups / Tutorials to be copied to our spreadsheet
    #accepts one parameter which is the subject
    if (slug == '' ):
        slug = 'pre-algebra'
        
    html = getKATopic(slug)    
    
    return HttpResponse(html)

def getKATopic(slug):

    hdrs = {
    'X-Requested-With':'XMLHttpRequest'
    }

    #X-Requested-With	XMLHttpRequest
    try:
        url = 'http://www.khanacademy.org/api/v1/topic/'+slug
        request = urllib2.Request(url, headers = hdrs)
        response = urllib2.urlopen(request)
        str = response.read()
        
        jsonData = json.loads(str)
        children = jsonData['children']
        
        html = ""
        #html += str.decode()
        
        # ka_url = url zur Khanacademy
        for child in children:
            if ( child['kind'] == 'Topic' ):
                html += "<b>{}</b><br/>\n".format(child['translated_title'])
                html += getKATopic(child['node_slug'].replace(' ', '-'))
            elif (child['kind'] == 'Exercise'):
                html += '=HYPERLINK("https://translate.khanacademy.org/translate/content/items?exercises='+child['id']+'","'+child['translated_title']+'")' + "<br>\n"
                #html += '<a href="https://translate.khanacademy.org/translate/content/items?exercises=' + child['id']+ '">' + child['translated_title'] + '</a><br>\n'
                
        return html
        
    except (IOError, httplib.HTTPException):
        return "URLError while loading from KA-API for " + slug
            

@cache_control(must_revalidate=True, max_age=60)
def StatisticData(request,lang):
    #parameters, language, ev. also date range
    #return same format like the data.json file
    import gviz_api
    
    today = datetime.date.today()
    #should be changed to 30 days over time as data quality in db improves
    thirty_days_ago = today - datetime.timedelta(days=14)
    #should be ordered by date ascending
    statDataList = LanguageStatistic.objects.all().filter(lang=lang).filter(date__gte=thirty_days_ago).order_by('date')

    data = []
    date = ''
    crowdin = ''
    dubVideo = ''
    subVideo = ''
    
    for s in statDataList:
        if (date != s.date):
            if (date != ''):
                # print("appending {}".format(date))
                data.append( [ s.date, int(crowdin.getLeft()), int(subVideo.getLeftString()), int(dubVideo.getLeftString()), subVideo.getLeft(), dubVideo.getLeft(), 
                float(crowdin.getPercent()), float(subVideo.getPercent()), float(dubVideo.getPercent())  ])
                crowdin = ''
                dubVideo = ''
                subVideo = ''
                
            date = s.date
            
        if (s.type == 'C'):
            crowdin = s
        elif (s.type == 'D'):
            dubVideo = s
        elif (s.type == 'S'):
            subVideo = s
    
    
    description = [ 
           ("Datum","string"),
           ("Crowdin","number"),
           ("Subtitle","number"),
           ("Video","number"),
           ("subtitleTime","string"),
           ("videoTime","string"),
           ("crowdinPercent","number"),
           ("subtitlePercent","number"),
           ("videoPercent","number"),
    ]    
    
    data_table = gviz_api.DataTable(description)
    data_table.LoadData(data)
    
    
    return HttpResponse(data_table.ToJSon(columns_order=("Datum", "Crowdin", "Subtitle", 'Video'),order_by="Datum"),content_type="application/json")