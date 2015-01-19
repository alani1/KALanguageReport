from __future__ import unicode_literals
import os
import sys
import json
import base64
import logging
import httplib
from time import time
from datetime import datetime

from django.conf import settings

headers = {
    "www.amara.org": { 
        "X-api-username"    : settings.AMARA_USER,
        "X-apikey"          : settings.AMARA_KEY
    }
}

def ftime(b):
    """Format a time string which is seconds as HH:MM:SS"""
    import math

    hours = int(math.floor(b/3600))
    min  = int(math.floor(b / 60) - (hours * 60))
    secs = int(b % 60)
    
    return "{0:02d}:{1:02d}:{2:02d}".format(hours,min,secs)

def decode_datetime(obj):
    """ Converts string into date time object. """
    if "created" not in obj:
        return obj
    dt = datetime.strptime(obj["created"], "%Y-%m-%dT%H:%M:%S")
    obj["created"] = dt
    return obj


def get_conn():
    """ Create a HTTP connection to Amara API. """
    conn = httplib.HTTPSConnection("www.amara.org")
    return conn

def get_conn_google():
    """ Create a HTTP connection to Google Docs. """
    conn = httplib.HTTPSConnection("docs.google.com")
    return conn

def get_conn_khan():
    """ Create a HTTP connection to Khan Academy API. """
    conn = httplib.HTTPConnection("www.khanacademy.org")
    return conn

def get_conn_youtube():
    """ Create a HTTP connection to Google API. """
    conn = httplib.HTTPSConnection("www.googleapis.com")
    return conn

def get_response(conn, query, decode=True):
    """ Execute API request specified by path with default authentication data
    and return unformatted content.

    """
    conn.putrequest("GET", query)
    conn.putheader("Content-type", "application/json; charset=utf-8")
    conn.putheader("Accept", "*/*")
    if conn.host in headers:
        for name, value in headers[conn.host].items():
            conn.putheader(name, value)
    conn.endheaders()

    response  = conn.getresponse().read()
    
    if decode:
        response = response.decode()

    return response

def get_response_json(conn, path, decode=True):
    """ Load content for given URL query using given connection
    and parse it as JSON.

    """
    doc = get_response(conn, path, decode)
    return json.loads(doc, encoding="utf-8")        
    

def get_google_csv(key, gid=0):
    """ Load content for given URL query using given connection
    and parse it as JSON.

    """
    conn = get_conn_google()
    path = "/spreadsheets/d/{0}/export?format=csv&id={0}"
    path = path.format(key, gid)
    doc = get_response(conn, path, False)
    return doc

def save_json(filename, jdoc):
    """ Save JSON object to file with given filename
    using some default formating rules,
    overwritting existing content in the process.

    """
    fout = open(filename, "wt", encoding="utf-8")
    doc = json.dump(jdoc, fout, indent=1, sort_keys=True, ensure_ascii=False)
    fout.close()

def save_text(filename, doc):
    """ Save text to file with given filename,
    overwritting existing content in the process.

    """
    fout = open(filename, "wt", encoding="utf-8")
    fout.write(doc)
    fout.close()

def save_text_binary(filename, doc):
    """ Save text to file with given filename using binary mode,
    overwritting existing content in the process.

    """
    fout = open(filename, "wb")
    fout.write(doc)
    fout.close()

def load_json(filename):
    """ Load file content and parse it as JSON expression."""
    fin = open(filename, encoding="utf-8")
    doc = json.load(fin, encoding="utf-8", object_hook=decode_datetime)
    fin.close
    return doc

def load_text(filename):
    """ Load file content and return it without any processing."""
    fin = open(filename, encoding="utf-8")
    doc = fin.read()
    fin.close
    return doc

def check_time(text, tstart):
    """ Get time progress information. """
    tend = time()
    return "Total time for {} was: {:.2f} sec".format(text, tend - tstart)
