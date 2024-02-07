import pygame
import random
import time
import sys

pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Hangman Game")

# Set up colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up fonts
font = pygame.font.Font(None, 36)

# Set up game variables
words = ["python", "hangman", "coding", "pygame", "github", "jusot", "love"]
word = random.choice(words)
guessed_letters = set()
max_attempts = 6
attempts = 0

# Animation variables
animate_text = False
animation_start_time = 0
animation_duration = 1.5  # seconds

# Word database
custom_words = ["custom", "database", "animation", "restart", "quit"]
custom_word = ""

# Function to display messages
def display_message(message, x, y):
    text = font.render(message, True, BLACK)
    win.blit(text, (x, y))

# Function to start animation
def start_animation():
    global animate_text, animation_start_time
    animate_text = True
    animation_start_time = time.time()

# Main game loop
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        elif event.type == pygame.KEYDOWN:
            if event.key in range(65, 91) or event.key in range(97, 123):
                letter = chr(event.key).lower()

                if letter not in guessed_letters:
                    guessed_letters.add(letter)

                    if letter not in word:
                        attempts += 1

                # Check for restart or quit
                if letter == "r":
                    # Restart the game
                    word = random.choice(words)
                    guessed_letters = set()
                    attempts = 0
                    animate_text = False
                elif letter == "q":
                    # Quit the game
                    run = False

                # Check for animation
                if letter == "a":
                    start_animation()

        # Handle window resize
        elif event.type == pygame.VIDEORESIZE:
            window_width, window_height = event.size
            win = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)

    # Draw the hangman
    win.fill(WHITE)
    pygame.draw.line(win, BLACK, (400, 50), (400, 500), 5)
    pygame.draw.line(win, BLACK, (400, 50), (700, 50), 5)
    pygame.draw.line(win, BLACK, (700, 50), (700, 100), 5)

    hangman_parts = [
        ((700, 125), 25),
        ((700, 150), (700, 300)),
        ((700, 200), (650, 250)),
        ((700, 200), (750, 250)),
        ((700, 300), (650, 350)),
        ((700, 300), (750, 350)),
    ]

    for i in range(attempts):
        part = hangman_parts[i]
        if isinstance(part[1], int):
            pygame.draw.circle(win, BLACK, part[0], part[1], 5)
        else:
            pygame.draw.line(win, BLACK, part[0], part[1], 5)

    # Draw the word with blanks and guessed letters
    display_word = ""
    for letter in word:
        if letter in guessed_letters:
            display_word += letter + " "
        else:
            display_word += "_ "
    text = font.render(display_word, True, BLACK)
    win.blit(text, (50, 400))

    # Check for win or lose
    if set(word) <= guessed_letters:
        display_message("You Win!", 350, 250)
        start_animation()  # Start win animation
        # Reset word for the next game
        word = random.choice(words)
        guessed_letters = set()
        attempts = 0
    elif attempts >= max_attempts:
        display_message("You Lose! The word was {}".format(word), 300, 250)
        start_animation()  # Start lose animation
        # Reset word for the next game
        word = random.choice(words)
        guessed_letters = set()
        attempts = 0

    # User Interaction
    display_message("Guess a letter:", 50, 550)
    display_message("Guessed Letters: " + ", ".join(sorted(guessed_letters)), 50, 580)
    display_message("Attempts left: {}".format(max_attempts - attempts), 600, 580)

    # Word Database
    if custom_word:
        display_message("Custom Word: " + custom_word, 50, 520)

    # Animation
    if animate_text:
        current_time = time.time()
        elapsed_time = current_time - animation_start_time
        if elapsed_time < animation_duration:
            display_message("Animation in progress!", 300, 500)

    pygame.display.update()

# Pause for a moment before quitting
time.sleep(2)
pygame.quit()
sys.exit()
