import json
import pygame
import datetime

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
width, height = screen.get_size()
clock = pygame.time.Clock()
done = False

font = pygame.font.SysFont(None, 72)


while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            done = True

    data = json.load(open('motor', 'r+'))
    screen.fill((255, 255, 255))
    newtime = datetime.datetime.now()
    text = font.render(str(data['vehicleVelocity']), True, (0, 128, 0))
    screen.blit(text, (
            screen.get_width()//2 - text.get_width() // 2,
            screen.get_height()//2 - text.get_height() // 2))

    pygame.display.flip()
    clock.tick(60)
