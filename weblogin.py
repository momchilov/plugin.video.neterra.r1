# -*- coding: utf-8 -*-
#
#     Copyright (C) 2018 zinobg@gmail.com
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#

import os,re,urllib2
import xbmcgui
from xbmc import translatePath as tP
from cookielib import LWPCookieJar as LWPCJ 

# load cookie
def initCookie():
    # if exist load file and cookie information 
    if os.path.isfile(cookiepath):
        LWPCJ().load(cookiepath, False, False)
    else:
        False

# save cookie to file
def updateCookie():
    LWPCJ().save(cookiepath)

def check_login(source_login,username):
    logged_in_string=username
    if re.search(logged_in_string,source_login,re.IGNORECASE):
        return True
    else:
        return False

def openUrl(url):
    initCookie()
    req=urllib.Request(url)
    req.add_header('User-Agent',header_string)
    try:
        response=urllib.urlopen(req)
    except urllib.HTTPError as err:
        if err.code==402:
            xbmcgui.Dialog().notification('[ Subscription ERROR ]','There\'s no active subscription paid!',xbmcgui.NOTIFICATION_ERROR,8000,sound=True)
            raise SystemExit
    source=response.read()
    response.close()
    updateCookie()
    return source

def doLogin(cookiepath,username,password,url_login):
    #check if user has supplied only a folder path, or a full path
    if not os.path.isfile(cookiepath):
        #if the user supplied only a folder path, append on to the end of the path a filename.
        cookiepath=os.path.join(cookiepath,cookie_path,cookie_file)
    #delete any old version of the cookie file
    try:
        os.remove(cookiepath)
    except:
        pass

    if username and password:
        #get the CSRF token
        regexCSRF = r"CSRF_TOKEN\":\"(.*)\",\""
        req = urllib.Request(url_login)
        req.add_header('User-Agent', header_string)
        response = opener.open(req)
        html = response.read()
        response.close()
        matches = re.finditer(regexCSRF, html, re.MULTILINE)
        for matchNum, match in list(enumerate(matches)):
            matchNum = matchNum + 1
            CSRF_TOKEN=match.group(1)
        #token gotten
        req=urllib.Request(url_login)
        req.add_data('_token='+CSRF_TOKEN+'&username='+username+'&password='+password)
        req.add_header('User-Agent',header_string)
        response=opener.open(req)
        source_login=response.read()
        response.close()
        login=check_login(source_login,username)
        if login==True:
            updateCookie()
            return source_login
        else:
            xbmcgui.Dialog().notification('[ Login ERROR ]','Wrong username or password!',xbmcgui.NOTIFICATION_ERROR,8000,sound=True)
            raise SystemExit

cookie_file='cookies_neterratv.r1.lwp'
cookie_path=os.path.join(tP('special://temp'))
header_string='Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'

# cookies
cookiepath=''
cookiepath=os.path.join(cookiepath,cookie_path,cookie_file)
opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(LWPCJ()))
urllib2.install_opener(opener)
initCookie()
