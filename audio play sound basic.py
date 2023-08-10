import vlc
from time import sleep

you_failed = vlc.MediaPlayer("/home/stopthebleed/StoptheBleed/Sounds/you_failed.mp3")
print(1)
you_failed.play()

scream1 = vlc.MediaPlayer("/home/stopthebleed/StoptheBleed/Sounds/Scream_v1.mp3")
scream2 = vlc.MediaPlayer("/home/stopthebleed/StoptheBleed/Sounds/Scream_v2.mp3")
scream3 = vlc.MediaPlayer("/home/stopthebleed/StoptheBleed/Sounds/Scream_v3.mp3")
scream4 = vlc.MediaPlayer("/home/stopthebleed/StoptheBleed/Sounds/Scream_v4.mp3")
scream5 = vlc.MediaPlayer("/home/stopthebleed/StoptheBleed/Sounds/Scream_v5.mp3")

scream4.play()
sleep (.75)
scream4.stop()
scream3.play()
sleep (.65)
scream3.stop()
scream2.play()
sleep (.75)
scream2.stop()
scream1.play()
sleep (.65)
scream1.stop()
scream4.play()
sleep (.75)
scream4.stop()
scream5.play()
sleep (.65)
scream5.stop()
scream1.play()
sleep (.75)
scream1.stop()
scream3.play()
sleep (.65)
scream3.stop()




player = vlc.MediaPlayer("/home/stopthebleed/STB/ducks1-32839.mp3")
print(1)
player.play()
sleep (5)
player.stop()
you_failed = vlc.MediaPlayer("/home/stopthebleed/StoptheBleed/Sounds/you_failed.mp3")
print(1)
you_failed.play()

you_succeded = vlc.MediaPlayer("/home/stopthebleed/StoptheBleed/Sounds/you_succeded.mp3")
print(1)
you_succeded.play()