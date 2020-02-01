import pygame
import random

pygame.init()

gD = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Helo')
pygame.display.update()
cl = (0,0,0)
pos_x = 200
pos_y = 300
pos_x_change = 0
clock = pygame.time.Clock()

gameExit = False

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
            if event.key == pygame.K_RIGHT:
                pos_x_change = 10
            if event.key == pygame.K_UP:
                pos_y -= 10
            if event.key == pygame.K_DOWN:
                pos_y += 10

    pos_x += pos_x_change
    gD.fill(cl)
    pygame.draw.rect(gD, (0,255,0), [400, 300, 30, 30])
    gD.fill((255,0,0), rect=[pos_x, pos_y, 10, 10])
    pygame.display.update()
    clock.tick(15)

pygame.quit()
quit()