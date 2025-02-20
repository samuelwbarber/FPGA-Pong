import pygame
import sys

def display_screen_with_options(name):
    pygame.init()

    # Screen setup
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Game Options")

    # Colors
    background_color = (0, 0, 0)
    button_color = (255, 0, 0)
    text_color = (255, 255, 255)

    # Font setup
    font = pygame.font.Font(None, 40)

    # Texts
    one_text = font.render('1', True, text_color)
    two_text = font.render('2', True, text_color)
    welcome_text = font.render(f"Welcome {name}", True, text_color)
    replay_text = font.render('Replays', True, text_color)
    multiplayer_text = font.render('Multiplayer', True, text_color)

    # Main loop
    running = True
    while running:
        screen.fill(background_color)

        # Adjusted button positions for more separation
        button1_pos = (screen_width / 2 - 200, screen_height / 2)
        button2_pos = (screen_width / 2 + 100, screen_height / 2)

        # Welcome text position
        welcome_text_rect = welcome_text.get_rect(center=(screen_width / 2, screen_height / 2 - 100))
        screen.blit(welcome_text, welcome_text_rect)

        # Button creation and placement
        button1 = pygame.Surface((100, 50))
        button1.fill(button_color)
        button2 = pygame.Surface((100, 50))
        button2.fill(button_color)

        screen.blit(button1, button1_pos)
        screen.blit(button2, button2_pos)
        
        # Button labels
        screen.blit(one_text, (button1_pos[0] + 35, button1_pos[1] + 10))
        screen.blit(two_text, (button2_pos[0] + 35, button2_pos[1] + 10))
        
        # Descriptive texts below buttons
        screen.blit(replay_text, (button1_pos[0] + 10, button1_pos[1] + 60))
        screen.blit(multiplayer_text, (button2_pos[0] - 30, button2_pos[1] + 60))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()

                # Button click detection
                if button1.get_rect(topleft=button1_pos).collidepoint(pos):
                    return 1
                elif button2.get_rect(topleft=button2_pos).collidepoint(pos):
                    return 2

        pygame.display.flip()

# Example usage
selected_option = display_screen_with_options("PlayerName")
print(f"Selected Option: {selected_option}")
