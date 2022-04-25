import pygame
import math

class Button:
    def __init__(self, color, x, y, width, height, text=""):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.visible = False

    def draw(self, surface, outline=None):
        if self.visible:
            # Call this method to draw the button on the screen
            if outline:
                pygame.draw.rect(
                    surface,
                    outline,
                    (self.x - 2, self.y - 2, self.width + 4, self.height + 4),
                    0,
                )

            pygame.draw.rect(
                surface, self.color, (self.x, self.y, self.width, self.height), 0
            )

            if self.text != "":
                fontB = pygame.font.SysFont("comfortaa", 45)
                textB = fontB.render(self.text, 1, (255, 255, 255))
                surface.blit(
                    textB,
                    (
                        math.floor(self.x + (self.width / 2 - textB.get_width() / 2)),
                        math.floor(self.y + (self.height / 2 - textB.get_height() / 2)),
                    ),
                )
                # print(self.width , self.height)

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False