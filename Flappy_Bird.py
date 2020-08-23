import pygame, sys, random


def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 820))
    screen.blit(floor_surface, (floor_x_pos + 500, 820))


def create_pipe():
    random_height = random.choice(pipe_height)
    new_bottom_pipe = pipe_surface.get_rect(midtop=(600, random_height))
    new_top_pipe = pipe_surface.get_rect(midbottom=(600, random_height - 230))
    return new_bottom_pipe, new_top_pipe


def collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            return False
        elif bird_rect.top <= -100 or bird_rect.bottom >= 820 :
            death_sound.play()
            return False
    return True


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 820:
            screen.blit(pipe_surface,pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird_surface, bird_movement*-1.5, 1)
    return new_bird


def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100,bird_rect.centery))
    return new_bird, new_bird_rect


def score_display(game_state):
    if game_state == "main_game":
        score_suface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_suface.get_rect(center=(250, 70))
        screen.blit(score_suface,score_rect)
    if game_state == "game_over":
        score_suface = game_font.render(f"Score : {int(score)} ", True, (255, 255, 255))
        score_rect = score_suface.get_rect(center=(250, 70))
        screen.blit(score_suface, score_rect)

        high_score_suface = game_font.render(f"High Score : {(int(high_score))} ", True, (255, 255, 255))
        high_score_rect = high_score_suface.get_rect(center=(250, 720))
        screen.blit(high_score_suface, high_score_rect)


def update_score(score, high_score):
     if score > high_score:
         high_score = score
     return high_score



#pygame.mixer.pre_init(frequency=44100, size=16, channels= 2 , buffer=1024)

pygame.init()

screen = pygame.display.set_mode((500, 900))
clock = pygame.time.Clock()
# Game Var
gravity = 0.15
bird_movement = 0
pipe_height = [520, 620, 720]
game_active = True
score = 0
high_score = 0
game_font = pygame.font.Font('04B_19.TTF', 50)
score_countdown = 100


bg_surface = pygame.image.load("assets/background-day.png").convert()
bg_surface = pygame.transform.scale(bg_surface, (500, 900))

floor_surface = pygame.image.load("assets/base.png").convert()
floor_surface = pygame.transform.scale(floor_surface, (500, 80))

bird_downflap = pygame.transform.scale(pygame.image.load("assets/bluebird-downflap.png").convert_alpha(), (60, 42))
bird_midflap = pygame.transform.scale(pygame.image.load("assets/bluebird-midflap.png").convert_alpha(),(60, 42))
bird_upflap = pygame.transform.scale(pygame.image.load("assets/bluebird-upflap.png").convert_alpha(), (60, 42))
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(100, 450))

pipe_surface = pygame.image.load("assets/pipe-green.png")
pipe_surface = pygame.transform.scale(pipe_surface, (100, 750))

game_over_surface = pygame.transform.scale(pygame.image.load("assets/message.png"), (200, 350))
game_over_rect = game_over_surface.get_rect(center=(250, 450))

flap_sound = pygame.mixer.Sound("sound/sfx_wing.wav")
hit_sound = pygame.mixer.Sound("sound/sfx_hit.wav")
score_sound = pygame.mixer.Sound("sound/sfx_point.wav")
death_sound = pygame.mixer.Sound("sound/sfx_die.wav")



SPAWNPIPE = pygame.USEREVENT
BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

pygame.time.set_timer(SPAWNPIPE, 1000)

pipe_list = []

floor_x_pos = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                flap_sound.play()
                bird_movement = -6
            if event.key == pygame.K_SPACE and game_active==False:
                game_active = True
                pipe_list.clear()
                bird_rect.center =(100, 450)
                bird_movement = 0
                score = 0

        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird_surface, bird_rect = bird_animation()

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

    screen.blit(bg_surface, (0, 0))
    if game_active:
        bird_movement += gravity
        bird_rect.centery += bird_movement
        rotated_bird = rotate_bird(bird_surface)
        screen.blit(rotated_bird, bird_rect)
        game_active = collision(pipe_list)
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
        draw_floor()
        score += 0.01
        score_display("main_game")
        score_countdown -= 1
        if score_countdown <= 0:
            score_sound.play()
            score_countdown = 100
    else:
        high_score = update_score(score, high_score)
        screen.blit(game_over_surface, game_over_rect)
        score_display("game_over")

    floor_x_pos -= 1
    if floor_x_pos == -500:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(115)




