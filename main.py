import pygame
import random
import sys
import os

pygame.init()

WIDTH, HEIGHT = (1000, 400)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("T-Rex")
pygame.font.init()

FPS = 60

T_REX_WIDTH, T_REX_HEIGHT = (64, 68)
CROUCH_WIDTH, CROUCH_HEIGHT = (86, 42)
CACTUS_WIDTH, CACTUS_HEIGHT = (36, 80)
BIRD_WIDTH, BIRD_HEIGHT = (56, 40)

BACKGROUND = pygame.image.load(os.path.join('Assets', 'background.png'))
PATH = pygame.image.load(os.path.join('Assets', 'path.png'))
T_REX_1 = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 't-rex.png')), (T_REX_WIDTH, T_REX_HEIGHT))
T_REX_2 = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 't-rex2.png')), (T_REX_WIDTH, T_REX_HEIGHT))
T_REX_JUMP = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 't-rex_jump.png')),
                                    (T_REX_WIDTH, T_REX_HEIGHT))
T_REX_CROUCH = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 't-rex_crouch.png')),
                                      (CROUCH_WIDTH, CROUCH_HEIGHT))
T_REX_CROUCH_2 = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 't-rex_crouch2.png')),
                                        (CROUCH_WIDTH, CROUCH_HEIGHT))
CACTUS = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'cactus.png')), (CACTUS_WIDTH, CACTUS_HEIGHT))
BIRD_1 = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'bird.png')), (BIRD_WIDTH, BIRD_HEIGHT))
BIRD_2 = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'bird2.png')), (BIRD_WIDTH, BIRD_HEIGHT))

JUMP_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'jump.wav'))
DIE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'die.wav'))

DARK_GREY = (96, 96, 96)
GREY = (160, 160, 160)
SMALL_FONT = pygame.font.SysFont('Agency FB', 40)
BIG_FONT = pygame.font.SysFont('Agency FB', 76)


def background_move(background):
    background.x -= 1
    if background.x < -1000:
        background.x = 0


def path_move(path, vel):
    path.x -= vel
    if path.x < -1000:
        path.x = 0


def jump(t_rex, grav, jumping):
    t_rex.y -= grav
    grav -= 1
    if grav < -18:
        jumping = False
        grav = 18
    return jumping, grav


def main(high_score=0):
    grav = 18
    jumping = False
    vel = 5
    score = 0

    background = pygame.Rect(0, 0, 1, 1)
    path = pygame.Rect(0, 200, 1, 1)
    t_rex = pygame.Rect(2, 228, T_REX_WIDTH, T_REX_HEIGHT)

    cacti = [pygame.Rect(1000, 226, CACTUS_WIDTH, CACTUS_HEIGHT)]
    birds = [pygame.Rect(3600, 220, BIRD_WIDTH, BIRD_HEIGHT)]

    clock = pygame.time.Clock()

    last_update = pygame.time.get_ticks()
    animation_cooldown = 100
    animation_number = 0
    walk_animation_list = [T_REX_1, T_REX_2]
    crouch_animation_list = [T_REX_CROUCH, T_REX_CROUCH_2]
    bird_animation_list = [BIRD_1, BIRD_2]

    checkpoints = [50 * i for i in range(1, 6)]

    run = True
    game_over = False

    while run:
        clock.tick(FPS)
        keys_pressed = pygame.key.get_pressed()

        # exiting the game using quit button and jumping by pressing space button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_SPACE) and not keys_pressed[pygame.K_s] and not jumping and not game_over:
                    jumping = True
                    JUMP_SOUND.play()

        if not game_over:
            # moving the background
            background_move(background)
            path_move(path, vel)

            # walking and crouching animations, increasing the score after changing the animation
            current_time = pygame.time.get_ticks()
            if current_time - last_update >= animation_cooldown:
                animation_number += 1
                last_update = current_time
                if animation_number == 2:
                    animation_number = 0
                    score += 1

            # changing the x and y when crouching and jumping
            if keys_pressed[pygame.K_s] and not jumping:
                t_rex = pygame.Rect(2, 266, CROUCH_WIDTH, CROUCH_HEIGHT)
            elif jumping:
                jumping, grav = jump(t_rex, grav, jumping)
            else:
                t_rex = pygame.Rect(2, 238, T_REX_WIDTH, T_REX_HEIGHT)

            # adding cacti and birds to a list
            if cacti[-1][0] < 800:
                cacti.append(pygame.Rect(random.randint(1100, 1800), 226, CACTUS_WIDTH, CACTUS_HEIGHT))
            if birds[-1][0] < 100:
                birds.append(pygame.Rect(random.randint(3600, 4000), 220, BIRD_WIDTH, BIRD_HEIGHT))

            # drawing the background and path
            WIN.blit(BACKGROUND, (background.x, background.y))
            WIN.blit(PATH, (path.x, path.y))

            # drawing the score
            zeros = "0" * (5 - len(str(score)))
            score_text = SMALL_FONT.render(f"{zeros}{score}", True, DARK_GREY)
            WIN.blit(score_text, (WIDTH - 100, 10))

            # drawing the high score
            zeros = "0" * (5 - len(str(high_score)))
            high_score_text = SMALL_FONT.render(f"HI {zeros}{high_score}", True, GREY)
            WIN.blit(high_score_text, (WIDTH - 240, 10))

            # drawing and moving cacti, removing when off-screen
            for cactus in cacti:
                cactus.x -= vel
                WIN.blit(CACTUS, (cactus.x, cactus.y))
                if cactus.x < 0 - CACTUS_WIDTH:
                    cacti.remove(cactus)

            # drawing and moving birds, removing when off-screen
            for bird in birds:
                bird.x -= vel + 3
                WIN.blit(bird_animation_list[animation_number], (bird.x, bird.y))
                if bird.x < 0 - BIRD_WIDTH:
                    birds.remove(bird)

            # drawing the dino
            if keys_pressed[pygame.K_s] and not jumping:
                WIN.blit(crouch_animation_list[animation_number], (2, 266))
            elif jumping:
                WIN.blit(T_REX_JUMP, (4, t_rex.y))
            else:
                WIN.blit(walk_animation_list[animation_number], (2, 238))

            # increasing the velocity of obstacles and path after reaching the checkpoints
            for checkpoint in checkpoints:
                if score > checkpoint:
                    vel = checkpoint / 50 + 5

            # losing the game when t rex collides with cactus or bird
            for cactus in cacti:
                if cactus.colliderect(t_rex):
                    game_over = True
                    DIE_SOUND.play()
            for bird in birds:
                if bird.colliderect(t_rex):
                    game_over = True
                    DIE_SOUND.play()

        # drawing game over prompts, restarting the game after pressing an "enter", updating the high score
        else:
            game_over_text_1 = BIG_FONT.render(f"GAME OVER", True, DARK_GREY)
            game_over_text_2 = SMALL_FONT.render(f"PRESS ENTER TO PLAY AGAIN", True, DARK_GREY)
            WIN.blit(game_over_text_1,
                     (WIDTH / 2 - game_over_text_1.get_width() / 2, HEIGHT / 2 - game_over_text_1.get_height()))
            WIN.blit(game_over_text_2,
                     (WIDTH / 2 - game_over_text_2.get_width() / 2, HEIGHT / 2))
            if score > high_score:
                high_score = score
            if keys_pressed[pygame.K_RETURN]:
                main(high_score)

        pygame.display.update()


if __name__ == '__main__':
    main()
