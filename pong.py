import pygame
import sys
import random
from pygame.locals import *

class Button:
    def __init__(self, text, x, y, width, height, font_size, inactive_color, active_color, action=None):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font_size = font_size
        self.inactive_color = inactive_color
        self.active_color = active_color
        self.action = action
        self.is_clicked = False

    def draw(self, win):
        mouse_pos = pygame.mouse.get_pos()
        button_rect = pygame.Rect(self.x, self.y, self.width, self.height)

        if button_rect.collidepoint(mouse_pos) or self.is_clicked:
            pygame.draw.rect(win, self.inactive_color, button_rect)
            pygame.draw.rect(win, WHITE, button_rect, 2)
        else:
            pygame.draw.rect(win, self.inactive_color, button_rect)

        font = pygame.font.Font(None, self.font_size)
        text_surf = font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=button_rect.center)
        win.blit(text_surf, text_rect)

        if button_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
            self.is_clicked = True
            return True
        return False

# beofre any funcs run
pygame.init()

WINDOW_WIDTH, WINDOW_HEIGHT = 600, 400
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 60
BALL_SIZE = 15
PADDLE_SPEED = 5
BALL_SPEED_X, BALL_SPEED_Y = 5.25, 5.25
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 60

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Pong Game')
fpsClock = pygame.time.Clock()

def draw_paddle(paddle):
    pygame.draw.rect(window, WHITE, paddle)

def draw_ball(ball):
    pygame.draw.ellipse(window, WHITE, ball)

def move_ball(ball, ball_speed_x, ball_speed_y):
    ball.x += ball_speed_x
    ball.y += ball_speed_y
    return ball

def check_collision(ball, ball_speed_x, ball_speed_y):
    if ball.top <= 0 or ball.bottom >= WINDOW_HEIGHT:
        ball_speed_y = -ball_speed_y
    return ball_speed_x, ball_speed_y

def check_paddle_collision(ball, paddle1, paddle2, ball_speed_x):
    if ball.colliderect(paddle1) or ball.colliderect(paddle2):
        ball_speed_x = -ball_speed_x
    return ball_speed_x

def ai_movement(paddle, ball, speed):
    if paddle.centery < ball.centery:
        paddle.y += speed
    else:
        paddle.y -= speed
    return paddle

def pause_screen():
    resume_button = Button("Resume", 225, 100, 150, 50, 36, BLACK, WHITE)
    home_button = Button("Home", 225, 175, 150, 50, 36, BLACK, WHITE)
    restart_button = Button("Restart", 225, 250, 150, 50, 36, BLACK, WHITE)

    paused = True
    while paused:
        window.fill(BLACK)
        if resume_button.draw(window):
            return "resume"
        if home_button.draw(window):
            return "home"
        if restart_button.draw(window):
            return "restart"

        pygame.display.flip()
        fpsClock.tick(FPS)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

def loading_screen():
    BUTTON_WIDTH = WINDOW_WIDTH // 6
    BUTTON_HEIGHT = 50
    BUTTON_SPACING_X = WINDOW_WIDTH // 15
    BUTTON_SPACING_Y = WINDOW_HEIGHT // 8

    MODE_BUTTON_Y = WINDOW_HEIGHT // 4
    TIME_BUTTON_Y = WINDOW_HEIGHT // 2

    mode_button_x1 = WINDOW_WIDTH // 2 - BUTTON_WIDTH - BUTTON_SPACING_X // 2
    mode_button_x2 = WINDOW_WIDTH // 2 + BUTTON_SPACING_X // 2

    time_button_x1 = WINDOW_WIDTH // 2 - (3 * BUTTON_WIDTH + 2 * BUTTON_SPACING_X) // 2
    time_button_x2 = time_button_x1 + BUTTON_WIDTH + BUTTON_SPACING_X
    time_button_x3 = time_button_x2 + BUTTON_WIDTH + BUTTON_SPACING_X
    time_button_x4 = time_button_x3 + BUTTON_WIDTH + BUTTON_SPACING_X

    mode_buttons = [
        Button("PvP", mode_button_x1, MODE_BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT, 36, BLACK, WHITE, "pvp"),
        Button("AI", mode_button_x2, MODE_BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT, 36, BLACK, WHITE, "ai")
    ]

    time_buttons = [
        Button("1 min", time_button_x1, TIME_BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT, 36, BLACK, WHITE, 60),
        Button("3 min", time_button_x2, TIME_BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT, 36, BLACK, WHITE, 180),
        Button("Endless", time_button_x3, TIME_BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT, 36, BLACK, WHITE, -1)
        # Button("None", time_button_x4, TIME_BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT, 36, BLACK, WHITE, -1)
    ]


    mode = None
    game_length = None

    running = True
    while running:
        window.fill(BLACK)
        for button in mode_buttons:
            if button.draw(window):
                mode = button.action

        for button in time_buttons:
            if button.draw(window):
                game_length = button.action

        if mode and game_length is not None:
            return mode, game_length

        pygame.display.flip()
        fpsClock.tick(FPS)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

def end_game_screen(score1, score2):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_h:
                    return

        window.fill(BLACK)
        font = pygame.font.Font(None, 36)
        text = font.render(f"Game Over! Final Score - Player 1: {score1}, Player 2: {score2}", True, WHITE)
        text2 = font.render("Press H for Home", True, WHITE)
        text_rect = text.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 20))
        text2_rect = text2.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 20))
        window.blit(text, text_rect)
        window.blit(text2, text2_rect)
        pygame.display.flip()
        fpsClock.tick(FPS)



def main():
    while True:
        font = pygame.font.Font(None, 36)

        mode, game_length = loading_screen()
        is_ai = mode == "ai"
        start_time = pygame.time.get_ticks() if game_length > 0 else None

        def start(): 
            score1, score2 = 0, 0
            ball_in_play = False
            paddle1 = pygame.Rect(10, WINDOW_HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
            paddle2 = pygame.Rect(WINDOW_WIDTH - 20, WINDOW_HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
            ball = pygame.Rect(WINDOW_WIDTH // 2 - BALL_SIZE // 2, WINDOW_HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)

            ball_speed_x, ball_speed_y = BALL_SPEED_X, BALL_SPEED_Y
            player_speed = PADDLE_SPEED

            running = True
            while running:
                if game_length > 0:
                    current_time = pygame.time.get_ticks()
                    if current_time - start_time >= game_length * 1000:
                        end_game_screen(score1, score2)
                        return

                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == KEYDOWN:
                        if event.key == K_p:
                            pause_action = pause_screen()
                            if pause_action == "home":
                                return
                            elif pause_action == "restart":
                                start()
                                return
                        if not ball_in_play and event.key == K_SPACE:
                            ball_in_play = True
                            ball_speed_x = BALL_SPEED_X * random.choice([-1, 1]) 
                            ball_speed_y = BALL_SPEED_Y * random.choice([-1, 1])

                keys = pygame.key.get_pressed()
                if keys[pygame.K_w]:
                    paddle1.y -= PADDLE_SPEED
                if keys[pygame.K_s]:
                    paddle1.y += PADDLE_SPEED

                if not is_ai:
                    if keys[pygame.K_UP]:
                        paddle2.y -= PADDLE_SPEED
                    if keys[pygame.K_DOWN]:
                        paddle2.y += PADDLE_SPEED

                    paddle2.y = max(paddle2.y, 0)
                    paddle2.y = min(paddle2.y, WINDOW_HEIGHT - PADDLE_HEIGHT)

                paddle1.y = max(paddle1.y, 0)
                paddle1.y = min(paddle1.y, WINDOW_HEIGHT - PADDLE_HEIGHT)

                if ball_in_play:
                    ball = move_ball(ball, ball_speed_x, ball_speed_y)
                    ball_speed_x, ball_speed_y = check_collision(ball, ball_speed_x, ball_speed_y)
                    ball_speed_x = check_paddle_collision(ball, paddle1, paddle2, ball_speed_x)

                if ball.left <= 0 or ball.right >= WINDOW_WIDTH:
                    if ball.left <= 0:
                        score2 += 1
                    else:
                        score1 += 1
                    ball_in_play = False
                    ball = pygame.Rect(WINDOW_WIDTH // 2 - BALL_SIZE // 2, WINDOW_HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
                    ball_speed_x, ball_speed_y = 0, 0

                if is_ai:
                    paddle2 = ai_movement(paddle2, ball, player_speed)

                window.fill(BLACK)

                if game_length > 0:
                    elapsed_time = (current_time - start_time) // 1000
                    remaining_time = max(game_length - elapsed_time, 0)
                    timer_text = font.render(f"Time Left: {remaining_time}s", True, WHITE)
                    timer_rect = timer_text.get_rect(center=(WINDOW_WIDTH // 2, 50))
                    window.blit(timer_text, timer_rect)

                score_text = font.render(f"Player 1: {score1}  Player 2: {score2}", True, WHITE)
                score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, 20))
                window.blit(score_text, score_rect)

                draw_paddle(paddle1)
                draw_paddle(paddle2)
                draw_ball(ball)

                pygame.display.flip()
                fpsClock.tick(FPS)

        start()

if __name__ == "__main__":
    main()