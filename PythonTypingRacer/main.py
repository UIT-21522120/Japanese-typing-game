import copy
import time
import pygame
import random

from wordlist import *
from convert import to_hiragana, to_roma, to_katakana

pygame.init()

WIDTH = 1000
HEIGHT = 700
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Japanese Typing Game!')
surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
timer = pygame.time.Clock()
fps = 60

score = 0
save_score = 0

# load image as theme
theme_list = ['1.png', '2.jpg', '3.jpg','4.jpg','5.jpg','6.jpg']
random_theme_index = random.randint(0, len(theme_list) - 1)

header_font = pygame.font.Font('D://Python/PythonTypingRacer/PythonTypingRacer/assets/fonts/square.ttf', 50)
header_font_2 = pygame.font.Font('D://Python/PythonTypingRacer/PythonTypingRacer/assets/fonts/square.ttf', 25)
pause_font = pygame.font.Font('D://Python/PythonTypingRacer/PythonTypingRacer/assets/fonts/1up.ttf', 38)
pause_font_for_mode = pygame.font.Font('D://Python/PythonTypingRacer/PythonTypingRacer/assets/fonts/1up.ttf', 25)
banner_font = pygame.font.Font('D://Python/PythonTypingRacer/PythonTypingRacer/assets/fonts/1up.ttf', 28)
font = pygame.font.Font('D://Python/PythonTypingRacer/PythonTypingRacer/assets/fonts/jp.ttf', 45)
font2 = pygame.font.Font('D://Python/PythonTypingRacer/PythonTypingRacer/assets/fonts/jp.ttf', 30)
font3 = pygame.font.Font('D://Python/PythonTypingRacer/PythonTypingRacer/assets/fonts/jp.ttf', 25)
font_for_manual = pygame.font.Font('D://Python/PythonTypingRacer/PythonTypingRacer/assets/fonts/jp.ttf', 20)

# music and sounds
# Music tracks list
music_tracks = [
    'D://Python/PythonTypingRacer/PythonTypingRacer/assets/sounds/music.mp3',
    'D://Python/PythonTypingRacer/PythonTypingRacer/assets/sounds/music1.mp3',
    'D://Python/PythonTypingRacer/PythonTypingRacer/assets/sounds/music2.mp3'
]
current_track_index = 0  # Index of the currently playing track

pygame.mixer.init()
pygame.mixer.music.load(music_tracks[0])
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)
click = pygame.mixer.Sound('D://Python/PythonTypingRacer/PythonTypingRacer/assets/sounds/click.mp3')
woosh = pygame.mixer.Sound('D://Python/PythonTypingRacer/PythonTypingRacer/assets/sounds/Swoosh.mp3')
wrong = pygame.mixer.Sound('D://Python/PythonTypingRacer/PythonTypingRacer/assets/sounds/Instrument Strum.mp3')
click.set_volume(0.3)
woosh.set_volume(0.2)
wrong.set_volume(0.3)

# game variables
level = 1
lives = 5
word_objects = []

high_score = 0

pz = True
new_level = True
submit = ''
submit_to_english = ['', '', '']
active_string = ''
active_string_hiragana = ''
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
           'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '-']

# list show những từ đã gõ đúng và gõ sai trong phần history
all_words_appeared = []
hit_list = []
miss_list = []

# 2 letter, 3 letter, 4 letter, 5 letter, 6 letter, etc
choices = [True, False, False, False, False, False]

music_choices = [False, True]

mode_choices = [True, False, False]

hira_or_kata = [True, False]


def to_kana(input_romaji):
    """
    Chuyển đổi văn bản từ romaji (chữ Latinh) sang kana (Hiragana hoặc Katakana) dựa trên cài đặt.
    
    Tham số:
        input_romaji (str): Chuỗi văn bản dạng romaji cần được chuyển đổi.
    ----------
    Trả về:
        str: Chuỗi văn bản đã được chuyển đổi sang dạng hira hoặc kana.
    ----------
    """

    if hira_or_kata[0]:
        return to_hiragana(input_romaji)
    if hira_or_kata[1]:
        return to_katakana(input_romaji)


mouse_detected = False
def one_click_accept():
    """
    Xác định xem người dùng đã nhấp chuột một lần hay không.
    
    Trả về:
        bool: Trả về True nếu người dùng đã nhấp chuột một lần, ngược lại là False.
    """

    global mouse_detected
    mouse_butt = pygame.mouse.get_pressed()
    if mouse_butt[0]:
        if not mouse_detected:
            mouse_detected = True
            return True
        if mouse_detected:
            return False
    else:
        mouse_detected = False
        return False


def del_repetition(input_list):
    """
    Xóa các phần tử trùng lặp trong danh sách và trả về danh sách mới.
    
    Tham số:
        input_list (list): Danh sách các phần tử cần loại bỏ trùng lặp.
    ----------
    Trả về:
        list: Danh sách sau khi đã loại bỏ các phần tử trùng lặp.
    ----------
    """
    output_list = []
    for a in input_list:
        if a not in output_list:
            output_list.append(a)
    return output_list


def split_str_to_list(input_string):
    """
    Chia một chuỗi thành danh sách với tối đa ba phần tử dựa trên dấu phẩy và xử lý chuỗi.

    Tham số:
        input_string (str): Chuỗi văn bản cần được chia tách.
    ----------
    Trả về:
        list: Danh sách chứa tối đa ba phần tử sau khi xử lý chuỗi đầu vào.
    ----------
    """
    lst = ['', '', '']

    input_string = input_string.split(',')
    for i in range(len(input_string)):
        input_string[i] = input_string[i].strip()
        if len(input_string[i]) < 20:
            lst[i] = '- ' + input_string[i]

    if lst[0] == '' and lst[1] == '' and lst[2] != '':
        lst[0] = lst[2]
        lst[2] = ''
    elif lst[0] == '' and lst[1] != '' and lst[2] != '':
        lst[0] = lst[1]
        lst[1] = lst[2]
        lst[2] = ''
    elif lst[0] == '' and lst[1] != '' and lst[2] == '':
        lst[0] = lst[1]
        lst[1] = ''
    elif lst[0] != '' and lst[1] == '' and lst[2] != '':
        lst[1] = lst[2]
        lst[2] = ''

    return lst


def ja_to_en(word):
    """
    Chuyển đổi một từ tiếng Nhật sang tiếng Anh dựa trên danh sách từ điển.

    Tham số:
        word (str): Từ tiếng Nhật cần chuyển đổi.
    ----------
    Trả về:
        str: Từ tương ứng trong tiếng Anh.
    ----------
    """
    index = 0
    for i in range(len(wordlist)):
        if wordlist[i] == word:
            index = i
            break
    return wordlist_translated[index]


class Word:
    """
    Lớp Word biểu diễn một từ trong trò chơi với các thuộc tính liên quan đến vị trí và tốc độ di chuyển của từ.

    Thuộc tính:
        text (str): Văn bản của từ.
        speed (float): Tốc độ di chuyển của từ trên màn hình.
        y_pos (int): Vị trí y của từ trên màn hình.
        x_pos (int): Vị trí x của từ trên màn hình.

    Phương thức:
        draw(): Hiển thị từ trên màn hình tại vị trí hiện tại.
        update(): Cập nhật vị trí của từ theo tốc độ di chuyển.
    """
    def __init__(self, text, speed, y_pos, x_pos):
        self.text = text
        self.speed = speed
        self.y_pos = y_pos
        self.x_pos = x_pos

    def draw(self):
        """
        Hiển thị từ trên màn hình tại vị trí hiện tại.
        Nếu từ khớp với phần đầu của chuỗi đang hoạt động, nó sẽ được tô màu xanh.
        """
        color = 'black'
        screen.blit(font.render(self.text, True, color), (self.x_pos, self.y_pos))
        act_len = len(to_kana(active_string))
        check_hira = to_kana(active_string)
        if check_hira == self.text[:act_len]:
            screen.blit(font.render(to_kana(active_string), True, 'green'), (self.x_pos, self.y_pos))

    def update(self):
        """
        Cập nhật vị trí của từ theo tốc độ di chuyển.
        """

        self.x_pos -= self.speed


class Button:
    """
    Lớp Button biểu diễn một nút trong trò chơi với các thuộc tính liên quan đến vị trí, văn bản và trạng thái của nút.

    Thuộc tính:
        x_pos (int): Vị trí x của nút trên màn hình.
        y_pos (int): Vị trí y của nút trên màn hình.
        text (str): Văn bản hiển thị trên nút.
        clicked (bool): Trạng thái của nút (đã được nhấp hay chưa).
        surf (pygame.Surface): Bề mặt để vẽ nút.

    Phương thức:
        draw(): Vẽ nút trên màn hình và kiểm tra sự tương tác của người dùng.
    """

    def __init__(self, x_pos, y_pos, text, clicked, surf):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.text = text
        self.clicked = clicked
        self.surf = surf

    def draw(self):
        """
        Vẽ nút trên màn hình và kiểm tra sự tương tác của người dùng.
        Nếu người dùng nhấp chuột lên nút, trạng thái của nút sẽ được cập nhật.
        """

        cir = pygame.draw.circle(self.surf, (45, 89, 135), (self.x_pos, self.y_pos), 35)
        if cir.collidepoint(pygame.mouse.get_pos()):
            if one_click_accept():
                pygame.draw.circle(self.surf, (190, 35, 35), (self.x_pos, self.y_pos), 35)
                self.clicked = True
            else:
                pygame.draw.circle(self.surf, (190, 89, 135), (self.x_pos, self.y_pos), 35)
        pygame.draw.circle(self.surf, 'white', (self.x_pos, self.y_pos), 35, 3)
        self.surf.blit(pause_font.render(self.text, True, 'white'), (self.x_pos - 15, self.y_pos - 25))


class LengthChoiceButton:
    """
    Lớp LengthChoiceButton biểu diễn một nút lựa chọn độ dài trong trò chơi với các thuộc tính liên quan đến vị trí, văn bản và trạng thái của nút.

    Thuộc tính:
        x_pos (int): Vị trí x của nút trên màn hình.
        y_pos (int): Vị trí y của nút trên màn hình.
        text (str): Văn bản hiển thị trên nút.
        clicked (bool): Trạng thái của nút (đã được nhấp hay chưa).
        surf (pygame.Surface): Bề mặt để vẽ nút.

    Phương thức:
        draw(): Vẽ nút trên màn hình và kiểm tra sự tương tác của người dùng.
    """

    def __init__(self, x_pos, y_pos, text, clicked, surf):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.text = text
        self.clicked = clicked
        self.surf = surf

    def draw(self):
        """
        Vẽ nút trên màn hình và kiểm tra sự tương tác của người dùng.
        Nếu người dùng nhấp chuột lên nút, trạng thái của nút sẽ được cập nhật.
        """

        cir = pygame.draw.circle(self.surf, (45, 89, 135), (self.x_pos, self.y_pos), 35)
        if cir.collidepoint(pygame.mouse.get_pos()):
            butts = pygame.mouse.get_pressed()
            if butts[0]:
                pygame.draw.circle(self.surf, (190, 35, 35), (self.x_pos, self.y_pos), 35)
                self.clicked = True
            else:
                pygame.draw.circle(self.surf, (190, 89, 135), (self.x_pos, self.y_pos), 35)
        pygame.draw.circle(self.surf, 'white', (self.x_pos, self.y_pos), 35, 3)
        self.surf.blit(pause_font.render(self.text, True, 'white'), (self.x_pos - 15, self.y_pos - 25))


class ModeButton:
    """
    Lớp ModeButton biểu diễn một nút chế độ trong trò chơi với các thuộc tính liên quan đến vị trí, văn bản, loại chế độ và trạng thái của nút.

    Thuộc tính:
        x_pos (int): Vị trí x của nút trên màn hình.
        y_pos (int): Vị trí y của nút trên màn hình.
        text (str): Văn bản hiển thị trên nút.
        clicked (bool): Trạng thái của nút (đã được nhấp hay chưa).
        surf (pygame.Surface): Bề mặt để vẽ nút.
        type (str): Loại chế độ của nút ("Mode" hoặc "Game_over").

    Phương thức:
        draw(): Vẽ nút trên màn hình và kiểm tra sự tương tác của người dùng.
    """

    def __init__(self, x_pos, y_pos, text, clicked, surf, type):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.text = text
        self.clicked = clicked
        self.surf = surf
        self.type = type

    def draw(self):
        """
        Vẽ nút trên màn hình và kiểm tra sự tương tác của người dùng.
        Nếu người dùng nhấp chuột lên nút, trạng thái của nút sẽ được cập nhật.
        """

        if self.type == 'Mode':
            rect = pygame.draw.rect(self.surf, (45, 89, 135), (self.x_pos, self.y_pos, 150, 60), 0, 10)
            if rect.collidepoint(pygame.mouse.get_pos()):
                if one_click_accept():
                    pygame.draw.rect(self.surf, (190, 35, 35), (self.x_pos, self.y_pos, 150, 60), 0, 10)
                    self.clicked = True
                else:
                    pygame.draw.rect(self.surf, (190, 89, 135), (self.x_pos, self.y_pos, 150, 60), 0, 10)
            pygame.draw.rect(self.surf, 'white', (self.x_pos, self.y_pos, 150, 60), 5, 10)
            len_text = len(self.text)
            if self.text == 'EASY':
                self.surf.blit(pause_font_for_mode.render(self.text, True, '#ffffcc'), (self.x_pos + 29, self.y_pos + 12))
            if self.text == 'MEDIUM':
                self.surf.blit(pause_font_for_mode.render(self.text, True, '#ffffcc'), (self.x_pos + 13, self.y_pos + 12))
            if self.text == 'HARD':
                self.surf.blit(pause_font_for_mode.render(self.text, True, '#ffffcc'), (self.x_pos + 29, self.y_pos + 12))
            if self.text == 'HIT!':
                self.surf.blit(pause_font_for_mode.render(self.text, True, '#ffffcc'), (self.x_pos + 39, self.y_pos + 12))
            if self.text == 'MISS!':
                self.surf.blit(pause_font_for_mode.render(self.text, True, '#ffffcc'), (self.x_pos + 29, self.y_pos + 12))

        if self.type == 'Game_over':
            rect = pygame.draw.rect(self.surf, (45, 89, 135), (self.x_pos, self.y_pos, 220, 60), 0, 10)
            if rect.collidepoint(pygame.mouse.get_pos()):
                if one_click_accept():
                    pygame.draw.rect(self.surf, (190, 35, 35), (self.x_pos, self.y_pos, 220, 60), 0, 10)
                    self.clicked = True
                else:
                    pygame.draw.rect(self.surf, (190, 89, 135), (self.x_pos, self.y_pos, 220, 60), 0, 10)
            pygame.draw.rect(self.surf, 'white', (self.x_pos, self.y_pos, 220, 60), 5, 10)
            len_text = len(self.text)
            if self.text == 'RESTART':
                self.surf.blit(pause_font_for_mode.render(self.text, True, '#ffffcc'), (self.x_pos + 34, self.y_pos + 12))
            if self.text == 'MENU':
                self.surf.blit(pause_font_for_mode.render(self.text, True, '#ffffcc'), (self.x_pos + 65, self.y_pos + 12))
            if self.text == 'QUIT':
                self.surf.blit(pause_font_for_mode.render(self.text, True, '#ffffcc'), (self.x_pos + 70, self.y_pos + 12))
            if self.text == 'HISTORY':
                self.surf.blit(pause_font_for_mode.render(self.text, True, '#ffffcc'), (self.x_pos + 36, self.y_pos + 12))
            if self.text == 'PLAY':
                self.surf.blit(pause_font_for_mode.render(self.text, True, '#ffffcc'), (self.x_pos + 65, self.y_pos + 12))
            if self.text == 'BACK MENU':
                self.surf.blit(pause_font_for_mode.render(self.text, True, '#ffffcc'), (self.x_pos + 10, self.y_pos + 12))
            if self.text == 'YES':
                self.surf.blit(pause_font_for_mode.render(self.text, True, '#ffffcc'), (self.x_pos + 75, self.y_pos + 12))
            if self.text == 'NO':
                self.surf.blit(pause_font_for_mode.render(self.text, True, '#ffffcc'), (self.x_pos + 90, self.y_pos + 12))
            if self.text == 'GAME MODE':
                self.surf.blit(pause_font_for_mode.render(self.text, True, '#ffffcc'), (self.x_pos + 15, self.y_pos + 12))
            if self.text == 'HIRAGANA':
                self.surf.blit(pause_font_for_mode.render(self.text, True, '#ffffcc'), (self.x_pos + 28, self.y_pos + 12))
            if self.text == 'KATAKANA':
                self.surf.blit(pause_font_for_mode.render(self.text, True, '#ffffcc'), (self.x_pos + 23, self.y_pos + 12))
            if self.text == 'SHOW THEME':
                self.surf.blit(pause_font_for_mode.render(self.text, True, '#ffffcc'), (self.x_pos + 2, self.y_pos + 12))


def draw_screen():
    # screen outlines for main game window and 'header' section
    pygame.draw.rect(screen, (32, 42, 68), [0, HEIGHT - 100, WIDTH, 100], 0)
    pygame.draw.rect(screen, 'white', [0, 0, WIDTH, HEIGHT], 5)
    pygame.draw.line(screen, 'white', (0, HEIGHT - 100), (WIDTH, HEIGHT - 100), 2)
    pygame.draw.line(screen, 'white', (250, HEIGHT - 100), (250, HEIGHT), 2)
    pygame.draw.line(screen, 'white', (900, HEIGHT - 100), (900, HEIGHT), 2)
    pygame.draw.line(screen, 'white', (610, HEIGHT - 100), (610, HEIGHT), 2)
    pygame.draw.rect(screen, 'black', [0, 0, WIDTH, HEIGHT], 2)
    # text for showing current level, player's current string, high score and pause options
    screen.blit(header_font.render(f'Level: {level}', True, 'white'), (10, HEIGHT - 75))
    screen.blit(font2.render(f'"{active_string}"', True, 'white'), (260, HEIGHT - 55))
    active_string_hiragana = to_kana(active_string)
    screen.blit(font2.render(f'"{active_string_hiragana}"', True, 'white'), (260, HEIGHT - 100))

    screen.blit(font3.render(f'{submit_to_english[0]}', True, 'white'), (620, HEIGHT - 105))
    screen.blit(font3.render(f'{submit_to_english[1]}', True, 'white'), (620, HEIGHT - 75))
    screen.blit(font3.render(f'{submit_to_english[2]}', True, 'white'), (620, HEIGHT - 45))

    pause_btn = Button(947, HEIGHT - 52, 'II', False, screen)
    pause_btn.draw()
    # draw lives, score, and high score on top of screen
    screen.blit(banner_font.render(f'Score: {score}', True, 'black'), (400, 10))
    screen.blit(banner_font.render(f'Best: {high_score}', True, 'black'), (700, 10))
    screen.blit(banner_font.render(f'Lives: {lives}', True, 'black'), (100, 10))
    return pause_btn.clicked


def draw_menu():
    choice_commits = copy.deepcopy(choices)
    surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    pygame.draw.rect(surface, (0, 0, 0, 100), [200, 100, 600, 450], 0, 5)
    pygame.draw.rect(surface, (0, 0, 0, 200), [200, 100, 600, 450], 5, 5)
    resume_btn = ModeButton(250, 135, 'PLAY', False, surface, 'Game_over')
    resume_btn.draw()

    quit_btn = ModeButton(250, 305, 'QUIT', False, surface, 'Game_over')
    backmenu_btn = ModeButton(250, 305, 'BACK MENU', False, surface, 'Game_over')
    if new_level:
        quit_btn.draw()
    else:
        backmenu_btn.draw()

    game_mode_btn = ModeButton(250, 220, 'GAME MODE', False, surface, 'Game_over')
    game_mode_btn.draw()

    # surface.blit(header_font.render('PLAY!', True, 'white'), (300, 140))
    surface.blit(header_font.render('MANUAL', True, 'white'), (600, 140))
    # surface.blit(header_font.render('QUIT', True, 'white'), (300, 225))
    surface.blit(header_font.render('MUSIC', True, 'white'), (600, 225))
    surface.blit(header_font.render('Active Letter Lengths:', True, 'white'), (210, 395))

    manual_btn = Button(550, 165, '?', False, surface)
    manual_btn.draw()

    music_btn = Button(550, 250, 'I>', False, surface)
    music_btn.draw()

    for i in range(len(choices)):
        btn = LengthChoiceButton(270 + (i * 90), 495, str(i + 2), False, surface)
        btn.draw()
        if btn.clicked:
            if choice_commits[i]:
                choice_commits[i] = False
            else:
                choice_commits[i] = True
        if choices[i]:
            pygame.draw.circle(surface, 'yellow', (270 + (i * 80), 495), 35, 5)
    screen.blit(surface, (0, 0))
    return (resume_btn.clicked, choice_commits, quit_btn.clicked, backmenu_btn.clicked, manual_btn.clicked,
            music_btn.clicked, game_mode_btn.clicked)


def draw_cannot_change_mode_while_playing():
    surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    pygame.draw.rect(surface, (0, 0, 0, 100), [805, 250, 150, 185], 0, 5)
    pygame.draw.rect(surface, (0, 0, 0, 200), [805, 250, 150, 185], 5, 5)
    surface.blit(header_font_2.render('Cannot', True, 'white'), (825, 270))
    surface.blit(header_font_2.render('change', True, 'white'), (825, 300))
    surface.blit(header_font_2.render('game mode', True, 'white'), (825, 330))
    surface.blit(header_font_2.render('while', True, 'white'), (825, 360))
    surface.blit(header_font_2.render('playing!', True, 'white'), (825, 390))

    screen.blit(surface, (0, 0))


def draw_manual():
    surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    pygame.draw.rect(surface, (0, 0, 0, 100), [200, 70, 600, 500], 0, 5)
    pygame.draw.rect(surface, (0, 0, 0, 200), [200, 70, 600, 500], 5, 5)
    surface.blit(header_font.render('How to play?', True, 'white'), (350, 90))
    surface.blit(font_for_manual.render('- Type the romaji transcription corresponding to the word on', True, 'white'), (210, 200))
    surface.blit(font_for_manual.render('the screen and press enter and the word will disappear if you', True, 'white'), (210, 230))
    surface.blit(font_for_manual.render('entered it correctly.', True, 'white'), (210, 260))
    surface.blit(font_for_manual.render('- The game mode is customizable: Word lists in Hiragana or', True, 'white'), (210, 320))
    surface.blit(font_for_manual.render('Katakana, varying word lengths for learning, and difficulty', True, 'white'), (210, 350))
    surface.blit(font_for_manual.render('levels (Easy, Medium, or Hard)', True, 'white'), (210, 380))
    
    manual_to_menu_btn = Button(245, 115, '<-', False, surface)
    manual_to_menu_btn.draw()

    screen.blit(surface, (0, 0))
    return manual_to_menu_btn.clicked


def draw_music_option():
    surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    pygame.draw.rect(surface, (0, 0, 0, 100), [200, 100, 600, 400], 0, 5)
    pygame.draw.rect(surface, (0, 0, 0, 200), [200, 100, 600, 400], 5, 5)
    surface.blit(header_font.render('Music option', True, 'white'), (350, 120))

    music_to_menu_btn = Button(245, 145, '<-', False, surface)
    music_to_menu_btn.draw()

    music_pause_btn = Button(630, 250, 'II', False, surface)
    music_pause_btn.draw()
    music_unpause_btn = Button(730, 250, 'I>', False, surface)
    music_unpause_btn.draw()

    if music_pause_btn.clicked:
        music_choices[0] = True
        music_choices[1] = False
    if music_unpause_btn.clicked:
        music_choices[0] = False
        music_choices[1] = True
    if music_choices[0]:
        pygame.draw.circle(surface, 'yellow', (630, 250), 35, 5)
    elif music_choices[1]:
        pygame.draw.circle(surface, 'yellow', (730, 250), 35, 5)

    volume_up = Button(530, 250, '>', False, surface)
    volume_up.draw()
    volume_down = Button(250, 250, '<', False, surface)
    volume_down.draw()

    pygame.draw.rect(surface, '#6ec6ff', (290, 247, 200, 15), 5, 20)

    current_vol = round(pygame.mixer.music.get_volume(), 1)
    current_vol *= 10

    pygame.draw.circle(surface, 'black', (300 + (current_vol * 18), 255), 9)

    # Thêm nút Previous và Next
    prev_btn = Button(250, 400, '<', False, surface)
    prev_btn.draw()
    next_btn = Button(730, 400, '>', False, surface)
    next_btn.draw()
    
    # Hiển thị tên bài nhạc đang chọn
    surface.blit(banner_font.render(f'MUSIC {current_track_index + 1}', True, 'white'), (440, 380))
    screen.blit(surface, (0, 0))
    return music_to_menu_btn.clicked, music_pause_btn.clicked, music_unpause_btn.clicked, volume_up.clicked, volume_down.clicked, prev_btn.clicked, next_btn.clicked


def draw_game_over():
    surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    pygame.draw.rect(surface, (0, 0, 0, 100), [200, 100, 600, 400], 0, 5)
    pygame.draw.rect(surface, (0, 0, 0, 200), [200, 100, 600, 400], 5, 5)

    surface.blit(header_font.render('GAME OVER!', True, 'white'), (380, 120))

    game_over_to_menu_btn = ModeButton(250, 330, 'RESTART', False, surface, 'Game_over')
    game_over_to_menu_btn.draw()

    back_to_menu_btn = ModeButton(250, 410, 'MENU', False, surface, 'Game_over')
    back_to_menu_btn.draw()

    game_over_quit_btn = ModeButton(530, 410, 'QUIT', False, surface, 'Game_over')
    game_over_quit_btn.draw()

    word_history_btn = ModeButton(530, 330, 'HISTORY', False, surface, 'Game_over')
    word_history_btn.draw()
    if not new_record_found:
        surface.blit(header_font.render('Your score: ', True, 'white'), (280, 220))
        surface.blit(header_font.render(f'{save_score}', True, 'white'), (620, 220))
    elif new_record_found:
        surface.blit(header_font.render('New record: ', True, 'white'), (280, 220))
        surface.blit(header_font.render(f'{save_score}', True, 'red'), (620, 220))

    screen.blit(surface, (0, 0))
    return game_over_to_menu_btn.clicked, back_to_menu_btn.clicked, game_over_quit_btn.clicked, word_history_btn.clicked


def draw_are_you_sure():
    surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    pygame.draw.rect(surface, (0, 0, 0, 100), [200, 200, 600, 250], 0, 5)
    pygame.draw.rect(surface, (0, 0, 0, 200), [200, 200, 600, 250], 5, 5)
    surface.blit(header_font.render('Are you sure ?', True, 'white'), (330, 220))

    no_btn = ModeButton(250, 330, 'NO', False, surface, 'Game_over')
    no_btn.draw()

    yes_btn = ModeButton(530, 330, 'YES', False, surface, 'Game_over')
    yes_btn.draw()

    screen.blit(surface, (0, 0))
    return yes_btn.clicked, no_btn.clicked


def draw_game_mode():
    surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    pygame.draw.rect(surface, (0, 0, 0, 100), [200, 100, 600, 460], 0, 5)
    pygame.draw.rect(surface, (0, 0, 0, 200), [200, 100, 600, 460], 5, 5)

    surface.blit(header_font.render('GAME MODE', True, 'white'), (380, 120))

    game_mode_to_menu_btn = Button(245, 145, '<-', False, surface)
    game_mode_to_menu_btn.draw()

    surface.blit(header_font.render('DIFFICULTY', True, 'white'), (375, 290))

    easy_btn = ModeButton(220, 350, 'EASY', False, surface, 'Mode')
    easy_btn.draw()
    medium_btn = ModeButton(420, 350, 'MEDIUM', False, surface, 'Mode')
    medium_btn.draw()
    hard_btn = ModeButton(620, 350, 'HARD', False, surface, 'Mode')
    hard_btn.draw()

    if mode_choices[0]:
        pygame.draw.rect(surface, 'yellow', (220, 350, 150, 60), 7, 10)
    if mode_choices[1]:
        pygame.draw.rect(surface, 'yellow', (420, 350, 150, 60), 7, 10)
    if mode_choices[2]:
        pygame.draw.rect(surface, 'yellow', (620, 350, 150, 60), 7, 10)

    hira_btn = ModeButton(250, 210, 'HIRAGANA', False, surface, 'Game_over')
    hira_btn.draw()
    kata_btn = ModeButton(520, 210, 'KATAKANA', False, surface, 'Game_over')
    kata_btn.draw()
    if hira_or_kata[0]:
        pygame.draw.rect(surface, 'yellow', (250, 210, 220, 60), 7, 10)
    if hira_or_kata[1]:
        pygame.draw.rect(surface, 'yellow', (520, 210, 220, 60), 7, 10)

    show_theme_btn = ModeButton(220, 470, 'SHOW THEME', False, surface, 'Game_over')
    show_theme_btn.draw()
    global show_theme, random_theme_index
    if show_theme_btn.clicked:
        if show_theme:
            pygame.time.delay(25)
            show_theme = False
        else:
            pygame.time.delay(25)
            show_theme = True
    if show_theme:
        pygame.draw.rect(surface, 'yellow', (220, 470, 220, 60), 7, 10)
    if random_theme_index < 10:
        surface.blit(banner_font.render(f'THEME {random_theme_index + 1}', True, 'white'), (536, 480))
    else:
        surface.blit(banner_font.render(f'THEME {random_theme_index + 1}', True, 'white'), (527, 480))

    next_theme_btn = Button(750, 500, '>', False, surface)
    next_theme_btn.draw()
    prev_theme_btn = Button(490, 500, '<', False, surface)
    prev_theme_btn.draw()

    if next_theme_btn.clicked:
        random_theme_index += 1
        if random_theme_index == len(theme_list):
            random_theme_index = 0
    if prev_theme_btn.clicked:
        random_theme_index -= 1
        if random_theme_index == -1:
            random_theme_index = len(theme_list) - 1

    screen.blit(surface, (0, 0))
    return (game_mode_to_menu_btn.clicked, easy_btn.clicked, medium_btn.clicked, hard_btn.clicked,
            hira_btn.clicked, kata_btn.clicked)


y_pos_of_text_part = 0
miss, hit = True, False
def draw_history():
    surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    pygame.draw.rect(surface, (0, 0, 0, 100), [140, 70, 720, 515], 0, 5)
    pygame.draw.rect(surface, (0, 0, 0, 200), [140, 70, 720, 515], 5, 5)
    hit_btn = ModeButton(570, 90, 'HIT!', False, surface, 'Mode')
    hit_btn.draw()
    miss_btn = ModeButton(350, 90, 'MISS!', False, surface, 'Mode')
    miss_btn.draw()
    history_to_game_over_btn = Button(185, 115, '<-', False, surface)
    history_to_game_over_btn.draw()
    global miss, hit
    if hit_btn.clicked:
        miss, hit = False, True
    if miss_btn.clicked:
        miss, hit = True, False

    pygame.draw.line(surface, '#cae63e', (145, 175), (853, 175), 8)

    length_of_text_surface = 0
    if miss:
        pygame.draw.rect(surface, 'yellow', (350, 90, 150, 60), 7, 10)
        length_of_text_surface = len(miss_list) * 170 + 10
    if hit:
        pygame.draw.rect(surface, 'yellow', (570, 90, 150, 60), 7, 10)
        length_of_text_surface = len(hit_list) * 170 + 10

    if length_of_text_surface <= 400:
        length_of_text_surface = 400

    history_text_surface = pygame.Surface((710, length_of_text_surface))
    history_text_surface.fill((70, 70, 70))

    global y_pos_of_text_part

    if miss:
        if miss_list:
            for i in range(len(miss_list)):
                history_text_surface.blit(font2.render(f'{i+1}. {miss_list[i]}', True, 'white'), (20, i*170 + 10))
                history_text_surface.blit(font2.render(f'  {to_roma(miss_list[i])}', True, 'white'), (20, i * 170 + 60))
                pygame.draw.line(history_text_surface, 'white', (0, i*170 + 170), (853, i*170 + 170), 5)
                pygame.draw.line(history_text_surface, 'white', (290, i*170), (290, i*170 + 170), 5)
                meaning_list = split_str_to_list(ja_to_en(miss_list[i]))
                if meaning_list[0]:
                    history_text_surface.blit(font2.render(f'{meaning_list[0]}', True, 'white'), (310, i * 170))
                if meaning_list[1]:
                    history_text_surface.blit(font2.render(f'{meaning_list[1]}', True, 'white'), (310, i * 170 + 55))
                if meaning_list[2]:
                    history_text_surface.blit(font2.render(f'{meaning_list[2]}', True, 'white'), (310, i * 170 + 110))

    if hit:
        if hit_list:
            for i in range(len(hit_list)):
                history_text_surface.blit(font2.render(f'{i + 1}. {hit_list[i]}', True, 'white'), (20, i * 170 + 10))
                history_text_surface.blit(font2.render(f'  {to_roma(hit_list[i])}', True, 'white'), (20, i * 170 + 60))
                pygame.draw.line(history_text_surface, 'white', (0, i * 170 + 170), (853, i * 170 + 170), 5)
                pygame.draw.line(history_text_surface, 'white', (290, i * 170), (290, i * 170 + 170), 5)
                meaning_list = split_str_to_list(ja_to_en(hit_list[i]))
                if meaning_list[0]:
                    history_text_surface.blit(font2.render(f'{meaning_list[0]}', True, 'white'), (310, i * 170))
                if meaning_list[1]:
                    history_text_surface.blit(font2.render(f'{meaning_list[1]}', True, 'white'), (310, i * 170 + 55))
                if meaning_list[2]:
                    history_text_surface.blit(font2.render(f'{meaning_list[2]}', True, 'white'), (310, i * 170 + 110))
        else:
            history_text_surface.blit(font.render('Let practice more!', True, 'white'), (110, 160))

    if y_pos_of_text_part <= 0:
        y_pos_of_text_part = 0
    if y_pos_of_text_part >= length_of_text_surface - 400:
        y_pos_of_text_part = length_of_text_surface - 400

    source_rect = pygame.Rect(0, y_pos_of_text_part, 710, 400)
    part_of_text_surf = history_text_surface.subsurface(source_rect)

    screen.blit(surface, (0, 0))
    screen.blit(part_of_text_surf, (145, 180))
    return history_to_game_over_btn.clicked


def get_speed(len_text):
    if mode_choices[0]:
        if len_text in [2, 3]:
            return random.choice([1, 1.5, 2])
        if len_text in [4, 5]:
            return random.choice([1, 1.3, 1.5])
        if len_text in [6, 7]:
            return random.choice([0.6, 0.8, 1])
    elif mode_choices[1]:
        if len_text in [2, 3]:
            return random.choice([1, 2, 3])
        if len_text in [4, 5]:
            return random.choice([1.5, 1.8, 2])
        if len_text in [6, 7]:
            return random.choice([1, 1.3, 1.5])
    elif mode_choices[2]:
        if len_text in [2, 3]:
            return random.choice([2, 3, 4, 5])
        if len_text in [4, 5]:
            return random.choice([2, 3, 4])
        if len_text in [6, 7]:
            return random.choice([1, 2, 2.5])


def get_number_of_word_base_on_mode():
    if mode_choices[0]:
        if level <= 2:
            return level
        if level >= 14:
            return 5
        else:
            return 2 + (level - 2) // 4
    if mode_choices[1]:
        if level <= 2:
            return level
        if level >= 14:
            return 6
        else:
            return 2 + (level - 2) // 3
    if mode_choices[2]:
        if level <= 2:
            return level
        if level >= 17:
            return 7
        else:
            return 2 + (level - 2) // 3


def generate_level():
    word_objs = []
    include = []
    vertical_spacing = (HEIGHT - 150) // get_number_of_word_base_on_mode()
    if True not in choices:
        choices[0] = True
    for i in range(len(choices)):
        if choices[i]:
            include.append((len_indexes[i], len_indexes[i + 1]))
    for i in range(get_number_of_word_base_on_mode()):
        ind_sel = random.choice(include)
        index = random.randint(ind_sel[0], ind_sel[1])
        text = wordlist[index].lower()
        len_text = len(text)
        y_pos = random.randint(30 + (i * vertical_spacing), (i + 1) * vertical_spacing)
        if get_number_of_word_base_on_mode() < 4:
            x_pos = random.randint(WIDTH, WIDTH + len_text*50)
        else:
            x_pos = random.randint(WIDTH, WIDTH + len_text*70)

        speed = get_speed(len_text)
        speed += level / 100

        new_word = Word(text, speed, y_pos, x_pos)
        word_objs.append(new_word)
    return word_objs


def check_answer(scor):
    global submit_to_english
    for wrd in word_objects:
        if wrd.text == submit:
            points = wrd.speed * len(wrd.text) * 10 * (len(wrd.text) / 4)
            scor += int(points)
            word_objects.remove(wrd)
            woosh.play()
            submit_to_english = split_str_to_list(ja_to_en(submit))
            # những từ submit đúng được cho vào hit_list
            hit_list.append(wrd.text)
    return scor


def check_high_score():
    global high_score
    if score > high_score:
        high_score = score


pop_up_start_time = 0
def pop_up(duration):
    global pop_up_start_time, show_cannot_change_mode_while_playing
    show_cannot_change_mode_while_playing = True
    pop_up_start_time = time.time()
    pygame.time.set_timer(pygame.USEREVENT + 1, duration * 1000)


show_history = False
new_record_found = False
show_theme = True
show_game_mode = False
show_are_you_sure = False
show_cannot_change_mode_while_playing = False
show_menu = True
show_manual = False
show_music = False
show_game_over = False

wordlist = []
wordlist_translated = []

run = True
while run:
    # load từ từ bảng hira hoặc kata vào
    if hira_or_kata[0]:
        wordlist = wordlist_hira
        wordlist_translated = wordlist_hira_translated
    if hira_or_kata[1]:
        wordlist = wordlist_kata
        wordlist_translated = wordlist_kata_translated

    len_indexes = []
    length = 1

    # wordlist.sort(key=len)
    for i in range(len(wordlist)):
        if len(wordlist[i]) > length:
            length += 1
            len_indexes.append(i)
    len_indexes.append(len(wordlist))

    # in lên màn hình
    screen.fill('gray')
    timer.tick(fps)
    # draw static background
    theme_image = pygame.image.load(f'D://Python/PythonTypingRacer/PythonTypingRacer/assets/theme/{theme_list[random_theme_index]}').convert()
    blurred_image = theme_image.copy()
    pygame.Surface.blit(blurred_image, theme_image, (0, 0))
    blurred_image.set_alpha(150)
    if show_theme:
        screen.blit(blurred_image, (0, 0))
    pause_butt = draw_screen()
    if pz:
        if show_menu:
            resume_butt, changes, quit_butt, backmenu_butt, manual_butt, music_butt, game_mode_butt = draw_menu()
            if resume_butt:
                pz = False
                show_menu = False
            if quit_butt:
                check_high_score()
                run = False
                pygame.time.delay(50)
            if backmenu_butt:
                show_are_you_sure = True
                show_menu = False
                pygame.time.delay(25)
            if game_mode_butt:
                show_game_mode = True
                show_menu = False
                pygame.time.delay(25)
            if manual_butt:
                show_menu = False
                show_manual = True
                pygame.time.delay(25)
            if music_butt:
                show_menu = False
                pygame.time.delay(25)
                show_music = True
            if one_click_accept():
                choices = changes
        if show_manual:
            manual_to_menu_butt = draw_manual()
            if manual_to_menu_butt:
                show_manual = False
                show_menu = True
                pygame.time.delay(25)
        if show_music:
            music_to_menu_butt, music_pause_butt, music_unpause_butt, vol_up_butt, vol_down_butt, prev_track_butt, next_track_butt = draw_music_option()
            if music_to_menu_butt:
                show_music = False
                show_menu = True
                pygame.time.delay(25)
            if music_pause_butt:
                pygame.mixer.music.pause()
            if music_unpause_butt:
                pygame.mixer.music.unpause()
            cur_vol = pygame.mixer.music.get_volume()
            if vol_up_butt and cur_vol <= 1:
                pygame.mixer.music.set_volume(cur_vol + 0.1)
                pygame.time.delay(25)
            if vol_down_butt and cur_vol >= 0:
                pygame.mixer.music.set_volume(cur_vol - 0.1)
                pygame.time.delay(25)
            if vol_down_butt and cur_vol <= 0.1:
                pygame.mixer.music.set_volume(0)

            # Xử lý đổi bài hát
            if prev_track_butt:
                current_track_index = (current_track_index - 1) % len(music_tracks)
                pygame.mixer.music.load(music_tracks[current_track_index])
                pygame.mixer.music.play(-1)
                pygame.time.delay(25)

            if next_track_butt:
                current_track_index = (current_track_index + 1) % len(music_tracks)
                pygame.mixer.music.load(music_tracks[current_track_index])
                pygame.mixer.music.play(-1)
                pygame.time.delay(25)
        if show_game_over:
            restart_butt, game_over_to_menu_butt, game_over_quit_butt, word_history_butt = draw_game_over()
            show_menu = False
            if restart_butt:
                show_game_over = False
                new_level = True
                pz = False
                active_string = ''
                all_words_appeared = []
                hit_list = []
                miss_list = []
                submit_to_english = ['', '', '']
                pygame.time.delay(25)
            if game_over_to_menu_butt:
                show_game_over = False
                show_menu = True
                all_words_appeared = []
                hit_list = []
                miss_list = []
                submit_to_english = ['', '', '']
                pygame.time.delay(25)
            if game_over_quit_butt:
                check_high_score()
                run = False
                pygame.time.delay(25)
            if word_history_butt:
                show_game_over = False
                show_history = True
                pygame.time.delay(25)
        if show_are_you_sure:
            yes_butt, no_butt = draw_are_you_sure()
            if yes_butt:
                level = 1
                lives = 5
                score = 0
                new_level = True
                active_string = ''
                word_objects = []
                all_words_appeared = []
                hit_list = []
                miss_list = []
                show_are_you_sure = False
                show_menu = True
                submit_to_english = ['', '', '']
            if no_butt:
                show_are_you_sure = False
                show_menu = True
        if show_game_mode:
            game_mode_to_menu_butt, easy_butt, medium_butt, hard_butt, hira_butt, kata_butt = draw_game_mode()
            if not new_level:
                if easy_butt or medium_butt or hard_butt or hira_butt or kata_butt:
                    pop_up(2)
                if show_cannot_change_mode_while_playing:
                    draw_cannot_change_mode_while_playing()
            if new_level:
                if easy_butt:
                    mode_choices[0], mode_choices[1], mode_choices[2] = True, False, False
                if medium_butt:
                    mode_choices[0], mode_choices[1], mode_choices[2] = False, True, False
                if hard_butt:
                    mode_choices[0], mode_choices[1], mode_choices[2] = False, False, True
                if hira_butt:
                    hira_or_kata[0], hira_or_kata[1] = True, False
                if kata_butt:
                    hira_or_kata[0], hira_or_kata[1] = False, True
            if game_mode_to_menu_butt:
                show_game_mode = False
                show_menu = True
                pygame.time.delay(25)
        if show_history:
            history_to_game_over_butt = draw_history()
            if history_to_game_over_butt:
                show_history = False
                show_game_over = True
    if not show_game_mode:
        show_cannot_change_mode_while_playing = False
    if new_level and not pz:
        word_objects = generate_level()
        # lấy tất cả những từ đã xuất hiện cho vào all_words_appeared list
        for i in word_objects:
            all_words_appeared.append(i.text)
        new_level = False
    else:
        for w in word_objects:
            w.draw()
            if not pz:
                w.update()
            if w.x_pos < -(len(w.text) * 50 + 50):
                word_objects.remove(w)
                lives -= 1
    if len(word_objects) <= 0 and not pz:
        level += 1
        new_level = True

    if submit != '':
        init = score
        score = check_answer(score)
        submit = ''
        if init == score:
            wrong.play()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            check_high_score()
            run = False
        elif event.type == pygame.USEREVENT + 1:
            show_cannot_change_mode_while_playing = False
        if event.type == pygame.KEYDOWN:
            if not pz:
                if event.unicode.lower() in letters:
                    if len(to_kana(active_string)) <= 10:
                        active_string += event.unicode
                    click.play()
                if event.key == pygame.K_BACKSPACE and len(active_string) > 0:
                    active_string = active_string[:-1]
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    submit = to_kana(active_string)
                    active_string = ''
            if event.key == pygame.K_ESCAPE:
                if pz and show_menu:
                    pz = False
                    show_menu = False
                elif not pz and not show_menu:
                    pz = True
                    show_menu = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            if show_history:
                if event.button == 4:
                    y_pos_of_text_part -= 20
                elif event.button == 5:
                    y_pos_of_text_part += 20

        if event.type == pygame.MOUSEBUTTONDOWN and pz:
            if event.button == 1:
                choices = changes

    if pause_butt:
        if not pz:
            pz = True
            show_menu = True

    if lives < 0:
        save_score = score
        if score > high_score:
            new_record_found = True
        else:
            new_record_found = False
        pz = True
        show_game_over = True
        level = 1
        lives = 5
        word_objects = []
        new_level = True
        check_high_score()
        score = 0
        all_words_appeared = del_repetition(all_words_appeared)
        hit_list = del_repetition(hit_list)
        miss_list = [wrd for wrd in all_words_appeared if wrd not in hit_list]

    real_fps = timer.get_fps()
    fps_text = font_for_manual.render("FPS: {:.1f}".format(real_fps), True, 'black')
    screen.blit(fps_text, (900, 10))

    pygame.display.flip()

pygame.quit()
