import pygame
from time import sleep
pygame.mixer.init()
pygame.mixer.music.load("/home/stopthebleed/STB/ducks1-32839.mp3")
pygame.mixer.music.play()
sleep(5)
pygame.mixer.music.play()
sleep(5)
pygame.mixer.music.play()
while pygame.mixer.music.get_busy() == True:
    continue