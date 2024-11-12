# audio.py
import pygame

# 播放提示音
def play_sound(sound_file):
    sound = pygame.mixer.Sound(sound_file)
    sound.play()
