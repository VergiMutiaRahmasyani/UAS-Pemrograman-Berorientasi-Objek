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

class TubeManager:
    #Manajer Tabung untuk Mengelola logika permainan, tabung warna, menggambar tabung di layar, dan validasi kondisi menang/kalah.
    def __init__(self, color_choices, screen_width):
    #Mengatur pilihan warna dan lebar layar.
    #Menginisialisasi tabung, warna tabung, dan salinan awal warna tabung.    
        self.color_choices = color_choices
        self.screen_width = screen_width
        self.tubes = []
        self.tube_colors = []
        self.initial_colors = []

    def generate_start(self):
        #Menghasilkan konfigurasi awal permainan:
        #Menentukan jumlah tabung secara acak.
        tubes_number = random.randint(10, 14)
        tubes_colors = [[] for _ in range(tubes_number)]
        available_colors = [i for i in range(tubes_number - 2) for _ in range(4)]

        #Mengisi warna ke tabung sesuai aturan permainan.
        for i in range(tubes_number - 2):
            for _ in range(4):
                color = random.choice(available_colors)
                tubes_colors[i].append(color)
                available_colors.remove(color)

        self.tubes = tubes_number
        self.tube_colors = tubes_colors
        self.initial_colors = copy.deepcopy(tubes_colors)

    def draw_tubes(self, screen, selected_index):
    #Menggambar tabung di layar:
    #Tabung dibagi menjadi dua baris dengan posisi tertentu.
    #Tabung yang dipilih diberi warna hijau.
        tube_boxes = []
        tubes_per_row = self.tubes // 2 if self.tubes % 2 == 0 else self.tubes // 2 + 1
        spacing = self.screen_width / tubes_per_row

        def draw_single_row(offset, start, end, y_start):
            for i in range(start, end):
                for j in range(len(self.tube_colors[i])):
                    pygame.draw.rect(screen, self.color_choices[self.tube_colors[i][j]],
                                     [offset + 5 + spacing * (i - start), y_start - (50 * j), 65, 50], 0, 3)
                box = pygame.draw.rect(screen, 'blue',
                                       [offset + 5 + spacing * (i - start), y_start - 150, 65, 200], 5, 5)
                if selected_index == i:
                    pygame.draw.rect(screen, 'green',
                                     [offset + 5 + spacing * (i - start), y_start - 150, 65, 200], 3, 5)
                tube_boxes.append(box)




