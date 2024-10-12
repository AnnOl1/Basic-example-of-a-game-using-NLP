import pygame
import random
import spacy

pygame.init()

# screen
WIDTH, HEIGHT = 500, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")

# color
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
current_color = random.choice(colors)

# character
player = pygame.Rect(WIDTH // 2 - 25, HEIGHT // 2 - 25, 50, 50)
speed = 5
jump_height = 100
is_jumping = False
jump_velocity = 15  
gravity = 1  

nlp = spacy.load("en_core_web_sm")

# text input field
input_box = pygame.Rect(10, HEIGHT - 40, WIDTH - 20, 30)
input_text = ''  

def parse_command(command):
    doc = nlp(command.lower())
    for token in doc:
        if token.lemma_ == "move" and "left" in command:
            return "move_left"
        elif token.lemma_ == "move" and "right" in command:
            return "move_right"
        elif token.lemma_ == "jump":
            return "jump"
        elif token.lemma_ == "change" and "color" in command:
            return "change_color"
    return "unknown_command"

def handle_action(action):
    global player, current_color, is_jumping, jump_velocity
    if action == "move_left":
        player.x -= speed
    elif action == "move_right":
        player.x += speed
    elif action == "jump" and not is_jumping:
        is_jumping = True
        jump_velocity = -15  
    elif action == "change_color":
        current_color = random.choice(colors)

running = True
clock = pygame.time.Clock()

player_y_original = player.y  

while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # handling keyboard input
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:  # Enter
                action = parse_command(input_text)
                handle_action(action)
                input_text = ''  # Reset
            elif event.key == pygame.K_BACKSPACE:  # Delete symbol
                input_text = input_text[:-1]
            else:
                input_text += event.unicode  # Adding a symbol to a command

    # Jump
    if is_jumping:
        player.y += jump_velocity 
        jump_velocity += gravity  

        if player.y >= player_y_original:
            player.y = player_y_original  
            is_jumping = False  

    # Draw a character
    pygame.draw.rect(screen, current_color, player)

    # Draw an input field
    pygame.draw.rect(screen, GRAY, input_box, 2)  # Рамка вокруг поля для ввода

    # Command text on screen inside the field
    font = pygame.font.Font(None, 32)
    command_surface = font.render(input_text, True, BLACK)
    screen.blit(command_surface, (input_box.x + 5, input_box.y + 5))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
