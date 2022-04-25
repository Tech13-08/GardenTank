from turtle import Turtle
import pygame
import numpy as np
import datetime as dt
import math

pygame.init()

infoObject = pygame.display.Info()

screenW = math.floor(infoObject.current_w * 0.8)
screenH = math.floor(infoObject.current_h * 0.8)

win = pygame.display.set_mode((screenW, screenH))
win.fill((250,250,250))
pygame.display.set_caption("Garden Tank App")
clock = pygame.time.Clock()

run = True

class Map:
    def __init__(self, height, width,boxSize):
        self.width = width
        self.height = height
        self.map_array = np.zeros((height, width),dtype=int)
        self.water_direction = "left"
        self.box_size = boxSize
        self.path_array = []
        self.x = math.floor((screenW - (self.box_size * self.width))/2)
        self.y = math.floor((screenH - (self.box_size * self.height))/2)
        self.bgC = (211,211,211)
        self.borderC = (0,0,0)
        self.plantC = (0,153,0)
        self.obstacleC = (102,51,0)
        self.pathC = (255,0,0)
        self.day_to_water = 0
        self.time_to_water = ""
        self.visible = False

    def draw(self, surface):
        if self.visible:
            self.x = math.floor((screenW - (self.box_size * self.width))/2)
            self.y = math.floor((screenH - (self.box_size * self.height))/2)
            for j in range (self.map_array.shape[0]):
                for i in range (self.map_array.shape[1]):
                    xPos = self.x + (i*self.box_size)
                    yPos = self.y + (j*self.box_size)
                    pygame.draw.rect(surface, self.borderC, ((xPos)-1, (yPos)-1,self.box_size+2,self.box_size+2))
                    if self.map_array[j][i] == 0:
                        pygame.draw.rect(surface, self.bgC, (xPos, yPos,self.box_size,self.box_size))
                    if self.map_array[j][i] == 1:
                        pygame.draw.rect(surface, self.plantC, (xPos, yPos,self.box_size,self.box_size))
                    if self.map_array[j][i] == 2:
                        pygame.draw.rect(surface, self.obstacleC, (xPos, yPos,self.box_size,self.box_size)) 
                    if self.map_array[j][i] == 3:   
                        pygame.draw.rect(surface, self.bgC, (xPos, yPos,self.box_size,self.box_size))
                        pygame.draw.circle(surface, self.pathC, ((xPos+(self.box_size//2), yPos+(self.box_size//2))),self.box_size//4)

    def updateMap(self, pos, block):
        xPos = ((pos[0]-self.x)//self.box_size)
        yPos = ((pos[1]-self.y)//self.box_size)
        if xPos >= 0 and xPos < self.width:
            if yPos >= 0 and yPos < self.height:
                self.map_array[yPos][xPos] = block
                if block == 3:
                    self.path_array.append((yPos,xPos))
                elif (yPos,xPos) in self.path_array:
                    self.path_array.remove((yPos,xPos))
    


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

class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.width = w
        self.color = (211,211,211)
        self.defaultText = text
        self.text = ""
        self.font = pygame.font.SysFont("comfortaa", 45)
        self.txt_surface = self.font.render(self.defaultText, True, self.color)
        self.active = False
        self.visible = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = (211,211,211) if self.active else (0,0,0)
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.font.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(self.width, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        if self.visible:
            # Blit the text.
            screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
            self.update()
            # Blit the rect.
            pygame.draw.rect(screen, self.color, self.rect, 2)

def redrawWindow():
    win.fill((250,250,250))
    mapEditBtn.draw(win, (0,0,0))
    inputDimensionsBtn.draw(win, (0,0,0))
    backBtn.draw(win, (0,0,0))
    mapDoneBtn.draw(win, (0,0,0))
    test_map.draw(win)
    input_width.draw(win)
    input_height.draw(win)
    plantBtn.draw(win, (0,0,0))
    obstacleBtn.draw(win, (0,0,0))
    eraserBtn.draw(win, (0,0,0))
    pathBtn.draw(win, (0,0,0))
    pygame.display.update()

test_map = Map(0,0,0)
mapEditBtn = Button((200,200,200),math.floor((screenW/2)-100),math.floor((screenH/2)-25),200,50,"EDIT MAP")
mapEditBtn.visible = True
inputDimensionsBtn = Button((200,200,200), math.floor((screenW/2)-100), math.floor((screenH/2)+70), 200,50,"ENTER")
backBtn = Button((200,200,200), math.floor((screenW*0.01)), math.floor((screenH*0.01)), 200,50,"BACK")
mapDoneBtn = Button((200,200,200), math.floor((screenW/2))-200, math.floor((screenH*0.905)), 400,50,"DONE WITH MAP")
plantBtn = Button(test_map.plantC, math.floor((screenW/2)-400), math.floor((screenH*0.01)), 200,50,"PLANT")
obstacleBtn = Button(test_map.obstacleC, math.floor((screenW/2))-190, math.floor((screenH*0.01)), 200,50,"NO ZONE")
eraserBtn = Button(test_map.bgC, math.floor((screenW/2))+210, math.floor((screenH*0.01)), 200,50,"ERASER")
pathBtn = Button(test_map.pathC, math.floor((screenW/2))+420, math.floor((screenH*0.01)), 200,50,"PATH")
input_width = InputBox(math.floor((screenW/2)-200),math.floor((screenH/2)-60),400,50,"ENTER WIDTH IN FEET")
input_height = InputBox(math.floor((screenW/2)-200),math.floor((screenH/2)+10),400,50,"ENTER HEIGHT IN FEET")
map_editing = False
currentBlock = 0
print(screenW)
print(screenH)
while run:
    clock.tick(27)
    
    # Check Events ----------------------------------------------------------------------------------------------------------------
    for event in pygame.event.get():
        mousePos = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if mapEditBtn.isOver(mousePos):
                mapEditBtn.visible = False
                map_editing = True
            if inputDimensionsBtn.isOver(mousePos) and test_map.width == 0:
                mapHeight = int(input_height.text)
                mapWidth = int(input_width.text)
                mapBoxSize = 0
                if (screenH*0.9)/mapHeight > (screenW*0.9)/mapWidth:
                    mapBoxSize = math.floor((screenW*0.9)/mapWidth)
                else:
                    mapBoxSize = math.floor((screenH*0.9)/mapHeight)
                test_map = Map(mapHeight, mapWidth, mapBoxSize)
                input_width.visible = False
                input_height.visible = False
                inputDimensionsBtn.visible = False
            if test_map.width > 0:
                if backBtn.isOver(mousePos):
                    mapEditBtn.visible = True
                    map_editing = False
                    backBtn.visible = False
                    test_map.visible = False
                    mapDoneBtn.visible = False
                    plantBtn.visible = False
                    obstacleBtn.visible = False
                    eraserBtn.visible = False
                    pathBtn.visible = False
                
                if plantBtn.isOver(mousePos):
                    currentBlock = 1
                if obstacleBtn.isOver(mousePos):
                    currentBlock = 2
                if pathBtn.isOver(mousePos):
                    currentBlock = 3
                if eraserBtn.isOver(mousePos):
                    currentBlock = 0
                if map_editing and not mapDoneBtn.isOver(mousePos):
                    test_map.updateMap(mousePos, currentBlock)
                if mapDoneBtn.isOver(mousePos):
                    print(test_map.path_array)

            
        if map_editing:
            if test_map.width == 0:
                input_width.visible = True
                input_height.visible = True
                inputDimensionsBtn.visible = True
                input_width.handle_event(event)
                input_height.handle_event(event)
            else:
                test_map.visible = True
                backBtn.visible = True
                mapDoneBtn.visible = True
                plantBtn.visible = True
                obstacleBtn.visible = True
                eraserBtn.visible = True
                pathBtn.visible = True

                

            
    redrawWindow()




