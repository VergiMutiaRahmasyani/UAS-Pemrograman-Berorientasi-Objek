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
        
        # Menggambar dua baris tabung
        draw_single_row(0, 0, tubes_per_row, 300)
        if self.tubes % 2 == 0:
            draw_single_row(0, tubes_per_row, self.tubes, 650)
        else:
            draw_single_row(spacing * 0.5, tubes_per_row, self.tubes, 650)

        return tube_boxes

    def reset(self):
        # Mereset warna tabung ke tata letak awal
        self.tube_colors = copy.deepcopy(self.initial_colors)

    def calc_move(self, selected_index, destination_index, sound_manager):
        # Menghitung gerakan antara dua tabung
        if len(self.tube_colors[selected_index]) > 0:
            color_to_move = self.tube_colors[selected_index][-1]  # Warna di bagian atas tabung
            if len(self.tube_colors[destination_index]) < 4 and \
                    (len(self.tube_colors[destination_index]) == 0 or
                     self.tube_colors[destination_index][-1] == color_to_move):
                # Memindahkan warna selama syarat terpenuhi
                while len(self.tube_colors[destination_index]) < 4 and \
                        len(self.tube_colors[selected_index]) > 0 and \
                        self.tube_colors[selected_index][-1] == color_to_move:
                    self.tube_colors[destination_index].append(self.tube_colors[selected_index].pop())
                sound_manager.play_move_sound()
                return True
        return False

    def check_victory(self):
        # Mengecek apakah semua tabung memiliki warna yang sama atau kosong
        for tube in self.tube_colors:
            if len(tube) > 0:
                if len(tube) != 4 or len(set(tube)) > 1:
                    return False
        return True

    def check_loss(self):
        # Mengecek apakah tidak ada lagi gerakan yang mungkin dilakukan
        for i in range(len(self.tube_colors)):
            for j in range(len(self.tube_colors)):
                if i != j and len(self.tube_colors[i]) > 0 and len(self.tube_colors[j]) < 4:
                    if len(self.tube_colors[j]) == 0 or self.tube_colors[i][-1] == self.tube_colors[j][-1]:
                        return False
        return True


class Game:
    def __init__(self):
        self.WIDTH = 900  # Lebar layar
        self.HEIGHT = 1000  # Tinggi layar
        self.screen = pygame.display.set_mode([self.WIDTH, self.HEIGHT])  # Membuat jendela layar
        pygame.display.set_caption('Water Sort PyGame')  # Judul permainan
        self.font = pygame.font.Font('freesansbold.ttf', 36)  # Font untuk skor
        self.large_font = pygame.font.Font('freesansbold.ttf', 72)  # Font untuk pesan besar
        self.fps = 60  # Kecepatan frame
        self.timer = pygame.time.Clock()  # Pengatur waktu

        # Warna-warna yang digunakan dalam permainan
        color_choices = [(255, 0, 0), (255, 165, 0), (173, 216, 230), (0, 0, 255),
                         (0, 100, 0), (255, 192, 203), (128, 0, 128), (169, 169, 169),
                         (139, 69, 19), (144, 238, 144), (255, 255, 0), (255, 255, 255)]

        self.sound_manager = SoundManager()  # Mengelola suara
        self.tube_manager = TubeManager(color_choices, self.WIDTH)  # Mengelola tabung

        self.new_game = True
        self.selected = False
        self.select_index = -1
        self.win = False
        self.lose = False
        self.score = 0
        self.message_played = False




