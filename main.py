# Write your code here :-)
import pgzrun
import random
from pgzhelper import *
import pygame.locals

WIDTH = 550
HEIGHT = 500
TITLE = "Flappy Bird"

ground = Actor("ground")
ground.x = 275
ground.y = 575

bird = Actor("planenew")
bird.x = 75
bird.y = 200
# bird.images = ['bird1','bird2','bird3']
bird.images = ["planenew"]
#bird.fps = 10

gameover = Actor("game_over")
gameover.x = 275
gameover.y = 250
gameover.scale = 2

top_pipe = Actor("pipe_top")
bottom_pipe = Actor("pipe_bottom")
top_pipe.x = 550
top_pipe.y = -250
# gap = 950
gap = 150
bottom_pipe.x = 550
# bottom_pipe.y = 750
bottom_pipe.y = top_pipe.y + top_pipe.height + gap

# set up game variables
gravity = 0.3
bird.speed = 1
bird.alive = True
scroll_speed = -5
score = 0
level = 1


def on_key_down(key):
    global score
    global level
    if key == keys.SPACE:
        if bird.alive:
            bird.speed = -6.5
            sounds.wing.play()
    elif key == keys.R:
        if not (bird.alive):
            bird.alive = True
            score = 0
            level = 1
    elif key == keys.RIGHT:
        bird.x += 60


def on_mouse_down():
    global score
    if bird.alive:
        bird.speed = -6.5
    else:
        bird.alive = True
        score = 0


def update():
    global score
    global scroll_speed
    global level
    # bird
    bird.animate()
    bird.y += bird.speed
    bird.speed += gravity

    # end the game if the bird hits the top or bottom of the screen
    if bird.y > HEIGHT - 40 or bird.y < 0:
        bird.alive = False
        sounds.sfx_die.play()
    # scroll the pipes across the screen
    top_pipe.x += scroll_speed
    bottom_pipe.x += scroll_speed

    # if the pipes hit the left side of the page
    if top_pipe.x < -50:
        offset = random.uniform(-150, -350)
        top_pipe.midleft = (550, offset)
        bottom_pipe.midleft = (550, offset + top_pipe.height + gap)
        score += 1
        sounds.sfx_point.play()
    # end if game if collision
    if bird.colliderect(top_pipe) or bird.colliderect(bottom_pipe):
        bird.alive = False
        sounds.sfx_hit.play()

    if score >= 5:
        level += 1

    if level == 1:
        scroll_speed = -5
    elif level == 2:
        scroll_speed = -7


def draw():
    screen.fill((0, 0, 0))
    screen.blit("bg", (0, 0))

    if bird.alive:
        # draw the actors
        top_pipe.draw()
        bottom_pipe.draw()
        bird.draw()
        ground.draw()
    # what happens when the bird crashes
    else:
        # screen.draw.text("Click R to play again", color = "white", center=(320,300), shadow = (0.5,0.5), scolor = "black", fontsize = 30)
        gameover.draw()
        bird.x = 75
        bird.y = 150
        gravity = 0
        bird.speed = 0
        top_pipe.x = 550
        bottom_pipe.x = 550
    screen.draw.text(
        "Score: " + str(score),
        color="white",
        midtop=(50, 10),
        shadow=(0.5, 0.5),
        scolor="black",
        fontsize=30,
    )


pgzrun.go()
