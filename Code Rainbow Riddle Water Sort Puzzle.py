import copy
import random
import pygame

# initialize pygame
pygame.init()

class SoundManager:
    #Manajer Suara Digunakan untuk mengelola efek suara seperti suara gerakan, menang, atau kalah.
    def __init__(self):
        #Memuat file suara untuk gerakan, kemenangan, dan kekalahan.
        try:
            self.move_sound = pygame.mixer.Sound("suara air.wav")
            self.win_sound = pygame.mixer.Sound("menang.mp3")
            self.lose_sound = pygame.mixer.Sound("kalah.mp3")
         #Jika file suara tidak ditemukan atau invalid, akan mengatur suara menjadi None.
        except pygame.error as e:
            print("File suara tidak ditemukan atau invalid:", e)
            self.move_sound = None
            self.win_sound = None
            self.lose_sound = None
    def play_move_sound(self):
    #Memutar efek suara untuk gerakan yang tersedia.
        if self.move_sound:
            self.move_sound.play()

    def play_win_sound(self):
    #Memutar efek suara untuk kemenangan yang tersedia.
        if self.win_sound:
            self.win_sound.play()

    def play_lose_sound(self):
    #Memutar efek suara untuk kekalahan yang tersedia.
        if self.lose_sound:
            self.lose_sound.play()

