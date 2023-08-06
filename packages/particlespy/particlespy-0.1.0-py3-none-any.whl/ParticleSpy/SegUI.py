# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 15:50:08 2018

@author: qzo13262
"""

from PyQt5.QtWidgets import QCheckBox, QPushButton, QLabel, QMainWindow, QSpinBox
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QComboBox
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import sys

import inspect
import numpy as np
from skimage.segmentation import mark_boundaries
from skimage.util import invert

from ParticleSpy.segptcls import process
from ParticleSpy.ParticleAnalysis import parameters

class Application(QMainWindow):

    def __init__(self,im_hs):
        super().__init__()
        self.setWindowTitle("Segmentation UI")
        self.imflag = "Image"
        
        self.getim(im_hs)
        self.getparams()
        
        self.prev_params = parameters()
        self.prev_params.generate()
        
        offset = 50

        #self.central_widget = QWidget()               
        #self.setCentralWidget(self.central_widget)
        lay = QVBoxLayout()

        self.label = QLabel(self)
        qi = QImage(self.image.data, self.image.shape[1], self.image.shape[0], self.image.shape[1], QImage.Format_Grayscale8)
        pixmap = QPixmap(qi)
        pixmap2 = pixmap.scaled(512, 512, Qt.KeepAspectRatio)
        self.label.setPixmap(pixmap2)
        self.label.setGeometry(10,10,pixmap2.width(),pixmap2.height())
        
        height = max((pixmap2.height()+50,300 + offset)) #300 +50
        
        self.resize(pixmap2.width()+130, height)
        
        self.filt_title = QLabel(self)
        self.filt_title.setText('Pre-filtering options')
        self.filt_title.move(pixmap2.width()+20, 0)
        
        self.sptxt = QLabel(self)
        self.sptxt.setText('Rolling ball size')
        self.sptxt.move(pixmap2.width()+20,20)
        
        self.sp = QSpinBox(self)
        self.sp.setMaximum(self.image.shape[0])
        self.sp.valueChanged.connect(self.rollingball)
        self.sp.move(pixmap2.width()+20, 45)
        
        self.gausstxt = QLabel(self)
        self.gausstxt.setText('Gaussian filter kernel size')
        self.gausstxt.move(pixmap2.width()+20,70)
        
        self.gauss = QSpinBox(self)
        self.gauss.setMaximum(self.image.shape[0])
        self.gauss.valueChanged.connect(self.gaussian)
        self.gauss.move(pixmap2.width()+20, 95)
        
        self.thresh_title = QLabel(self)
        self.thresh_title.setText('Thresholding options')
        self.thresh_title.move(pixmap2.width()+20, 135)
        
        self.comboBox = QComboBox(self)
        self.comboBox.addItem("Otsu")
        self.comboBox.addItem("Mean")
        self.comboBox.addItem("Minimum")
        self.comboBox.addItem("Yen")
        self.comboBox.addItem("Isodata")
        self.comboBox.addItem("Li")
        self.comboBox.addItem("Local")
        self.comboBox.addItem("Local Otsu")
        self.comboBox.addItem("Local+Global Otsu")
        self.comboBox.move(pixmap2.width()+20, 160)
        self.comboBox.activated[str].connect(self.threshold_choice)
        
        self.localtxt = QLabel(self)
        self.localtxt.setText('Local filter kernel')
        self.localtxt.move(pixmap2.width()+20,195)
        
        self.local_size = QSpinBox(self)
        self.local_size.setMaximum(self.image.shape[0])
        self.local_size.valueChanged.connect(self.local)
        self.local_size.move(pixmap2.width()+20, 220)
        
        cb = QCheckBox('Watershed', self)
        cb.move(pixmap2.width()+20, 260)
        cb.stateChanged.connect(self.changeWatershed)
        
        cb2 = QCheckBox('Invert', self)
        cb2.move(pixmap2.width()+20, 260 + offset /2 )
        cb2.stateChanged.connect(self.changeInvert)
        
        self.minsizetxt = QLabel(self)
        self.minsizetxt.setText('Min particle size (px)')
        self.minsizetxt.move(pixmap2.width()+20, 280+offset)
        
        self.minsizev = QSpinBox(self)
        self.minsizev.setMaximum(self.image.shape[0]*self.image.shape[1])
        self.minsizev.valueChanged.connect(self.minsize)
        self.minsizev.move(pixmap2.width()+20, 305+offset)
        
        updateb = QPushButton('Update',self)
        updateb.move(pixmap2.width()+20,355+offset)
        updateb.clicked.connect(self.update)
        
        paramsb = QPushButton('Get Params',self)
        paramsb.move(pixmap2.width()+20,385+offset)
        
        paramsb.clicked.connect(self.return_params)
        
        self.imagetxt = QLabel(self)
        self.imagetxt.setText('Display:')
        self.imagetxt.move(75, pixmap2.height()+15)
        
        self.imBox = QComboBox(self)
        self.imBox.addItem("Image")
        self.imBox.addItem("Labels")
        self.imBox.move(pixmap2.width()/2-10, pixmap2.height()+15)
        
        self.imBox.activated[str].connect(self.changeIm)
        
        lay.addWidget(self.thresh_title)
        lay.addWidget(self.filt_title)
        lay.addWidget(self.label)
        lay.addWidget(self.comboBox)
        lay.addWidget(self.sp)
        lay.addWidget(self.sptxt)
        lay.addWidget(self.gauss)
        lay.addWidget(self.gausstxt)
        lay.addWidget(self.imagetxt)
        lay.addWidget(self.minsizev)
        self.show()
        
    def getim(self,im_hs):
        self.im_hs = im_hs
        im = im_hs.data.astype(np.float64)
        im = im-np.min(im)
        image = np.uint8(255*im/np.max(im))
        self.image = image
        
    def getparams(self):
        self.params = parameters()
        self.params.generate()
        
    def changeIm(self):
        if str(self.imBox.currentText()) == "Image":
            self.imflag = "Image"
        if str(self.imBox.currentText()) == "Labels":
            self.imflag = "Labels"
        
    def changeWatershed(self, state):
        if state == Qt.Checked:
            self.params.segment['watershed'] = True
        else:
            self.params.segment['watershed'] = False
            
    def changeInvert(self, state):
        if state == Qt.Checked:
            self.params.segment['invert'] = True
            qi = QImage(invert(self.image).data, self.image.shape[1], self.image.shape[0], self.image.shape[1], QImage.Format_Indexed8)
            
        else:
            self.params.segment['invert'] = False
            qi = QImage(self.image.data, self.image.shape[1], self.image.shape[0], self.image.shape[1], QImage.Format_Indexed8)
        
        pixmap = QPixmap(qi)
        pixmap2 = pixmap.scaled(512, 512, Qt.KeepAspectRatio)
        self.label.setPixmap(pixmap2)
            
    def rollingball(self):
        if self.sp.value() == 1:
            self.params.segment['rb_kernel'] = 0
        else:
            self.params.segment['rb_kernel'] = self.sp.value()
            
    def gaussian(self):
        self.params.segment['gaussian'] = self.gauss.value()
        
    def local(self):
        self.params.segment['local_size'] = self.local_size.value()
            
    def minsize(self):
        self.params.segment['min_size'] = self.minsizev.value()
            
    def update(self):
        labels = process(self.im_hs,self.params)
        labels = np.uint8(labels*(256/labels.max()))
        if self.imflag=="Image":
            #b=image
            b = np.uint8(mark_boundaries(self.image, labels, color=(1,1,1))[:,:,0]*255)
            qi = QImage(b.data, b.shape[1], b.shape[0], b.shape[1], QImage.Format_Indexed8)
        if self.imflag=="Labels":
            qi = QImage(labels.data, labels.shape[1], labels.shape[0], labels.shape[1], QImage.Format_Indexed8)
        #qi = QImage(imchoice.data, imchoice.shape[1], imchoice.shape[0], imchoice.shape[1], QImage.Format_Indexed8)
        pixmap = QPixmap(qi)
        pixmap2 = pixmap.scaled(512, 512, Qt.KeepAspectRatio)
        self.label.setPixmap(pixmap2)
        
        self.prev_params.load()
        self.prev_params.save(filename=inspect.getfile(process).rpartition('\\')[0]+'/Parameters/parameters_previous.hdf5')
        
        self.params.save()
        
    def undo(self):
        self.params.load(filename='Parameters/parameters_previous.hdf5')
        
        labels = process(self.im_hs,self.params)
        labels = np.uint8(labels*(256/labels.max()))
        if self.imflag=="Image":
            #b=image
            b = np.uint8(mark_boundaries(self.image, labels, color=(1,1,1))[:,:,0]*255)
            qi = QImage(b.data, b.shape[1], b.shape[0], b.shape[1], QImage.Format_Indexed8)
        if self.imflag=="Labels":
            qi = QImage(labels.data, labels.shape[1], labels.shape[0], labels.shape[1], QImage.Format_Indexed8)
        #qi = QImage(imchoice.data, imchoice.shape[1], imchoice.shape[0], imchoice.shape[1], QImage.Format_Indexed8)
        pixmap = QPixmap(qi)
        pixmap2 = pixmap.scaled(512, 512, Qt.KeepAspectRatio)
        self.label.setPixmap(pixmap2)
        
    def return_params(self,params):
        print(self.params.segment)
        
    def threshold_choice(self):
        if str(self.comboBox.currentText()) == "Otsu":
            self.params.segment['threshold'] = "otsu"
        if str(self.comboBox.currentText()) == "Mean":
            self.params.segment['threshold'] = "mean"
        if str(self.comboBox.currentText()) == "Minimum":
            self.params.segment['threshold'] = "minimum"
        if str(self.comboBox.currentText()) == "Yen":
            self.params.segment['threshold'] = "yen"
        if str(self.comboBox.currentText()) == "Isodata":
            self.params.segment['threshold'] = "isodata"
        if str(self.comboBox.currentText()) == "Li":
            self.params.segment['threshold'] = "li"
        if str(self.comboBox.currentText()) == "Local":
            self.params.segment['threshold'] = "local"
        if str(self.comboBox.currentText()) == "Local Otsu":
            self.params.segment['threshold'] = "local_otsu"
        if str(self.comboBox.currentText()) == "Local+Global Otsu":
            self.params.segment['threshold'] = "lg_otsu"
    
def main(haadf):
    
    ex = Application(haadf)
    
    return(ex)
    
def SegUI(image):
    app = QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)
    
    #params = ParticleAnalysis.param_generator()
    ex = main(image)
    
    #ex.show()
    app.exec_()
    
    return(ex)
    
if __name__ == '__main__':
    import hyperspy.api as hs
    filename = "Data/JEOL HAADF Image.dm4"
    haadf = hs.load(filename)
    app = QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)
    
    #params = ParticleAnalysis.param_generator()
    ex = main(haadf)
    
    #ex.show()
    app.exec_()
    