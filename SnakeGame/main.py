import pygame
import sys
import random

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Load sound effects
move_sound = pygame.mixer.Sound("sounds/move_sound.mp3")
eat_sound = pygame.mixer.Sound("sounds/eat_sound.mp3")
dead_sound = pygame.mixer.Sound("sounds/dead_sound.mp3")

# Game parameters
cell_size = 20
background_color = (0, 0, 0)
snake_color = (0, 255, 0)
apple_color = (255, 0, 0)

# Initialize the window
window_width = 600
window_height = 400
window = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)
pygame.display.set_caption("Snake Game")

# Initialize the snake
snake = [(100, 100), (90, 100), (80, 100)]
direction = (1, 0)  # Initialize movement to the right

# Initialize the apple
apple = (random.randint(0, window_width // cell_size - 1) * cell_size,
         random.randint(0, window_height // cell_size - 1) * cell_size)

# Initialize the score, level, and timer
score = 0
level = 1
timer = 0
start_time = pygame.time.get_ticks()

# Initialize the font for the score display
font = pygame.font.Font(None, 36)

# Pause flag
paused = False

# Game over flag
game_over = False

# Function to display the snake
def display_snake():
    for segment in snake:
        pygame.draw.rect(window, snake_color, (segment[0], segment[1], cell_size, cell_size))

# Function to display the Game Over screen
def display_game_over():
    game_over_text = font.render(f"Game Over - Score: {score} - Level: {level} - Time: {timer}s", True, (255, 255, 255))
    text_rect = game_over_text.get_rect(center=(window_width // 2, window_height // 2 - 30))
    window.blit(game_over_text, text_rect)

    restart_text = font.render("Press SPACE to Restart", True, (255, 255, 255))
    restart_rect = restart_text.get_rect(center=(window_width // 2, window_height // 2 + 30))
    window.blit(restart_text, restart_rect)

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Handle keys to change snake direction
        elif event.type == pygame.KEYDOWN:
            if not game_over:
                if event.key == pygame.K_UP and direction != (0, 1):
                    direction = (0, -1)
                elif event.key == pygame.K_DOWN and direction != (0, -1):
                    direction = (0, 1)
                elif event.key == pygame.K_LEFT and direction != (1, 0):
                    direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                    direction = (1, 0)

                # Toggle pause on space bar
                elif event.key == pygame.K_SPACE:
                    paused = not paused

            # Restart the game on space bar after Game Over
            elif event.key == pygame.K_SPACE:
                snake = [(100, 100), (90, 100), (80, 100)]
                direction = (1, 0)
                apple = (random.randint(0, window_width // cell_size - 1) * cell_size,
                         random.randint(0, window_height // cell_size - 1) * cell_size)
                score = 0
                level = 1
                timer = 0
                start_time = pygame.time.get_ticks()
                game_over = False

        # Handle window resize
        elif event.type == pygame.VIDEORESIZE:
            window_width, window_height = event.size
            window = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)

    # Check if the game is over
    if not paused and not game_over:
        # Move the snake
        head_x, head_y = snake[0]
        new_head = (head_x + direction[0] * cell_size, head_y + direction[1] * cell_size)
        snake.insert(0, new_head)

        # Check for collisions with the borders
        if not (0 <= new_head[0] < window_width and 0 <= new_head[1] < window_height):
            game_over = True
            dead_sound.play()

        # Check for collision with the snake body
        if len(snake) > 1 and new_head in snake[1:]:
            game_over = True
            dead_sound.play()

        # Check for collision with the apple
        if new_head == apple:
            apple = (random.randint(0, window_width // cell_size - 1) * cell_size,
                     random.randint(0, window_height // cell_size - 1) * cell_size)
            score += 1  # Increase the score when the snake eats the apple
            eat_sound.play()

            # Level up every 5 points
            if score % 5 == 0:
                level += 1
                move_sound.set_volume(0.5 + level * 0.1)  # Adjust the volume based on the level

        else:
            # If no collision with the apple, remove the last part of the snake
            snake.pop()
            move_sound.play()

        # Update the timer
        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
        if elapsed_time != timer:
            timer = elapsed_time

    # Draw game elements
    window.fill(background_color)

    if not game_over:
        # Display the score, level, and timer at the top center
        game_info_text = font.render(f"Score: {score} - Level: {level} - Time: {timer}s", True, (255, 255, 255))
        text_rect = game_info_text.get_rect(center=(window_width // 2, 20))
        window.blit(game_info_text, text_rect)

        display_snake()
        pygame.draw.rect(window, apple_color, (apple[0], apple[1], cell_size, cell_size))

        # Display pause text when paused
        if paused:
            pause_text = font.render("Paused", True, (255, 255, 255))
            pause_rect = pause_text.get_rect(center=(window_width // 2, window_height // 2))
            window.blit(pause_text, pause_rect)

    else:
        display_game_over()

    # Refresh the screen
    pygame.display.flip()

    # Control the frame rate
    pygame.time.Clock().tick(10)
