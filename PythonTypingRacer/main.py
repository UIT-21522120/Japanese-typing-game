import copy
import time
import pygame
import random
import sys


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

header_font = pygame.font.Font('D://Python/PythonTypingRacer/Japanese-typing-game/PythonTypingRacer/assets/fonts/square.ttf', 50)
header_font_2 = pygame.font.Font('D://Python/PythonTypingRacer/Japanese-typing-game/PythonTypingRacer/assets/fonts/square.ttf', 25)
pause_font = pygame.font.Font('D://Python/PythonTypingRacer/Japanese-typing-game/PythonTypingRacer/assets/fonts/1up.ttf', 38)
pause_font_for_mode = pygame.font.Font('D://Python/PythonTypingRacer/Japanese-typing-game/PythonTypingRacer/assets/fonts/1up.ttf', 25)
banner_font = pygame.font.Font('D://Python/PythonTypingRacer/Japanese-typing-game/PythonTypingRacer/assets/fonts/1up.ttf', 28)
font = pygame.font.Font('D://Python/PythonTypingRacer/Japanese-typing-game/PythonTypingRacer/assets/fonts/jp.ttf', 45)
font2 = pygame.font.Font('D://Python/PythonTypingRacer/Japanese-typing-game/PythonTypingRacer/assets/fonts/jp.ttf', 30)
font3 = pygame.font.Font('D://Python/PythonTypingRacer/Japanese-typing-game/PythonTypingRacer/assets/fonts/jp.ttf', 25)
font_for_manual = pygame.font.Font('D://Python/PythonTypingRacer/Japanese-typing-game/PythonTypingRacer/assets/fonts/jp.ttf', 20)

# music and sounds
# Music tracks list
music_tracks = [
    'D://Python/PythonTypingRacer/Japanese-typing-game/PythonTypingRacer/assets/sounds/music.mp3',
    'D://Python/PythonTypingRacer/Japanese-typing-game/PythonTypingRacer/assets/sounds/music1.mp3',
    'D://Python/PythonTypingRacer/Japanese-typing-game/PythonTypingRacer/assets/sounds/music2.mp3'
]
current_track_index = 0  # Index of the currently playing track

pygame.mixer.init()
pygame.mixer.music.load(music_tracks[0])
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)
click = pygame.mixer.Sound('D://Python/PythonTypingRacer/Japanese-typing-game/PythonTypingRacer/assets/sounds/click.mp3')
woosh = pygame.mixer.Sound('D://Python/PythonTypingRacer/Japanese-typing-game/PythonTypingRacer/assets/sounds/Swoosh.mp3')
wrong = pygame.mixer.Sound('D://Python/PythonTypingRacer/Japanese-typing-game/PythonTypingRacer/assets/sounds/Instrument Strum.mp3')
click.set_volume(0.3)
woosh.set_volume(0.2)
wrong.set_volume(0.3)

# game variables
level = 1
lives = 5
word_objects = []
high_score = 0
new_game = True
pz = True
new_level = True
submit = ''
submit_to_english = ['', '', '']
active_string = ''
active_string_hiragana = ''
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
           'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '-']

# list shows correctly typed and incorrectly typed words in the history
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
    Converts text from romaji (ローマ字) to kana (Hiragana or Katakana) based on settings.
    
     Parameters:
         input_romaji (str): The romaji text string to be converted.
     ----------
     Return:
         str: Text string that has been converted to hira or kana.
     ----------
    """

    if hira_or_kata[0]:
        return to_hiragana(input_romaji)
    if hira_or_kata[1]:
        return to_katakana(input_romaji)


mouse_detected = False
def one_click_accept():
    """
    Determine whether the user clicked once or not.
    
    Return:
         bool: Returns True if the user has clicked once, False otherwise.
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
    Remove duplicate elements in the list and return a new list.
    
    Parameters:
         input_list (list): List of elements to remove duplicates.
     ----------
    Return:
         list: List after removing duplicate elements.
    ----------

    """
    output_list = []
    for a in input_list:
        if a not in output_list:
            output_list.append(a)
    return output_list


def split_str_to_list(input_string):
    """
    Split a string into a list with up to three elements based on commas and process the string.

    Parameters:
         input_string (str): Text string to be split.
     ----------
    Return:
         list: List containing up to three elements after processing the input string.
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
    Convert a Japanese word to English based on the dictionary list.

    Parameters:
         word (str): Japanese word to convert.
     ----------
    Return:
         str: Corresponding word in English.
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
    The Word class represents a word in the game with properties related to the word's position and movement speed.

    Properties:
         text (str): Text of the word.
         speed (float): Speed of movement of words on the screen.
         y_pos (int): The y position of the word on the screen.
         x_pos (int): The x position of the word on the screen.

    Method:
         draw(): Display the word on the screen at the current position.
         update(): Updates the position of the word according to movement speed.

    """
    def __init__(self, text, speed, y_pos, x_pos):
        self.text = text
        self.speed = speed
        self.y_pos = y_pos
        self.x_pos = x_pos

    def draw(self):
        """
        Displays the word on the screen at the current location.
        If the word matches the beginning of the active string, it will be colored blue.
        """
        color = 'black'
        screen.blit(font.render(self.text, True, color), (self.x_pos, self.y_pos))
        act_len = len(to_kana(active_string))
        check_hira = to_kana(active_string)
        if check_hira == self.text[:act_len]:
            screen.blit(font.render(to_kana(active_string), True, 'green'), (self.x_pos, self.y_pos))

    def update(self):
        """
        Update the position of the word according to the movement speed.
        """
        self.x_pos -= self.speed


class Button:
    """
    The Button class represents a button in a game with properties related to the button's position, text, and state.

    Properties:
         text (str): Text displayed on the button.
         clicked (bool): Status of the button (has been clicked or not).
         surf (pygame.Surface): Surface to draw buttons.
    """

    def __init__(self, x_pos, y_pos, text, clicked, surf):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.text = text
        self.clicked = clicked
        self.surf = surf

    def draw(self):
        """
        Draw a button on the screen and test user interaction.
        If the user clicks on the button, the button's state will be updated.
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
    The LengthChoiceButton class represents an in-game length selection button with properties related to the button's position, text, and state.
    """

    def __init__(self, x_pos, y_pos, text, clicked, surf):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.text = text
        self.clicked = clicked
        self.surf = surf

    def draw(self):
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
       ModeButton class represents an in-game mode button with properties related to position, text, mode type, and button state.
    """

    def __init__(self, x_pos, y_pos, text, clicked, surf, type):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.text = text
        self.clicked = clicked
        self.surf = surf
        self.type = type

    def draw(self):
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
            if self.text == 'RANKING':
                self.surf.blit(pause_font_for_mode.render(self.text, True, '#ffffcc'), (self.x_pos + 36, self.y_pos + 12))
            if self.text == 'HISTORY':
                self.surf.blit(pause_font_for_mode.render(self.text, True, '#ffffcc'), (self.x_pos + 45, self.y_pos + 12))
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
    """
    Draw the main interface of the game on the screen.
    
    Describe:
        - Draw borders and lines dividing different areas of the screen.
        - Displays information about the current level, player's activity sequence, score and highest score.
        - Draw and process interface elements such as pause button and game-related information.
    
    Return:
        - `bool`: State of the pause button (True if clicked, False otherwise).
    """

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
    """
    Draw the game's menu interface on the screen.
    
    Describe:
        - Draw interface elements such as game mode options buttons, exit button, guide button, and music option buttons.
        - Check player interactions with buttons and update status accordingly.
    
    Return:
     - `tuple`: A tuple contains:
     - `bool`: State of the "PLAY" button (True if clicked, False otherwise).
     - `list`: Status list of letter length options (True or False).
     - `bool`: State of the "QUIT" button
     - `bool`: State of the "BACK MENU" button 
     - `bool`: Status of button "?" (instructions)
     - `bool`: State of the "I>" (music) button
     - `bool`: State of the "GAME MODE" button
    """

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

    leaderboard_button = ModeButton(520, 305, 'RANKING', False, surface, 'Game_over')
    leaderboard_button.draw()


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
            pygame.draw.circle(surface, 'yellow', (270 + (i * 90), 495), 35, 5)
    screen.blit(surface, (0, 0))
    return (resume_btn.clicked, choice_commits, quit_btn.clicked, backmenu_btn.clicked, manual_btn.clicked,
            music_btn.clicked, game_mode_btn.clicked, leaderboard_button.clicked)

def draw_cannot_change_mode_while_playing():
    """
    Draw the message that you cannot change the game mode while playing on the screen.

    Describe:
     - Create a new surface with transparency effect.
     - Draw a dialog box containing a message that you cannot change the game mode while playing.
     - Display notification text in specified font and color.
    """

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
    """
    Draw instructions on how to play on the screen.

    Describe:
     - Create a new surface with transparency effect.
     - Draw a dialog box containing instructions on how to play.
     - Display instruction text in specified font and color.
     - Draw navigation button back to menu.

    Return:
     - `bool`: State of the back menu navigation button 
    """

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
    """
    Draw music options on screen.

    Describe:
     - Create a new surface with transparency effect.
     - Draw a dialog box containing music options.
     - Display title text and music options such as stop/play music, increase/decrease volume.
     - Draw navigation buttons back to menu, stop/play music, and volume up/down buttons.
     - Shows the current status of music options.

    Return:
     - A tuple contains the following values:
        + `bool`: State of the back menu navigation button
        + `bool`: Status of the music stop button 
        + `bool`: State of the music playback button
        + `bool`: State of the volume up button 
        + `bool`: State of the volume down button 
    """

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
    """
    Draw the interface when the game ends on the screen.

    Describe:
     - Create a new surface with transparency effect.
     - Draw a dialog box containing the end-of-game message.
     - Displays information about the player's score, including the current score and whether a new record has been set.
     - Draw buttons such as: start again, return to menu, exit, and word history.
    
    Return:
     - A tuple contains the following values:
         - `bool`: State of the restart button.
         - `bool`: State of the menu back button.
         - `bool`: State of the exit button.
         - `bool`: State of the word history button.
    """

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
    """
    VDraw the action confirmation interface on the screen.

    Describe:
     - Create a new surface with transparency effect.
     - Draw a dialog box containing an action confirmation question from the player.
     - Display "YES" and "NO" buttons for players to choose from.

    Return:
     - A tuple contains the following values:
         - `bool`: Status of the "YES" button
         - `bool`: State of the "NO" button
    """

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
    """
    Draw the game mode interface on the screen.

    Describe:
     - Create a new surface with transparency effect.
     - Draw a dialog box containing options for game mode, difficulty, and theme display.
     - Displays the title and controls such as returning to the menu, selecting difficulty (easy, medium, hard), and text style (hiragana, katakana).
     - Displays buttons to adjust game theme, including increase/decrease theme and display current theme.
     - Updates and displays options selected by the user, such as difficulty and font style.

    Return:
     - A tuple contains the following values:
         - `bool`: Status of the menu return button.
         - `bool`: Status of the difficulty button.
         - `bool`: State of the difficulty button.
         - `bool`: State of the hiragana select button.
         - `bool`: State of the katakana selection button.
    """
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
    """
    Draw a history screen in the pygame application, showing a list of 'hit' (true) or 'miss' (false) choices.
    Users can review their previous answers categorized as hits or misses along with their respective translations and meanings.
    This screen also provides interactive buttons to toggle between displaying the hit or miss list and a button to return to the end-game screen.

    This function handles user interaction with the hit and miss buttons to toggle the display list.
    It dynamically adjusts content size based on the number of items and ensures content fits within a predetermined area, with the ability to scroll through items if they exceed the visible area.

    Global variables used:
     - miss: A boolean variable indicating if the miss button is active.
     - hit: A boolean variable indicating if the hit button is active.
     - y_pos_of_text_part: An integer variable that tracks the vertical scroll position of the history text part.
    
    Change:
     - Global variables `miss`, `hit` and `y_pos_of_text_part` based on user interaction.
    
    Return:
     - Boolean: Returns True if the button to return to the game end screen is pressed, otherwise returns False.
    """
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


def get_player_name():
    """
    Lấy tên người chơi từ bàn phím.

    Mô tả:
    - Tạo một bề mặt mới với hiệu ứng trong suốt.
    - Vẽ một hộp thoại chứa hướng dẫn nhập tên người chơi.
    - Hiển thị văn bản hướng dẫn bằng phông chữ và màu sắc được chỉ định.
    - Hiển thị tên người chơi được nhập vào bàn phím.

    Trả về:
    - String: Tên người chơi được nhập từ bàn phím.
    """
   
    surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    pygame.draw.rect(surface, (0, 0, 0, 100), [200, 200, 600, 250], 0, 5)
    pygame.draw.rect(surface, (0, 0, 0, 200), [200, 200, 600, 250], 5, 5)
    surface.blit(header_font.render('Enter your name:', True, 'white'), (300, 220))
    
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.fill((0, 0, 0))  
    overlay.set_alpha(100)  
    screen.blit(overlay, (0, 0))  

    name = ''
    name_entered = False
    clock = pygame.time.Clock()
    while not name_entered:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    name_entered = True
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    name += event.unicode
        surface.blit(font.render(name, True, 'white'), (WIDTH // 2 - 50, HEIGHT // 2 - 50))
        screen.blit(surface, (0, 0))
        pygame.display.update()
        clock.tick(60)
    return name


def save_score_to_leaderboard(name, score):
    """
    Save the player's name and score to a leaderboard file.
    """
    with open("D://Python/PythonTypingRacer/Japanese-typing-game/PythonTypingRacer/leaderboard.txt", "a") as f:
        f.write(f"{name}: {score}\n")


def load_leaderboard():
    """
    Load the leaderboard from the leaderboard file.

    Returns:
    - list: A list of tuples containing the player's name and score.
    """
    try:
        with open("D://Python/PythonTypingRacer/Japanese-typing-game/PythonTypingRacer/leaderboard.txt", "r") as f:
            leaderboard = []
            for line in f.readlines():
                parts = line.strip().split(": ")
                if len(parts) == 2:
                    try:
                        name, score = parts[0], int(parts[1])
                        leaderboard.append((name, score))
                    except ValueError:
                        print(f"Skipping line due to invalid score: {line.strip()}")
                else:
                    print(f"Skipping incorrectly formatted line: {line.strip()}")

            leaderboard.sort(key=lambda x: x[1], reverse=True)
            return leaderboard
    except FileNotFoundError:
        print("Leaderboard file not found.")
        return []


y_pos_of_leaderboard = 0  # Define this outside the function, globally

def draw_leaderboard():
    """
    Draw the leaderboard screen with scroll functionality and bounded display.
    """
    global y_pos_of_leaderboard

    # Define the area for the leaderboard and its visual boundaries
    bounds_x, bounds_y, bounds_width, bounds_height = 200, 70, 550, 500
    visible_area = pygame.Rect(bounds_x, bounds_y, bounds_width, bounds_height-30)

    # Create a semi-transparent surface for the leaderboard
    surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    pygame.draw.rect(surface, (0, 0, 0, 100), [bounds_x, bounds_y, bounds_width, bounds_height], 0,5)
    pygame.draw.rect(surface, (0, 0, 0, 200), [bounds_x, bounds_y, bounds_width, bounds_height], 5,5)

    leaderboard = load_leaderboard()

    # Setting up scrolling bounds
    total_content_height = len(leaderboard) * 50
    min_y_pos = min(100, bounds_height - total_content_height)  # Negative or zero
    y_pos_of_leaderboard = max(min_y_pos, y_pos_of_leaderboard)  # Ensure not to scroll past content

    # Process events (assume this function is called within the event loop context)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Scroll up
                y_pos_of_leaderboard += 50
            elif event.button == 5:  # Scroll down
                y_pos_of_leaderboard -= 50

        # Restrict the scroll position
        y_pos_of_leaderboard = max(min_y_pos, min(0, y_pos_of_leaderboard))

    # Apply clipping to the main screen for drawing leaderboard
    screen.set_clip(visible_area)
    y_start = bounds_y + y_pos_of_leaderboard  # Start drawing from this y position

    # Draw the leaderboard entries within bounds
    for i, (name, score) in enumerate(leaderboard):
        entry_y = y_start + i * 50
        if bounds_y <= entry_y <= bounds_y + bounds_height - 50:  # Check if within visible bounds
            entry_text = font.render(f"{i + 1}. {name}: {score}", True, 'white')
            screen.blit(entry_text, (bounds_x + 100, entry_y))

    # Reset clipping to allow drawing other elements
    screen.set_clip(None)

    # Draw the "Back" button or other interface elements
    leaderboard_to_menu_btn = Button(245, 115, '<-', False, surface)
    leaderboard_to_menu_btn.draw()

    # Blit the entire surface to the main screen
    screen.blit(surface, (0, 0))
    return leaderboard_to_menu_btn.clicked


def get_speed(len_text):
    """
    Determine the speed of the word based on the length of the word and the current game mode.

    Parameters:
     - len_text (int): Length of word.

    Return:
     - float: The speed of the word is determined randomly from a set of values based on the length of the word and the current game mode.
    """

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
    """
    Determines the number of words required in the current level based on the game mode and game level.

    Return:
     - int: Number of words required in the current level based on game mode and game level.
    """
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
    """
    Create new game levels with some random words.

    Describe:
     - Determine the number of words needed in the current level.
     - Generate random words with y and x position, speed and text.
     - Save word objects to `word_objs` list.

    Return:
     - list: List of word objects created in the current level.
    """

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
    """
    Check the answer the user entered.

    Parameters:
     - scor (int): Player's current score.

    Return:
     - int: Updated score after checking answers.
    """

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
    """
    Update high score if current score is higher than existing high score.
    """

    global high_score
    if score > high_score:
        high_score = score


pop_up_start_time = 0
def pop_up(duration):
    """
    Trigger a pop-up notification and set a timer based on the specified duration.
    This message prevents users from changing game modes while the game is in progress.
    This function uses global variables to track the start time of the pop-up and to manage the display state of the game mode change prevention warning.

    Args:
     - duration (int or float): Pop-up display time, in seconds. This is also the time period during which users cannot change the game mode.

    Global variables:
     - pop_up_start_time (float): Variable used to store the pop-up activation start time. This value is updated every time the function is called.
     - show_cannot_change_mode_while_playing (bool): Variable that controls the display of messages preventing mode changes.
     - Is set to True when the pop-up is triggered and should be reset to False by the timer event when the specified time expires.

    Side effects:
     - Set up a timer in pygame, this event is defined to automatically handle notification hiding and allow changing the game mode back after the specified time has passed.
     - This event uses pygame.USEREVENT + 1 for recognition and should be handled appropriately in the game's main event loop.

    """

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
show_leaderboard = False
play_name = False

wordlist = []
wordlist_translated = []

run = True
# player_name = get_player_name()
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
    theme_image = pygame.image.load(f'D://Python/PythonTypingRacer/Japanese-typing-game/PythonTypingRacer/assets/theme/{theme_list[random_theme_index]}').convert()
    blurred_image = theme_image.copy()
    pygame.Surface.blit(blurred_image, theme_image, (0, 0))
    blurred_image.set_alpha(150)
    if show_theme:
        screen.blit(blurred_image, (0, 0))
    pause_butt = draw_screen()
    if play_name == False:
        player_name = get_player_name()
        play_name = True
    if pz:
        if show_menu:
            resume_butt, changes, quit_butt, backmenu_butt, manual_butt, music_butt, game_mode_butt, leaderboard_pressed = draw_menu()
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
            if leaderboard_pressed:
                show_menu = False
                show_leaderboard = True
                pygame.time.delay(25)
        if show_leaderboard:
            leaderboard_to_menu_butt = draw_leaderboard()
            
            if leaderboard_to_menu_butt:
                show_leaderboard = False
                show_menu = True
                pygame.time.delay(25)
        
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

    if lives == 0:
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
        save_score_to_leaderboard(player_name, high_score)
        score = 0
        all_words_appeared = del_repetition(all_words_appeared)
        hit_list = del_repetition(hit_list)
        miss_list = [wrd for wrd in all_words_appeared if wrd not in hit_list]
        

    real_fps = timer.get_fps()
    fps_text = font_for_manual.render("FPS: {:.1f}".format(real_fps), True, 'black')
    screen.blit(fps_text, (900, 10))

    pygame.display.flip()

pygame.quit()
