import pygame
import map
import button
import inputBox
import datetime as dt
import math

pygame.init()

infoObject = pygame.display.Info()

screenW = math.floor(infoObject.current_w * 0.8)
screenH = math.floor(infoObject.current_h * 0.8)

win = pygame.display.set_mode((screenW, screenH))
win.fill((250, 250, 250))
pygame.display.set_caption("Garden Tank App")
clock = pygame.time.Clock()

run = True

def redrawWindow():
    win.fill((250, 250, 250))
    mapEditBtn.draw(win, (0, 0, 0))
    inputDimensionsBtn.draw(win, (0, 0, 0))
    backBtn.draw(win, (0, 0, 0))
    mapDoneBtn.draw(win, (0, 0, 0))
    user_map.draw(win)
    input_width.draw(win)
    input_height.draw(win)
    plantBtn.draw(win, (0, 0, 0))
    obstacleBtn.draw(win, (0, 0, 0))
    eraserBtn.draw(win, (0, 0, 0))
    pathBtn.draw(win, (0, 0, 0))
    pygame.display.update()


user_map = map.Map(0,0, 0, 0, 0)
mapEditBtn = button.Button(
    (200, 200, 200),
    math.floor((screenW / 2) - 100),
    math.floor((screenH / 2) - 25),
    200,
    50,
    "EDIT MAP",
)
mapEditBtn.visible = True
inputDimensionsBtn = button.Button(
    (200, 200, 200),
    math.floor((screenW / 2) - 100),
    math.floor((screenH / 2) + 70),
    200,
    50,
    "ENTER",
)
backBtn = button.Button(
    (200, 200, 200),
    math.floor((screenW * 0.01)),
    math.floor((screenH * 0.01)),
    200,
    50,
    "BACK",
)
mapDoneBtn = button.Button(
    (200, 200, 200),
    math.floor((screenW / 2)) - 200,
    math.floor((screenH * 0.905)),
    400,
    50,
    "DONE WITH MAP",
)
plantBtn = button.Button(
    user_map.plantC,
    math.floor((screenW / 2) - 400),
    math.floor((screenH * 0.01)),
    200,
    50,
    "PLANT",
)
obstacleBtn = button.Button(
    user_map.obstacleC,
    math.floor((screenW / 2)) - 190,
    math.floor((screenH * 0.01)),
    200,
    50,
    "NO ZONE",
)
eraserBtn = button.Button(
    user_map.bgC,
    math.floor((screenW / 2)) + 210,
    math.floor((screenH * 0.01)),
    200,
    50,
    "ERASER",
)
pathBtn = button.Button(
    user_map.pathC,
    math.floor((screenW / 2)) + 420,
    math.floor((screenH * 0.01)),
    200,
    50,
    "PATH",
)
input_width = inputBox.InputBox(
    math.floor((screenW / 2) - 200),
    math.floor((screenH / 2) - 60),
    400,
    50,
    "ENTER WIDTH IN FEET",
)
input_height = inputBox.InputBox(
    math.floor((screenW / 2) - 200),
    math.floor((screenH / 2) + 10),
    400,
    50,
    "ENTER HEIGHT IN FEET",
)
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
            if inputDimensionsBtn.isOver(mousePos) and user_map.width == 0:
                mapHeight = int(input_height.text)
                mapWidth = int(input_width.text)
                mapBoxSize = 0
                if (screenH * 0.9) / mapHeight > (screenW * 0.9) / mapWidth:
                    mapBoxSize = math.floor((screenW * 0.9) / mapWidth)
                else:
                    mapBoxSize = math.floor((screenH * 0.9) / mapHeight)
                user_map = map.Map(screenW, screenH, mapHeight, mapWidth, mapBoxSize)
                input_width.visible = False
                input_height.visible = False
                inputDimensionsBtn.visible = False
            if user_map.width > 0:
                if backBtn.isOver(mousePos):
                    mapEditBtn.visible = True
                    map_editing = False
                    backBtn.visible = False
                    user_map.visible = False
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
                    user_map.updateMap(mousePos, currentBlock)
                if mapDoneBtn.isOver(mousePos):
                    print(user_map.path_array)

        if map_editing:
            if user_map.width == 0:
                input_width.visible = True
                input_height.visible = True
                inputDimensionsBtn.visible = True
                input_width.handle_event(event)
                input_height.handle_event(event)
            else:
                user_map.visible = True
                backBtn.visible = True
                mapDoneBtn.visible = True
                plantBtn.visible = True
                obstacleBtn.visible = True
                eraserBtn.visible = True
                pathBtn.visible = True

    redrawWindow()