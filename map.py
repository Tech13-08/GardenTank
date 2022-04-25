import math
import pygame
import numpy as np

class Map:
    def __init__(self, screenW, screenH, height, width, boxSize):
        self.width = width
        self.height = height
        self.screenW = screenW
        self.screenH = screenH
        self.map_array = np.zeros((height, width), dtype=int)
        self.water_direction = "left"
        self.box_size = boxSize
        self.path_array = []
        self.x = math.floor((screenW - (self.box_size * self.width)) / 2)
        self.y = math.floor((screenH - (self.box_size * self.height)) / 2)
        self.bgC = (211, 211, 211)
        self.borderC = (0, 0, 0)
        self.plantC = (0, 153, 0)
        self.obstacleC = (102, 51, 0)
        self.pathC = (255, 0, 0)
        self.day_to_water = 0
        self.time_to_water = ""
        self.visible = False

    def draw(self, surface):
        if self.visible:
            self.x = math.floor((self.screenW - (self.box_size * self.width)) / 2)
            self.y = math.floor((self.screenH - (self.box_size * self.height)) / 2)
            for j in range(self.map_array.shape[0]):
                for i in range(self.map_array.shape[1]):
                    xPos = self.x + (i * self.box_size)
                    yPos = self.y + (j * self.box_size)
                    pygame.draw.rect(
                        surface,
                        self.borderC,
                        ((xPos) - 1, (yPos) - 1, self.box_size + 2, self.box_size + 2),
                    )
                    if self.map_array[j][i] == 0:
                        pygame.draw.rect(
                            surface,
                            self.bgC,
                            (xPos, yPos, self.box_size, self.box_size),
                        )
                    if self.map_array[j][i] == 1:
                        pygame.draw.rect(
                            surface,
                            self.plantC,
                            (xPos, yPos, self.box_size, self.box_size),
                        )
                    if self.map_array[j][i] == 2:
                        pygame.draw.rect(
                            surface,
                            self.obstacleC,
                            (xPos, yPos, self.box_size, self.box_size),
                        )
                    if self.map_array[j][i] == 3:
                        pygame.draw.rect(
                            surface,
                            self.bgC,
                            (xPos, yPos, self.box_size, self.box_size),
                        )
                        pygame.draw.circle(
                            surface,
                            self.pathC,
                            (
                                (
                                    xPos + (self.box_size // 2),
                                    yPos + (self.box_size // 2),
                                )
                            ),
                            self.box_size // 4,
                        )

                        fontB = pygame.font.SysFont("comfortaa", (self.box_size // 6))
                        textB = fontB.render(str(self.path_array.index((j,i))), 1, (255, 255, 255))
                        surface.blit(
                            textB,
                                (
                                    math.floor((xPos + (self.box_size // 2)) + (self.width / 2 - textB.get_width() / 2)),
                                    math.floor((yPos + (self.box_size // 2)) + (self.height / 2 - textB.get_height() / 2)),
                                ),
                        )

    def updateMap(self, pos, block):
        if 3 not in self.map_array:
            self.path_array.clear()
        
        xPos = (pos[0] - self.x) // self.box_size
        yPos = (pos[1] - self.y) // self.box_size
        if xPos >= 0 and xPos < self.width:
            if yPos >= 0 and yPos < self.height:
                self.map_array[yPos][xPos] = block
                if block == 3:
                    self.path_array.append((yPos, xPos))
                elif (yPos, xPos) in self.path_array:
                    self.path_array.remove((yPos, xPos))