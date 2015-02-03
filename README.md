# KALanguageReport

KALanguageReport is a lightweight Django web app for to show progress Khan Academy's different Language Translation efforts are making toward reaching certain milestones defined by KA.
KALanguageReport is a tool of the KA Deutsch Community and is not officially affiliated with, nor maintained by, Khan Academy, but rather makes use of different APIs all over the internet to track the translation progress for different languages.
Especially reaching 100% does in no way mean that Khan Academy will upgrade your language to the next stage. But could be a strong indicator that you are getting ready for this.

## Installation
  1. Install Python 2.7
  2. Install Django 1.7
  3. get code from github
  4. copy the file KALanguageReport/settings.default to settings.py and adapt the DB and last 3 values 

## Enhancement Ideas and TODOs
- [ ] Add awesome charts with dynamic date selection etc.
- [ ] Proper configuration to serve static files (css, js, images) from django development server
- [ ] the imagination is your limit

## Commands to be used on the commandline

To start the development server use:
`python manage.py runserver 37.221.195.59:8008

`python manage.py loadMasterlist`
Should be run every Month once the new Masterlist is out. First update with new DocumentID

`python manage.py updateAmaraMapping`
Run directly after loadMasterlist to add refresh AmaraMappings

`python manage.py updateSubtitles`
download amara subtitle information, this process takes very long

`python manage.py KALangStatistic LANGUAGE`
generate the report files for specific LANGUAGE. Make sure the LANGUAGE is defined in the database

## Python prerequirements to be installed

pip install jsonfield
pip install django-import-export

## License information:

The KALanguageReport sourcecode itself is open-source MIT licensed, and the other included software and content is licensed as described in the LICENSE file. 
