#! /bin/sh

rm plugin.audio.cherrymusic.zip
cd ..
zip -r --exclude="*.git*" --exclude="*create_plugin_archive.sh*" plugin.audio.cherrymusic/plugin.audio.cherrymusic.zip plugin.audio.cherrymusic
