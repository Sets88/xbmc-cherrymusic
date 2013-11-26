#! /bin/sh

CURRDIR=`pwd`
rm plugin.audio.cherrymusic.zip
cd ..
zip -r --exclude="*.git*" --exclude="*create_plugin_archive.sh*" $CURRDIR/plugin.audio.cherrymusic.zip $CURRDIR
