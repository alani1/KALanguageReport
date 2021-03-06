# KALanguageReport

KALanguageReport is a lightweight Django web app for to show progress Khan Academy's different Language Translation efforts are making toward reaching certain milestones defined by KA.
KALanguageReport is a tool of the KA Deutsch Community and is not officially affiliated with, nor maintained by, Khan Academy, but rather makes use of different APIs all over the internet to track the translation progress for different languages.
Especially reaching 100% does in no way mean that Khan Academy will upgrade your language to the next stage. But could be a strong indicator that you are getting ready for this.

## Installation
  1. Install Python 2.7 and `pip` (e.g. `sudo easy_install pip`)
  2. `sudo pip install -r requirements.txt`
  3. Clone git repository: `git clone https://github.com/alani1/KALanguageReport.git`
  4. Copy default configuration: `cp KALanguageReport/settings.default KALanguageReport/settings.py`
  5. Create database: `python manage.py syncdb`

Now you're ready for the initial data import:
  1. `python manage.py loadMasterList`
  2. `python manage.py upateAmaraMapping`
  3. `python manage.py updateSubtitles`
  4. `python manage.py KALangStatistics de`

If desired, replace `de` by your language in step 4.


## Enhancement Ideas and TODOs
- [ ] Add awesome charts with dynamic date selection etc.
- [ ] Proper configuration to serve static files (css, js, images) from django development server
- [ ] the imagination is your limit

## Commands to be used on the commandline

To start the development server use:
```python manage.py runserver 0.0.0.0:8008```

```python manage.py loadMasterlist```
Should be run every Month once the new Masterlist is out. First update with new DocumentID

`python manage.py updateAmaraMapping`
Run directly after loadMasterlist to add refresh AmaraMappings

`python manage.py updateSubtitles`
download amara subtitle information, this process takes very long

`python manage.py KALangStatistic LANGUAGE`
generate the report files for specific LANGUAGE. Make sure the LANGUAGE is defined in the database

## License information:

The KALanguageReport sourcecode itself is open-source MIT licensed, and the other included software and content is licensed as described in the LICENSE file. 
