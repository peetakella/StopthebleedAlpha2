
import time
import vlc
from time import sleep
import pygame
from time import sleep
pygame.mixer.init()
background = vlc.MediaPlayer("/home/stopthebleed/StoptheBleed/Sounds/police-siren-water-cannon-tear-gas-people-coughing-and-protesters-throwing-stones-at-the-police-during-the-chilean-uprising-november-2019-24871.mp3")
#background.play()
pygame.mixer.music.load("/home/stopthebleed/StoptheBleed/Sounds/Please Stop_v1.mp3")
pygame.mixer.music.play()
sleep(5)
pygame.mixer.music.load("/home/stopthebleed/StoptheBleed/Sounds/Ow_v1.mp3")
pygame.mixer.music.set_volume(1)
pygame.mixer.music.play()
sleep(5)
pygame.mixer.music.set_volume(.5)
sleep(5)
pygame.mixer.music.play()