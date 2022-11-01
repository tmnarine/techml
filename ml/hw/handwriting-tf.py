# Simple canvas for entering numbers that will
# be passed to Tensorflow for inference.
#
# Work in progress:
# - Tensorflow/Keras hookup still to be done
#
# Commands to setup:
# python -m venv ./pygenv
# pip3 install pygame
#

import pygame

class DrawGrid:

    H = 800
    W = 600
    DIVISIONS = 3 # grid divisions

    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GRAY = (127, 127, 127)
    WHITE = (255, 255, 255)

    TITLE = "Hand writing input:  "

    def __init__(self):
        pygame.init()

        self.screen = None
        self.input = [ "-", "-", "-", "-", "-", "-" ]
        self.points = []
        self.lines = []
        self.lineUpdate = False
        self.drawing = False

    def updateCaption(self):
        caption = self.TITLE + str(self.input)
        pygame.display.set_caption(caption)
        
    def run(self):
        caption = self.TITLE + str(self.input)
        self.createWindow(caption, self.H, self.W, self.GRAY)

        running = True
        # Event loop
        while running:
            # Draw
            self.drawGrid( self.DIVISIONS, True )
            if self.lineUpdate:
                self.drawLines(self.lines)
                self.lineUpdate = False
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_u:
                        # Undo: control + u
                        if len(self.lines) > 0:
                            self.lines.pop()
                            self.setBackground(self.GRAY)
                            self.lineUpdate = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.points.append(event.pos)
                    self.drawing = True
                elif event.type == pygame.MOUSEMOTION and self.drawing:
                    self.points.append(event.pos)
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.points.append(event.pos)
                    if self.drawing:
                        self.lines.append(self.points)
                        self.points = []
                        self.drawing = False
                        self.lineUpdate = True
                        
        self.done()

    def createWindow(self, name, h, w, color):
        self.screen = pygame.display.set_mode((h, w))
        self.setBackground(color)
        pygame.display.set_caption(name)

    def setBackground(self, color):
        self.screen.fill(color)
        pygame.display.update()

    def drawGrid(self, d, update=False):
        # Left, top, width, height
        rh = self.H/self.DIVISIONS
        wh = self.W/self.DIVISIONS
        for i in range(0, self.DIVISIONS):
            for j in range(0, self.DIVISIONS):
                crect = pygame.Rect(0, 0, rh, wh)
                crect.move_ip(i*rh, j*wh)
                pygame.draw.rect(self.screen, self.BLACK, crect, 3)
        if update:
            self.updateCaption()
            pygame.display.update()

    def drawLines(self, lines):
        for line in self.lines:
            # print(line)
            pygame.draw.lines(self.screen, self.RED, False, line, 3)
       
    def done(self):
        pygame.quit()


def main():
    dg = DrawGrid()
    dg.run()
  
  
if __name__=="__main__":
    main()

