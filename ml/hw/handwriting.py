# Simple canvas for entering numbers that will
# be passed to Tensorflow for number inference
# using MNIST.
# Accurracy is low and code has some trouble
# with some numbers.  The line drawing code is very
# simple and would probably need to be improved to
# fix this.
# Recognized numbers are added to the title name at
# the right index.
#
# Commands to setup:
# python -m venv ./winenv
# pip3 install pygame
# pip3 install tensorflow
# pip3 install keras
# pip3 install matplotlib (used for debugging of images)
#
# Once the environment is set  you can run with: python handwriting.py
#
# Notes:
# Tensorflow model is trained the first time the code runs.
# The model will be saved and loaded on subsequent invocations of the script.
#
# Lower case ctrl+z will undo the last drawn line
# Tested on Windows using the CPU version of Tensorflow
#

import os
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
# Class for Keras support of MNIST
#

class MnistInference:

    MODEL_NAME = "./hwmodel"

    BUILD_MODEL = False

    def __init__(self):
        print("# Initializing tensorflow")

        if self.BUILD_MODEL or not os.path.exists(self.MODEL_NAME):
            self.buildModel(True)
        else:
            print("# Loading model: %s" %(self.MODEL_NAME))
            self.network = tf.keras.models.load_model(self.MODEL_NAME)
 
    def buildModel(self, saveModel):

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

        if saveModel:
            print("# Saving model: %s" %(self.MODEL_NAME))
            self.network.save(self.MODEL_NAME)
       
    def predictOneImage(self, nparray):
        predictions = None
        if self.network:
            predictions = self.network.predict(nparray)
        return predictions

    def getImageAndLabel(self, test, idx):
        assert(self.BUILD_MODEL)
        label = self.test_labels[idx] if test else self.train_labels[idx]
        image = self.test_images[idx] if test else self.train_images[idx]
        return label, image

    def displayImage(self, test, idx):
        assert(self.BUILD_MODEL)
        label, image = self.getImageAndLabel(test, idx)
        #
        im = self.train_images[idx]
        im = im.reshape(28, 28)
        plt.imshow(im, cmap=plt.cm.binary)
        plt.show()
       
    def displayArrayImage(self, nparray, h=28, w=28):
        assert(self.BUILD_MODEL)
        im = nparray
        im = im.reshape(h, w)
        plt.imshow(im, cmap=plt.cm.binary)
        plt.show()       

    def debugDisplaySomeImages(self):
        assert(self.BUILD_MODEL)
        for idx in range(0,10):
            print("# test label %s", self.train_labels[idx]);
            print(self.train_images[idx])
            self.displayImage(True, idx)

    def debugGetTrainedImageByNumber(self, number, display = False):
        assert(self.BUILD_MODEL)
        idx = 0
        for label_array in self.train_labels:
            if label_array[number] >= 1:
                if display:
                    print("# label_array: ", label_array)
                    self.displayImage(True, idx)
                return self.train_images[idx]
            idx += 1
        return None

#
# Grid screen class to handle input and display
# using pygame
#

class GridScreen:

    DIVISIONS = 3 # grid divisions
    K = 28
    H = K*10*DIVISIONS
    W = K*10*DIVISIONS
    IMG_SIZE = (K, K)

    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GRAY = (127, 127, 127)
    BLUE = (0, 0, 255)
    WHITE = (255, 255, 255)

    # Line width is an important variable to
    # set correctly.  As the image will be
    # scaled down below a width that won't
    # make the character disappear is needed
    LINE_WIDTH = 10

    TITLE = "Write numbers 0-9 filling grid:  "

    def __init__(self):
        pygame.init()

        self.screen = None
        self.input = [ " - " for i in range(0,self.DIVISIONS*self.DIVISIONS) ]
        self.points = []
        self.lines = []
        self.drawAllLines = False
        self.penDown = False
        self.penUp = False
        self.backgroundColour = self.BLACK
        self.gridColour = self.GRAY
        self.lineColour = self.BLUE
        self.debugCounter = 0

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
            if self.drawAllLines:
                self.drawLines(self.lines)
                self.drawAllLines = False
            if self.penDown:
                self.drawPoints(self.points)
            # Extract images
            if self.penUp:
                self.extractGridImagesAndPredict()
                self.penUp = False
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_z and pygame.key.get_mods() & pygame.KMOD_LCTRL:
                        # Undo: ctr + z key
                        if len(self.lines) > 0:
                            self.lines.pop()
                            self.setBackground(self.backgroundColour)
                            self.drawAllLines = True
                            # Allow undo operation to run character prediction
                            self.penUp = True
                            # Keep same debug state
                            self.debugCounter -= 1
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.points.append(event.pos)
                    self.penDown = True
                elif event.type == pygame.MOUSEMOTION and self.penDown:
                    self.points.append(event.pos)
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.penUp = True
                    self.points.append(event.pos)
                    if self.penDown:
                        self.lines.append(self.points)
                        self.points = []
                        self.penDown = False
                        self.drawAllLines = True
                        
        self.done()

    def extractGridImagesAndPredict(self):
        pygame.display.update()
        # Following 3 variables used for debug images
        showTrainingImages = False        
        gridsurfaces = []
        gridrects = []
        # Reset the input string
        self.input = []
        # Left, top, width, height
        rh = self.H/self.DIVISIONS
        wh = self.W/self.DIVISIONS
        for i in range(0, self.DIVISIONS):
            for j in range(0, self.DIVISIONS):
                # Create the rectangle, position and inset it to avoid the grids
                gridrect = pygame.Rect(0, 0, rh, wh)
                gridrect.move_ip(j*rh, i*wh)
                gridrect.inflate_ip(-8, -8)
                # Get the subsurface copy of the current grid rectangle
                subsurface = pygame.display.get_surface().subsurface(gridrect).copy()
                # Reduce the surface to the prediction image size we need
                # Smooth scale is used as it averages pixels as it collapses the image
                small_surface =  pygame.transform.smoothscale(subsurface, self.IMG_SIZE)
                nrgbimage  = pygame.surfarray.array_red(small_surface)
                nrgbimage += pygame.surfarray.array_green(small_surface)
                nrgbimage += pygame.surfarray.array_blue(small_surface)
                nrgbimage = nrgbimage / 3.0
                # Remove the transpose that pygame uses for draw data
                nrgbimage = np.fliplr(nrgbimage)
                nrgbimage = np.rot90(nrgbimage)
                nrgbimage = nrgbimage.astype('float32') / 255.0
                #
                if showTrainingImages:
                    gridsurfaces.append(small_surface)
                    gridrects.append(gridrect)                   
                    # print("H %d W %d BYTES: %d" % (small_surface.get_height(), small_surface.get_width(), small_surface.get_bytesize()))
                # Run the prediction on the nprgb image colour array
                num = self.predicateImageNumber(nrgbimage, i, j)
                if num < 0:
                    self.input.append(" - ")
                else:
                    self.input.append(" " + str(num) + " ")
                    
        self.updateCaption()

        # Turn the following code path on to see debug images in the -2, -1 grid positions
        if showTrainingImages:
            scaled_surface = self.scaleUp(gridsurfaces[0])
             # Blit of first grid image to the second to last position
            pygame.display.get_surface().blit(scaled_surface, gridrects[-2])
            
            # Draw mnist characters 0,1,...,9
            mnist_image = self.mnist.debugGetTrainedImageByNumber(self.debugCounter)
            mnist_image = mnist_image.reshape(28, 28)
            mnist_image = np.fliplr(mnist_image)
            mnist_image = np.rot90(mnist_image)
            # print("mnist_image: ",mnist_image.shape, mnist_image)
            mnist_surface = pygame.surfarray.make_surface(mnist_image)
            mnist_surface = self.scaleUp(mnist_surface)
            pygame.display.get_surface().blit(mnist_surface, gridrects[-1])
            #
            self.debugCounter += 1
            self.debugCounter = self.debugCounter % 10
        
    def scaleUp(self, surface):
        scaled_surface = surface
        for i in range(0,3):
            scaled_surface = pygame.transform.scale2x(scaled_surface)
        return scaled_surface
            
    def predicateImageNumber(self, nprgb, i, j):
        if self.mnist:
            debug = True
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
                if debug: print("### Prediction (%d, %d) %d " % (i, j, max_idx))
                return max_idx
            else:
                if debug: print("### No prediction (%d, %d)" % (i, j))

        return -1 

    def debugDisplaySurface(self, surface):
        nrgbimage  = pygame.surfarray.array_red(surface)
        nrgbimage += pygame.surfarray.array_green(surface)
        nrgbimage += pygame.surfarray.array_blue(surface)
        nrgbimage = nrgbimage / 3.0
        nrgbimage = np.fliplr(nrgbimage)
        nrgbimage = np.rot90(nrgbimage)
        self.mnist.displayArrayImage(nrgbimage, 272, 272)
        
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
            # Smooth out the line points with circles
            self.drawPoints(line)
       
    def drawPoints(self, points):
        for point in points:
            pygame.draw.circle(self.screen, self.lineColour, point, round(self.LINE_WIDTH))      

    def done(self):
        pygame.quit()


def main():
    dg = GridScreen()
    dg.run()
  
  
if __name__=="__main__":
    main()

