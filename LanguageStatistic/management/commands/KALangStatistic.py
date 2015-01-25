"""KALangStatistic Module

Main Module to create Khan Academy Language translation report
HTML Reports are generated in the ouputDirectory

For every Language setLanguage and generateStatistic are called in this order.

Project Website
http://www.kadeutsch.org

Definition of Crowdin Files
https://docs.google.com/document/d/12xylj_z3BbjMF57WdXJ2Mjr2DduhD5FiVKgb5GQBfvs/edit
"""
from __future__ import unicode_literals
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.db.models import Q
from django.template import Context, loader

from LanguageStatistic.models import Video,Subtitle,Language,LanguageStatistic
from LanguageStatistic.utils import ftime


import _CrowdinAnalyzer
import _VideoStatistic

import codecs
import sys
import pickle
import os.path
import time
   
class Command(BaseCommand):
    """
    Class to generate all Report Files for Language Statistic report
     - Creates Instances of CrowdinAnalyzer and 2 instances of VideoStatistic
     - Uses Django Templates to generate the report Files
    
    Args:
    outputDir (string): OutputDirectory for Report Files
    
    """
    
    args = '<language1 language2 ...>'
    help = 'Generates the Lanugage Progress Report'

    statistics = {}
    lang = {}
    target = 'Test'
    outputDirectory = ""
    langSummary = []
    Targets = ('Test', 'Live', 'Rockstar' )
       
    def setLanguage(self,lang):
        self.lang = lang
        self.setTargetPlatform(lang.target)
        self.crowdin.setLang(lang)
        self.dubVideo.setLang(lang)
        self.subVideo.setLang(lang)
    
    def setTargetPlatform(self,target):
        self.target = target
    
    def writeHTMLFile(self,fileName,html):
        import os
        directory = self.outputDirectory + self.lang.code
        fileName = directory+'/'+fileName
        if not os.path.exists(directory):
            os.makedirs(directory)
            
        file = codecs.open(fileName, 'wt', encoding='utf-8')
        file.write(html)
        file.close()
 
    def generateStatistic(self):
        print("Generating Translation Statistic for " + self.lang.ename + " " + self.target + " Site")    
        self.crowdin.prepareStatistics(self.target)
        
        self.dubVideo.prepareStatistics()
        self.subVideo.prepareStatistics()
        
        self.writeMissingVideoStatistics()
        self.writeDoneVideoStatistics()
        self.writeStatisticFile()
        
    def writeStatisticFile(self):
        html = ""

        menuItems = []
        menuItems.append(['missingVideos','Missing Videos'])
        menuItems.append(['missingSubtitles','Missing Subtitles'])
        menuItems.append(['activity', 'Activity'])
        menuItems.append(['charts','Charts'])
        
        

        context = Context( {
            'title':u"Khan Academy " + self.lang.name + self.target + " Progess Report",
            'base': "http://www.kadeutsch.org/report/static",
            'updated': time.strftime("%d.%m.%Y - %H:%M %Z"),
            'lang': self.lang,
            'menuItems':menuItems,
            'summary': self.printSummaryTable(),
            'crowdin': self.crowdin.StatisticTable,
            'dubVideo': self.dubVideo.StatisticTable,
            'subVideo': self.subVideo.StatisticTable,
            'crowdinActivity': self.crowdin.UserStatisticTable,
            'amaraActivity': self.subVideo.getActivity(),
            'parentPage': self.target+'SiteStatistic.html'
        })
        template = loader.get_template('LanguageStatistic/languageProgress.html')          
        self.writeHTMLFile(self.target+'SiteStatistic.html',template.render(context));           
  
    def writeMissingVideoStatistics(self):
        html = ""
        html += self.dubVideo.generateMissingVideoTable(False)
        html += self.subVideo.generateMissingVideoTable(False)
  
        self.generateVideoTable(html,'SiteMissingVideos.html')
  
    def writeDoneVideoStatistics(self):
        
        html = ""
        html += self.dubVideo.generateCompletedVideoTable(True)
        html += self.subVideo.generateCompletedVideoTable(True)
        
        self.generateVideoTable(html,'SiteDoneVideos.html')

    def generateVideoTable(self,html,fileName):
        menuItems = []
        #only call generateMenu on one VideoObject
        self.dubVideo.generateMenu(menuItems)
        
        context = Context( {
            'title':"Completed Videos for "+self.lang.name+ ' ' +self.target+ " site of Khanacademy",
            'base': "http://www.kadeutsch.org/report/static",
            'updated': time.strftime("%d.%m.%Y - %H:%M %Z"),
            'lang': self.lang,
            'menuItems':menuItems,
            'html': html,
            'parentPage': self.target+'SiteStatistic.html'
        })
        template = loader.get_template('LanguageStatistic/siteVideos.html')          
        self.writeHTMLFile(self.target+fileName,template.render(context));   
        
    def printSummaryTable(self):
        totalAmount = self.crowdin.TotalStrings + self.dubVideo.TotalStrings + self.subVideo.TotalStrings 
        totalLeft = self.crowdin.Left + self.dubVideo.LeftString + self.subVideo.LeftString
        
        progress =  ( self.crowdin.Percent + self.subVideo.Percent + self.dubVideo.Percent ) / 3
        
        print( "Language {0} is at {1:0.2f}% for {2}".format(self.lang.name,progress * 100,self.lang.target ))

        #self.createDataFiles()

        output = u'<h1>Status Khan Academy '+self.lang.name+ " " + self.target + ' platform</h1>'
        
        output += u'<table id="keywords" cellspacing="0" cellpadding="0">'
        output += u'<div class="html5-progress-bar"><span>{0:0.2f}</span>%<progress value="{0:0.2f}" max="100"></progress></div>'.format(progress*100)
        output += u"<thead><th class='lalign'></th><th>Completed</th><th># left</th><th>Total</th></thead>"
        output += u"<tr class='odd'><td class='lalign'><a href='#crowdin'>Crowdin Strings</a></td><td>{0:0.2f}%</td><td>{1}</td><td>{2}</td></tr>".format(self.crowdin.Percent*100,self.crowdin.Left,self.crowdin.TotalStrings)
        output += u"<tr class='even'><td class='lalign'><a href='#missingSubtitles'>Video Subtitles</a><td>{0:0.2f}%</td><td>{1}</td><td>{3}</td></tr>".format(self.subVideo.Percent*100, ftime(self.subVideo.Left),self.subVideo.LeftString,self.subVideo.Total)
        output += u"<tr class='odd'><td class='lalign'><a href='#missingVideos'>Video Synchronisation</a><td>{0:0.2f}%</td><td>{1}</td><td>{3}</td></tr>".format(self.dubVideo.Percent*100, ftime(self.dubVideo.Left),self.dubVideo.LeftString,self.dubVideo.Total)
        output += u"<tr class='total'><td class='lalign'>Total</td><td>{0:0.2f}%</td><td></td><td></td>".format(progress*100,'',totalLeft,totalAmount)
        output += u"</table><center>Aktualisiert " + time.strftime("Updated %d.%m.%Y - %H:%M %Z") +self.crowdin.velocityString
        
        sum = {}
        sum['target']       = self.target
        sum['language']     = self.lang.name
        sum['code']         = self.lang.code
        sum['target']         = self.lang.target
        sum['hours']        = self.dubVideo.Left
        sum['subtitles']    = self.subVideo.Left        
        sum['left']         = self.crowdin.Left #totalLeft
        sum['progress'] = progress
        sum['speed'] = self.crowdin.speed
        sum['eta'] = self.crowdin.eta
        self.langSummary.append(sum)
        return output           
    
    #Main Entry Point
    def handle(self, *args, **options):
        self.outputDirectory = settings.OUTPUTDIRECTORY
        
        #videoListTemplate = loader.get_template('LanguageStatistic/videoList.html')
        self.crowdin = _CrowdinAnalyzer.CrowdinAnalyzer()
        self.dubVideo = _VideoStatistic.VideoStatistic(True)
        self.subVideo = _VideoStatistic.VideoStatistic(False)        
        
        #load the languages specified
        languages = Language.objects.filter(enabled=True)
        for lang in args:
            languages = languages.filter(ename=lang)
                
        for lang in languages:
            self.setLanguage(lang)
            self.generateStatistic()


