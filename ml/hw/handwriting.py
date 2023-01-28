# Simple canvas for entering numbers that will
# be passed to Tensorflow for inference.
# Accurracy is low and seems to have trouble with
# numbers like 9.  The line drawing code is very
# simple and would probably need to be improved.
#
# Commands to setup:
# python -m venv ./winenv
# pip3 install pygame
# pip3 install tensorflow
# pip3 install keras
# pip3 install matplotlib (used for debugging of images)
#
# Once environment is set  you can run with: python handwriting.py
#
# Notes:
# Tensorflow model is trained everytime on startup
# Lower case u will undo the last drawn line
# Tested on Windows
# Used a CPU version of Tensorflow
#

import pygame

try:
    import tensorflow as tf
    from keras import models
    from keras import layers
    from keras.utils import to_categorical
    from keras.datasets import mnist
    import numpy as np
    import matplotlib.pyplot as plt
    use_tf = True
except:
    print("# Tensorflow and keras.datasets not available")
    use_tf = False

#
# Class for keras support of mnist
#

class MnistInference:

    def __init__(self):
        print("# Initializing tensorflow")

        (self.train_images, self.train_labels), (self.test_images, self.test_labels) = mnist.load_data()

        self.network = models.Sequential()
        self.network.add(layers.Dense(512, activation='relu', input_shape=(28*28,)))
        self.network.add(layers.Dense(10, activation='softmax'))

        self.network.compile(optimizer='rmsprop',
                            loss='categorical_crossentropy',
                            metrics=['accuracy'])

        self.train_images = self.train_images.reshape(60000, 28*28)
        self.train_images = self.train_images.astype('float32') / 255
        
        self.test_images = self.test_images.reshape(10000, 28*28)
        self.test_images = self.test_images.astype('float32') / 255

        self.train_labels = to_categorical(self.train_labels)
        self.test_labels = to_categorical(self.test_labels)

        self.network.fit(self.train_images, self.train_labels, epochs=5, batch_size=128)

        test_loss, test_accuracy = self.network.evaluate(self.test_images, self.test_labels)
        print("# test_loss %g test_accuracy %g" % (test_loss, test_accuracy))

        # self.debugDisplaySomeImages()
       
    def predictOneImage(self, nparray):
        predictions = None
        if self.network:
            predictions = self.network.predict(nparray)
        return predictions

    def getImageAndLabel(self, test, idx):
        label = self.test_labels[idx] if test else self.train_labels[idx]
        image = self.test_images[idx] if test else self.train_images[idx]
        return label, image

    def displayImage(self, test, idx):
        label, image = self.getImageAndLabel(test, idx)
        #
        im = self.train_images[idx]
        im = im.reshape(28, 28)
        plt.imshow(im, cmap=plt.cm.binary)
        plt.show()
       
    def displayArrayImage(self, nparray, h=28, w=28):
        im = nparray
        im = im.reshape(h, w)
        plt.imshow(im, cmap=plt.cm.binary)
        plt.show()       

    def debugDisplaySomeImages(self):
        for idx in range(0,10):
            print("# test label %s", self.train_labels[idx]);
            print(self.train_images[idx])
            self.displayImage(True, idx)

#
# Grid screen class to handle input and display
# using pygame
#

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

    # Line width is an important variable to
    # set correctly.  As the image will be
    # scaled down below a width that won't
    # make the character disappear is needed
    LINE_WIDTH = 20

    TITLE = "Hand writing input:  "

    def __init__(self):
        pygame.init()

        self.screen = None
        self.input = [ " - " for i in range(0,self.DIVISIONS*self.DIVISIONS) ]
        self.points = []
        self.lines = []
        self.lineUpdate = False
        self.drawing = False
        self.afterMouseUp = False
        self.backgroundColour = self.BLACK
        self.gridColour = self.GRAY
        self.lineColour = self.GRAY

        self.mnist = MnistInference()
        
    def updateCaption(self):
        caption = self.TITLE + str(self.input)
        pygame.display.set_caption(caption)
        
    def run(self):
        caption = self.TITLE + str(self.input)
        self.createWindow(caption, self.H, self.W, self.backgroundColour)

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
                            self.setBackground(self.backgroundColour)
                            self.lineUpdate = True
                            # Allow undo operation to run character prediction
                            self.afterMouseUp = True
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

    def extractImages(self):
        debug = False
        pygame.display.update()
        surface = pygame.display.get_surface().copy()
        firstsmallsurface = None
        lastcrect = None
        # Reset the input string
        self.input = []
        # Left, top, width, height
        rh = self.H/self.DIVISIONS
        wh = self.W/self.DIVISIONS
        for i in range(0, self.DIVISIONS):
            for j in range(0, self.DIVISIONS):
                # Create the rectangle, position and inset it to avoid the grids
                crect = pygame.Rect(0, 0, rh, wh)
                crect.move_ip(j*rh, i*wh)
                crect.inflate_ip(-8, -8)
                # Get the subsurface copy
                subsurface = pygame.display.get_surface().subsurface(crect).copy()
                # Reduce the surface to the prediction image size we need
                # Smooth scale is used as it averages pixels as it collapses the image
                small_surface =  pygame.transform.smoothscale(subsurface, self.IMG_SIZE)
                nprgb  = pygame.surfarray.array_red(small_surface)
                nprgb += pygame.surfarray.array_green(small_surface)
                nprgb += pygame.surfarray.array_blue(small_surface)
                nprgb = nprgb / 3.0
                # Remove the transpose that pygame uses for draw data
                nprgb = np.fliplr(nprgb)
                nprgb = np.rot90(nprgb)
                nprgb = nprgb.astype('float32') / 255.0
                #
                if debug:
                    # self.displaySurface(subsurface)
                    self.mnist.displayArrayImage(nprgb)
                    print(nprgb)
                    # Track debug vars
                    if not firstsmallsurface:
                        firstsmallsurface = small_surface
                    lastcrect = crect
                    print("H %d W %d BYTES: %d" % (small_surface.get_height(), small_surface.get_width(), small_surface.get_bytesize()))
                # Run the prediction on the nprgb image colour array
                num = self.predicateImageNumber(nprgb)
                if num < 0:
                    self.input.append(" - ")
                else:
                    self.input.append(" " + str(num) + " ")
                    
        self.updateCaption()
        
        if debug:
            # Blit of first grid image to the last position
            pygame.display.get_surface().blit(firstsmallsurface, lastcrect)

    def displaySurface(self, surface):
        nprgb  = pygame.surfarray.array_red(surface)
        nprgb += pygame.surfarray.array_green(surface)
        nprgb += pygame.surfarray.array_blue(surface)
        nprgb = nprgb / 3.0
        nprgb = np.fliplr(nprgb)
        nprgb = np.rot90(nprgb)
        self.mnist.displayArrayImage(nprgb, 272, 272)       

    def predicateImageNumber(self, nprgb):
        if self.mnist:
            debug = False
            # Reshape so image can be passed to predictor
            nprgb = nprgb.reshape(1, nprgb.shape[0]*nprgb.shape[1])
            predictions = self.mnist.predictOneImage(nprgb)
            if debug: print("# prediction: ", predictions, predictions.shape)
            max_idx = -1
            maximum = 0
            for p in range(0, len(predictions[0])):
                if predictions[0,p] > maximum:
                    max_idx = p
                    maximum = predictions[0,p]
            if maximum > 0.4:
                if debug: print("#### ",max_idx)
                return max_idx

        return -1 
            
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
                pygame.draw.rect(self.screen, self.gridColour, crect, 3)
        if update:
            self.updateCaption()
            pygame.display.update()

    def drawLines(self, lines):
        for line in self.lines:
            # print(line)
            pygame.draw.lines(self.screen, self.lineColour, False, line, self.LINE_WIDTH)
       
    def done(self):
        pygame.quit()


def main():
    dg = DrawGrid()
    dg.run()
  
  
if __name__=="__main__":
    main()

