# Simple canvas for entering numbers that will
# be passed to Tensorflow for inference.
#
# Work in progress:
# - Tensorflow/Keras hookup still to be done
#
# Commands to setup:
# python -m venv ./pygenv
# pip3 install pygame
# pip3 install tensorflow
# pip3 install keras
#

import pygame

try:
    import tensorflow as tf
    from keras import models
    from keras import layers
    from keras.utils import to_categorical
    from keras.datasets import mnist
    use_tf = True
except:
    print("# Tensorflow and keras.datasets not available")
    use_tf = False


class DrawGrid:

    DIVISIONS = 3 # grid divisions
    K = 28
    H = K*10*DIVISIONS
    W = K*10*DIVISIONS
    IMG_SIZE = (K, K)

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
        self.afterMouseUp = False
        self.network = None
        
        if use_tf:
            self.init_tf()

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
            #
            if self.lineUpdate:
                self.drawLines(self.lines)
                self.lineUpdate = False
            # Extract images
            if self.afterMouseUp and not self.drawing:
                self.extractImages()
                self.afterMouseUp = False
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
                    self.afterMouseUp = True
                    self.points.append(event.pos)
                    if self.drawing:
                        self.lines.append(self.points)
                        self.points = []
                        self.drawing = False
                        self.lineUpdate = True
                        
        self.done()

    def init_tf(self):
        print("# Initializing tensorflow")

        (train_images, train_labels), (test_images, test_labels) = mnist.load_data()

        self.network = models.Sequential()
        self.network.add(layers.Dense(512, activation='relu', input_shape=(28*28,)))
        self.network.add(layers.Dense(10, activation='softmax'))

        self.network.compile(optimizer='rmsprop',
                            loss='categorical_crossentropy',
                            metrics=['accuracy'])

        train_images = train_images.reshape(60000, 28*28)
        train_images = train_images.astype('float32') / 255
        
        test_images = test_images.reshape(10000, 28*28)
        test_images = test_images.astype('float32') / 255

        train_labels = to_categorical(train_labels)
        test_labels = to_categorical(test_labels)

        self.network.fit(train_images, train_labels, epochs=1, batch_size=128)

        test_loss, test_accuracy = self.network.evaluate(test_images, test_labels)
        print("# test_loss %g test_accuracy %g" % (test_loss, test_accuracy))
       
        
    def extractImages(self):
        debug = True
        pygame.display.update()
        surface = pygame.display.get_surface().copy()
        subsurfaces = []
        crects = []
        views = []
        # Left, top, width, height
        rh = self.H/self.DIVISIONS
        wh = self.W/self.DIVISIONS
        for i in range(0, 1): # range(0, self.DIVISIONS):
            for j in range(0, self.DIVISIONS):
                crect = pygame.Rect(0, 0, rh, wh)
                crect.move_ip(i*rh, j*wh)
                crect.inflate_ip(-8, -8)
                subsurface = surface.subsurface(crect)
                small_surface =  pygame.transform.scale(subsurface, self.IMG_SIZE)
                view = small_surface.get_view('3')
                print(view.raw)
                nparray = pygame.surfarray.array2d(subsurface)
                #print("# small surface shape %s" % (str(nparray.shape)))
                nparray = nparray.reshape(1, nparray.shape[0]*nparray.shape[1])
                #print("# small surface shape %s" % (str(nparray.shape)))
                print(nparray)
                subsurfaces.append(subsurface)
                crects.append(crect)
                #views.append(view)
                #
                if debug:
                    print("H %d W %d BYTES: %d" % (small_surface.get_height(), small_surface.get_width(), small_surface.get_bytesize()))
                    #print("\tview %d\n" % (view.length))
                #
                #if self.network:
                #    prediction = self.network.predict(1, nparray)
                #    print("# prediction: ", prediction)

        if debug:
            #pygame.display.get_surface().blit(subsurfaces[0], crects[-1])
            pass
    
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

