import pygame
import random
import time
from collections import deque

pygame.init()

gameDisplay = pygame.display.set_mode((600, 600))
pygame.display.set_caption('Poly_cortex_P300')
pygame.display.update()
clock = pygame.time.Clock()

# Color
white = (255, 255, 255)
grey = (105, 105, 105)
sys_font = pygame.font.SysFont("None", 100)
dist = 85
shift = 70

alphNumList = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
                '0','1', '2', '3', '4', '5', '6', '7', '8', '9']

timeFlashQ = deque([0, 0, 0, 0])

def randColumnOrRow():
    columnOrRow = random.randrange(2)
    columnOrRowNum = random.randrange(6)
    return columnOrRow, columnOrRowNum

p300Exit = False

millisInit = int(round(time.time()*1000))

while not p300Exit:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            p300Exit = True

    columnOrRow, columnOrRowNum = randColumnOrRow()

    for i in range(6):
        for j in range(6):

            if columnOrRow == 0 and j == columnOrRowNum:
                color = white
            elif columnOrRow == 1 and i == columnOrRowNum:
                color = white
            else:
                color = grey

            rendered = sys_font.render(alphNumList[6*j + i], 0, color)
            gameDisplay.blit(rendered, (dist*i + shift, dist*j + shift))

    time.sleep(0.100)

    # To find back which letter has been flashed at what time:
    # The program seems to take about 5 ms to run one time the loop
    timeFlashQ.append((int(round(time.time()*1000)) - millisInit, columnOrRow, columnOrRowNum))
    timeFlashQ.popleft()

    print(timeFlashQ)

    pygame.display.update()

pygame.quit()
quit()



