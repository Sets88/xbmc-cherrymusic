#!/usr/bin/python
# -*- coding: utf-8 -*-

import xbmc, xbmcgui, xbmcplugin
import xbmcaddon
import sys
import urllib
import urllib2
import urlparse
import simplejson

# Set global values.
version = "0.0.1"
plugin = 'CherryMusic-' + version
author = 'Sets'

# XBMC Hooks
PLUGIN = 'plugin.audio.cherrymusic'
settings = xbmcaddon.Addon(id=PLUGIN)
language = settings.getLocalizedString
enabledebug = settings.getSetting('enabledebug') == "true"
translated = settings.getLocalizedString


host = settings.getSetting('cherrymusichost')
username =  settings.getSetting('cherrymusicuser')
password = settings.getSetting('cherrymusicpass')
session_id = None

#def debug(msg):
#    f = open("/home/sets/.xbmc/temp/log.log", "w")
#    f.write(msg)
#    f.close()
class UI(object):
    def __init__():
        pass

    def add_item(name, url, mode=False, iconimage=""):
        is_folder = None
        new_url = [sys.argv[0] + '?url=%s' % urllib.quote_plus(url)]
        new_url.append('name' % urllib.quote_plus(name.encode("utf-8")))
        if mode:
            is_folder = True
            new_url.append('mode=%s' % str(mode))
        else:
            is_folder = False
        list_item = xbmcgui.ListItem(unicode(name), iconImage=iconimage, thumbnailImage=iconimage)
        list_item.setInfo(type="Audio", infoLabels={ "Title": name })
        ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url="&".join(new_url), listitem=list_item, isFolder=is_folder)
        return ok

    def end_of_directory():
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

    def show_message(header, mesage, iconimage=""):
        xbmc.executebuiltin('XBMC.Notification("%s", "%s", %s, "")' % (header.encode("utf-8"), message.encode("utf-8"), timeout))


def addDir(name, url, mode, iconimage):
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name.encode("utf-8"))
    liz = xbmcgui.ListItem(unicode(name), iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={ "Title": name })
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
    return ok


def addLink(name, url, iconimage):
    liz = xbmcgui.ListItem(unicode(name), iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={ "Title": name })
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=liz)
    return ok


def show_message(header, message, timeout=3000):
    xbmc.executebuiltin('XBMC.Notification("%s", "%s", %s, "")' % (header.encode("utf-8"), message.encode("utf-8"), timeout))


def get_params():
    param = {}
    paramstring = sys.argv[2]
    if len(paramstring) >= 2:
        params = sys.argv[2]
        cleanedparams = params.replace('?', '')
        if params[len(params)-1] == '/':
            params = params[0:len(params) - 2]
        pairsofparams = cleanedparams.split('&')
        param = {}
        for i in range(len(pairsofparams)):
            splitparams = {}
            splitparams = pairsofparams[i].split('=')
            if (len(splitparams)) == 2:
                param[splitparams[0]] = splitparams[1]
    return param


def login(host, username, password):
    """ Login to CherryMusic using POST method """
    global session_id
    req = urllib2.Request(host)
    data = urllib.urlencode({"username": username, "password": password, "login": "login"})
    try:
        res = urllib2.urlopen(req, data=data)
    except urllib2.HTTPError as e:
        pass
    session_id = res.headers.getheader("Set-Cookie").split(";")[0]
    res.close()


def get_random_list():
    """ CherryMusic server generates random playlist, function returns deserialised data """
    request = urllib2.Request(urlparse.urljoin(host, "api/generaterandomplaylist"))
    request.add_header("Cookie", session_id)
    try:
        response = urllib2.urlopen(request)
    except urllib2.HTTPError as e:
        if e.code == 401:
            show_message(translated(30013), translated(30014), 6000)
            return None
    data = response.read()
    response.close()
    return simplejson.loads(data)


def get_playlists():
    """ CherryMusic server returns available playlists, function returns deserialised data """
    request = urllib2.Request(urlparse.urljoin(host, "api/showplaylists"))
    request.add_header("Cookie", session_id)
    try:
        response = urllib2.urlopen(request)
    except urllib2.HTTPError as e:
        if e.code == 401:
            show_message(translated(30013), translated(30014), 6000)
            return None
    data = response.read()
    response.close()
    return simplejson.loads(data)


def get_playlist(id):
    """ CherryMusic server returns playlists by id, function returns deserialised data """
    request = urllib2.Request(urlparse.urljoin(host, "api/loadplaylist"))
    data = urllib.urlencode({"data": simplejson.dumps({"playlistid": id})})
    request.add_header("Cookie", session_id)
    response = urllib2.urlopen(request, data=data)
    data = response.read()
    response.close()
    return simplejson.loads(data)


def search(text):
    """ CherryMusic server returns found tracks by sting, function returns deserialised data """
    request = urllib2.Request(urlparse.urljoin(host, "api/search"))
    data = urllib.urlencode({"data": simplejson.dumps({"searchstring": text})})
    request.add_header("Cookie", session_id)
    try:
        response = urllib2.urlopen(request, data=data)
    except urllib2.HTTPError as e:
        if e.code == 401:
            show_message(translated(30013), translated(30014), 6000)
            return None
    data = response.read()
    response.close()
    return simplejson.loads(data)


def add_to_current_playlist(name, url):
    playlist = xbmc.PlayList(xbmc.PLAYLIST_MUSIC)
    listitem = xbmcgui.ListItem('test')
    listitem.setInfo(type='music', infoLabels={'title': name})
    playlist.add(urllib.unquote(url), listitem)
    show_message("CherryMusic", translated(30015), 6000)


def CATEGORIES():
    """ Main Menu """
    addDir(translated(30010),"",1,"")
    addDir(translated(30011),"",2,"")
    addDir(translated(30012),"",3,"")
    return True


def RANDOM_LIST():
    """ Randomize playlist menu """
    playlist = xbmc.PlayList(xbmc.PLAYLIST_MUSIC)
    playlist.clear()
    data = get_random_list()
    if data is not None:
        for item in data['data']:
            listitem = xbmcgui.ListItem('test')
            listitem.setInfo(type='music', infoLabels={'title': item['label']})
            url = urlparse.urljoin(host, "/serve/")
            url = urlparse.urljoin(url, item['urlpath'])
            playlist.add(url, listitem)
        xbmc.Player().play(playlist)


def SHOW_PLAYLISTS():
    """ Load Playlist menu """
    data = get_playlists()
    if data is not None:
        for item in data['data']:
            addDir(item['title'], str(item['plid']),3,"")
        return True


def SEARCH():
    """ Load Playlist menu """
    keyboard = xbmc.Keyboard('', translated(30016), False)
    keyboard.doModal()
    if keyboard.isConfirmed() and keyboard.getText() != '':
        text = keyboard.getText()
        data = search(text)
        if data is not None:
            for item in data['data']:
                url = urlparse.urljoin(host, "/serve/")
                url = urlparse.urljoin(url, item.get('urlpath'))
                addDir(item.get("label"), url, 1, "")
            return True


def LOAD_PLAYLIST(url):
    """ Load selected playlist """
    playlist = xbmc.PlayList(xbmc.PLAYLIST_MUSIC)
    playlist.clear()
    data = get_playlist(url)['data']
    for item in data:
        listitem = xbmcgui.ListItem('test')
        listitem.setInfo(type='music', infoLabels={'title': item.get("label")})
        url = urlparse.urljoin(host, "/serve/")
        url = urlparse.urljoin(url, item['urlpath'])
        playlist.add(url, listitem)
    xbmc.Player().play(playlist)


params = get_params()

mode = params.get("mode", None)
url = params.get("url", None)
name = params.get("name", "")

if session_id is None:
    if not host or not username or not password:
        show_message(translated(30017), translated(30018), 10000)
    else:
        login(host, username, password)


if not mode:
    if CATEGORIES():
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == '1' and url is None:
    if SEARCH():
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == '1' and url:
    add_to_current_playlist(name, url)
elif mode == '2':
    RANDOM_LIST()
elif mode == '3' and url is None:
    if SHOW_PLAYLISTS():
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == '3' and url:
    LOAD_PLAYLIST(url)
