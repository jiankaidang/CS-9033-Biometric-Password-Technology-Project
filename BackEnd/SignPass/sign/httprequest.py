'''
Created on Dec 7, 2012

@author: Paul
'''
import urllib,urllib2


headers = {
    "User-Agent" : "Mozilla/5.0 (Windows NT 5.1; rv:15.0) Gecko/20100101 Firefox/15.0",
    "Accept" : "text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,text/png,*/*;q=0.5",
    "Accept-Language" : "en-us,en;q=0.5",
    "Accept-Charset" : "ISO-8859-1",
    "Content-type": "application/x-www-form-urlencoded",
    "Host": "m.facebook.com"
}
params = urllib.urlencode({'user':'username','pass':'password','login':'Log+In'})
req = urllib2.Request('http://www.facebook.com/login.php', params, headers)
res = urllib2.urlopen(req)