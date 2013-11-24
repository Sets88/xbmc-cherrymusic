import xbmc, xbmcgui, xbmcplugin
import xbmcaddon
import sys
import urllib

# Set global values.
version = "0.0.1"
plugin = 'CherryMusic-' + version
author = 'Sets'

# XBMC Hooks
PLUGIN = 'plugin.audio.cherrymusic'
settings = xbmcaddon.Addon(id=PLUGIN)
language = settings.getLocalizedString
enabledebug = settings.getSetting('enabledebug') == "true"
host = settings.getSetting('cherrymusichost')
login =  settings.getSetting('cherrymusicuser')
password = settings.getSetting('cherrymusicpass')
session_id = None

def CATEGORIES():
	addDir("Search by Title","",1,"")
	addDir("Random","",2,"")
	addDir("Load Playlists","",3,"")


def addDir(name,url,mode,iconimage):
	u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "name=" + urllib.quote_plus(name)
	liz = xbmcgui.ListItem(unicode(name), iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo(type="Video", infoLabels={ "Title": name })
	ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
	return ok


def get_params():
	param = []
	paramstring = sys.argv[2]
	if len(paramstring) >= 2:
		params = sys.argv[2]
		cleanedparams = params.replace('?','')
		if params[len(params) - 1] == '/':
			params = params[0:len(params) - 2]
		pairsofparams = cleanedparams.split('&')
		param = {}
		for i in range(len(pairsofparams)):
			splitparams = {}
			splitparams = pairsofparams[i].split('=')
			if (len(splitparams)) == 2:
				param[splitparams[0]] = splitparams[1]
	return param


def login(host, user, password):
	req = urllib2.Request(host)
	data = urllib.urlencode({"username": user, "password": password, "login": "login"})
	res = urllib2.urlopen(req, data=data)
	session_id = res.headers.getheader("Set-Cookie").split(";")[0]


def get_random_list():
	req = urllib2.Request(host + "api/generaterandomplaylist/")
	req.add_header("Cookie", session_id)
	res = urllib2.urlopen(req)
	


params = get_params()
mode = None


login(host, user, password)

try:
	mode=int(params["mode"])
except:
	pass

if mode is None:
	CATEGORIES()
elif mode == 1:
	pass
elif mode == 2:
	pass

xbmcplugin.endOfDirectory(int(sys.argv[1]))