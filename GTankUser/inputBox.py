import pygame

class InputBox:
    def __init__(self, x, y, w, h, text=""):
        self.rect = pygame.Rect(x, y, w, h)
        self.width = w
        self.color = (211, 211, 211)
        self.defaultText = text
        self.text = ""
        self.font = pygame.font.SysFont("comfortaa", 45)
        self.txt_surface = self.font.render(self.defaultText, True, self.color)
        self.active = False
        self.visible = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.visible:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = (211, 211, 211) if self.active else (0, 0, 0)
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ""
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.font.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(self.width, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        if self.visible:
            # Blit the text.
            screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
            self.update()
            # Blit the rect.
            pygame.draw.rect(screen, self.color, self.rect, 2)