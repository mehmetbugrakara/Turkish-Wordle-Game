import pygame
import random
import pandas as pd

# Load the word list
words_df = pd.read_csv('words_df.csv')
words = words_df['Words'].to_list()
choosen_words = [word for word in words if 4 <= len(word) <= 6]

alphabet = 'ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ'
used_letters = set()

def choose_word():
    """Choose a random word from the selected word list."""
    return random.choice(choosen_words)

def show_letter_list():
    """Display the list of letters on the screen."""
    x = 50  
    y = 500  
    for letter in alphabet:
        if letter not in used_letters:
            letter_surface = font.render(letter, True, BLACK)
        elif letter in word:
            letter_surface = font.render(letter, True, GREEN)
        else:
            letter_surface = font.render(letter, True, RED)  
        win.blit(letter_surface, (x, y))
        x += 25  

def show_popup_message(message):
    """Display a popup message on the screen."""
    popup = pygame.Surface((400, 200))
    popup.fill(WHITE)
    popup_rect = popup.get_rect(center=(win_width/2, win_height/2))
    text_surface = info_font.render(message, True, BLACK)
    text_rect = text_surface.get_rect(center=popup_rect.center)
    win.blit(popup, popup_rect.topleft)
    win.blit(text_surface, text_rect.topleft)
    pygame.display.update()
    pygame.time.wait(1000)

# Initialize pygame window
pygame.init()
win_width, win_height = 800, 600
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Wordle")

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

font = pygame.font.Font(None, 48)
info_font = pygame.font.Font(None, 32)  

word = choose_word()
print(word)

# Settings for input box
input_box = pygame.Rect(100, 550, 140, 32)
color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')
color = color_inactive
active = False
text = ''

running = True
guesses = []
max_attempts = 5  
attempts = 0  
while running:
    win.fill(WHITE)
    show_letter_list()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_box.collidepoint(event.pos):
                active = not active
            else:
                active = False
            color = color_active if active else color_inactive
        if event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_RETURN:
                    guess = text
                    attempts += 1
                    if attempts > max_attempts:
                        show_popup_message(f"YOU LOST! Correct word: {word}")
                        running = False
                    if guess not in choosen_words:
                        show_popup_message("Error: Enter a Turkish word!")
                    if len(guess) != len(word) or not guess.isalpha():
                        show_popup_message(f"Invalid input! Please enter a {len(word)}-letter word.")
                    else:
                        guesses.append(guess)
                        used_letters.update(set(guess))
                        
                        show_letter_list()
                        if guess == word:
                            show_popup_message("YOU WIN!")
                            running = False
                    text = ''
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode
    
    txt_surface = font.render(text, True, color)
    width = max(200, txt_surface.get_width()+10)
    input_box.w = width
    win.blit(txt_surface, (input_box.x+5, input_box.y+5))
    pygame.draw.rect(win, color, input_box, 2)
    
    info_text = f"Word Length: {len(word)} letters"
    info_surface = info_font.render(info_text, True, BLACK)
    win.blit(info_surface, (win_width - 300, 10))

    for i, guess in enumerate(guesses):
        word_letter_count = {letter: word.count(letter) for letter in set(word)}
        guess_letter_status = ['' for _ in range(len(guess))]

        for j, letter in enumerate(guess):
            if word[j] == letter:
                guess_letter_status[j] = 'green'
                word_letter_count[letter] -= 1

        for j, letter in enumerate(guess):
            if guess_letter_status[j] != 'green':
                if letter in word and word_letter_count[letter] > 0:
                    guess_letter_status[j] = 'yellow'
                    word_letter_count[letter] -= 1

        for j, letter in enumerate(guess):
            rect = pygame.Rect(j*60 + 100, i*60, 50, 50)
            pygame.draw.rect(win, BLACK, rect, 1)
            letter_color = BLACK
            if guess_letter_status[j] == 'green':
                pygame.draw.rect(win, GREEN, rect)
                letter_color = WHITE
            elif guess_letter_status[j] == 'yellow':
                pygame.draw.rect(win, YELLOW, rect)
                letter_color = BLACK
            else:
                pygame.draw.rect(win, RED, rect)
                letter_color = WHITE

            text_surface = font.render(letter.upper(), True, letter_color)
            win.blit(text_surface, (j*60 + 110, i*60 + 5))
    
    pygame.display.update()

pygame.quit()
