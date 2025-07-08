import pygame
import time

pygame.init()
pygame.mixer.music.load("bluesky.mp3")
pygame.mixer.music.play()

while pygame.mixer.music.get_busy():  
    time.sleep(1)  