import pygame
import random
import time

pygame.init()
display_width = 800
display_height = 600
gD = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Helo')
pygame.display.update()

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
cl = (0,0,0)
font = pygame.font.SysFont(None, 25)
pos_x = 200
pos_y = 300
pos_x_change = 0
pos_y_change = 0
clock = pygame.time.Clock()

gameExit = False

def message_to_screen(msg,color):
    screen_text = font.render(msg, True, color)
    gD.blit(screen_text, [display_width/2-50, display_height/2])


while not gameExit:

    for event in pygame.event.get():
        print(event)

        if event.type == pygame.QUIT:
            gameExit = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                cl = (random.randrange(255), random.randrange(255), random.randrange(255))

                #pygame.display.update()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                pos_x_change = -10
                pos_y_change = 0
            elif event.key == pygame.K_RIGHT:
                pos_x_change = 10
                pos_y_change = 0
            elif event.key == pygame.K_UP:
                pos_y_change = -10
                pos_x_change = 0
            elif event.key == pygame.K_DOWN:
                pos_y_change = 10
                pos_x_change = 0


    if pos_x >= display_width or pos_x < 0 or pos_y >= display_height or pos_y < 0:
        gameExit = True

    pos_x += pos_x_change
    pos_y += pos_y_change
    gD.fill(cl)
    pygame.draw.rect(gD, (0,255,0), [400, 300, 30, 30])
    gD.fill((255,0,0), rect=[pos_x, pos_y, 10, 10])
    pygame.display.update()
    clock.tick(30)

message_to_screen("Vesztettél te BÉNA", red)
pygame.display.update()
time.sleep(4)
pygame.quit()
quit()