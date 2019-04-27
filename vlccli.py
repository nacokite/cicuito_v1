from vlc import vlc
from time import sleep
import sys
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
file_name = 'semaforo.mp3'
# VLC player controls
#~ Instance = vlc.Instance()
#~ p = Instance.media_player_new()
p = vlc.MediaPlayer(dir_path + '/' + file_name)
p.play()
sleep(5)
p.stop()
