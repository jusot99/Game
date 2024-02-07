import pygame
import sys
from pygame.math import Vector2
import random
import argparse
import socket
import pickle
import time

# Initialize Pygame mixer
pygame.mixer.init()

# Constants
WIDTH, HEIGHT = 800, 600
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_SIZE = 20
FPS = 60

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PLAYER_COLOR = (0, 128, 255)  # Blue
OPPONENT_COLOR = (255, 0, 0)  # Red
BALL_COLOR = (255, 255, 0)  # Yellow

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Game")

# Initialize paddles and ball
class Player:
    def __init__(self, x, y, width, height, color, client):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.power_counter = 0
        self.client = client

    def move(self, direction):
        if direction == "UP" and self.rect.top > 0:
            self.rect.y -= 5
            self.send_player_input()
        elif direction == "DOWN" and self.rect.bottom < HEIGHT:
            self.rect.y += 5
            self.send_player_input()

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def send_player_input(self):
        if self.client:
            self.client.send_player_input('player1', self.rect.y)

class Computer:
    def __init__(self, x, y, width, height, color, ball, client):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.ball = ball
        self.power_counter = 0
        self.client = client

    def move(self):
        if self.ball.rect.centery < self.rect.centery and self.rect.top > 0:
            self.rect.y -= 5
            self.send_player_input()
        elif self.ball.rect.centery > self.rect.centery and self.rect.bottom < HEIGHT:
            self.rect.y += 5
            self.send_player_input()

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def send_player_input(self):
        if self.client:
            self.client.send_player_input('player2', self.rect.y)

class Ball:
    def __init__(self, x, y, size, color):
        self.rect = pygame.Rect(x, y, size, size)
        self.color = color

    def draw(self, screen):
        pygame.draw.ellipse(screen, self.color, self.rect)

# PongClient class for handling multiplayer functionality
class PongClient:
    def __init__(self, host, port):
        self.server_address = (host, port)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.game_state = None

    def connect_to_server(self):
        self.client_socket.connect(self.server_address)

    def receive_game_state(self):
        data = self.client_socket.recv(1024)
        if data:
            self.game_state = pickle.loads(data)

    def send_player_input(self, player, y):
        player_input = {'player': player, 'y': y}
        serialized_input = pickle.dumps(player_input)
        self.client_socket.send(serialized_input)

    def close_connection(self):
        self.client_socket.close()

# Sounds
paddle_hit_sound = pygame.mixer.Sound('sounds/8-bit-jump.mp3')
goal_sound = pygame.mixer.Sound('sounds/8-bit-hit.mp3')
power_hit_sound = pygame.mixer.Sound('sounds/8-bit-hard.mp3')

# Initialize Pygame
pygame.init()

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Pong Game")
parser.add_argument('--multiplayer', action='store_true', help='Play in multiplayer mode')
parser.add_argument('--computer', action='store_true', help='Play against the computer in single-player mode')
args = parser.parse_args()

if args.multiplayer:
    print("Starting Pong Game in multiplayer mode...")

    # Connect to the server
    client = PongClient(host='127.0.0.1', port=5555)
    client.connect_to_server()

    # Wait for both Player1 and Player2 to connect
    while True:
        client.receive_game_state()
        if client.game_state and 'player1' in client.game_state and 'player2' in client.game_state:
            break
        time.sleep(0.1)

else:
    print("Starting Pong Game in single-player mode...")
    client = None

# Initialize paddles and ball
player = Player(50, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT, PLAYER_COLOR, client)
computer = Computer(WIDTH - 50 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT, OPPONENT_COLOR, None, client)

ball = Ball(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_COLOR)
computer.ball = ball

# Initialize ball movement
ball_velocity = Vector2(random.choice([-5, 5]), random.choice([-5, 5]))

# Initialize scores
player1_score = 0
player2_score = 0
font = pygame.font.Font(None, 36)

# Game loop
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if client:
                client.close_connection()
            pygame.quit()
            sys.exit()

    # Move player paddle
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player.rect.top > 0:
        player.move("UP")
    if keys[pygame.K_DOWN] and player.rect.bottom < HEIGHT:
        player.move("DOWN")

    # Move computer paddle in single-player mode
    if not args.multiplayer and args.computer:
        computer.move()

    if client:
        # Receive and update game state in multiplayer mode
        client.receive_game_state()
        if client.game_state:
            player.rect.y = client.game_state['player1']['y']
            computer.rect.y = client.game_state['player2']['y']
            ball.rect.x = client.game_state['ball']['x']
            ball.rect.y = client.game_state['ball']['y']
            player1_score = client.game_state['score']['player1']
            player2_score = client.game_state['score']['player2']

    # Move the ball
    ball.rect.x += ball_velocity.x
    ball.rect.y += ball_velocity.y

    # Ball collisions with walls
    if ball.rect.top <= 0 or ball.rect.bottom >= HEIGHT:
        ball_velocity.y = -ball_velocity.y

    # Ball collisions with paddles
    if ball.rect.colliderect(player.rect):
        ball_velocity.x = abs(ball_velocity.x)  # Make the ball move away from the paddle
        ball_velocity.y = random.uniform(-5, 5)   # Randomize the vertical direction
        paddle_hit_sound.play()

        # Increase power-up counter
        player.power_counter += 1
        if player.power_counter == 5:
            player.power_counter = 0
            power_hit_sound.play()
            ball_velocity *= 1.5  # Increase ball speed after 5 successful hits

    elif ball.rect.colliderect(computer.rect):
        ball_velocity.x = -abs(ball_velocity.x)  # Make the ball move away from the paddle
        ball_velocity.y = random.uniform(-5, 5)   # Randomize the vertical direction
        paddle_hit_sound.play()

        # Increase power-up counter
        computer.power_counter += 1
        if computer.power_counter == 5:
            computer.power_counter = 0
            power_hit_sound.play()
            ball_velocity *= 1.5  # Increase ball speed after 5 successful hits

    # Ball out of bounds (score)
    if ball.rect.left <= 0:
        if client:
            client.send_player_input('player1', player.rect.y)
            client.send_player_input('player2', computer.rect.y)
        player2_score += 1
        ball.rect.x = WIDTH // 2 - BALL_SIZE // 2
        ball.rect.y = HEIGHT // 2 - BALL_SIZE // 2
        ball_velocity = Vector2(random.choice([-5, 5]), random.choice([-5, 5]))
        goal_sound.play()

    elif ball.rect.right >= WIDTH:
        if client:
            client.send_player_input('player1', player.rect.y)
            client.send_player_input('player2', computer.rect.y)
        player1_score += 1
        ball.rect.x = WIDTH // 2 - BALL_SIZE // 2
        ball.rect.y = HEIGHT // 2 - BALL_SIZE // 2
        ball_velocity = Vector2(random.choice([-5, 5]), random.choice([-5, 5]))
        goal_sound.play()

    # Clear the screen
    screen.fill(BLACK)

    # Draw paddles and ball
    player.draw(screen)
    computer.draw(screen)
    ball.draw(screen)

    # Draw the middle line (Yeah but it's optional)
    pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

    # Draw scores
    player_text = font.render(f"Player1: {player1_score}", True, WHITE)
    screen.blit(player_text, (20, 20))

    computer_text = font.render(f"Player2: {player2_score}", True, WHITE)
    screen.blit(computer_text, (WIDTH - 220, 20))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)
