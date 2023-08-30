import sys
import os

from interfaz import *
from PyQt5.QtWidgets import QMainWindow, QApplication,QWidget,QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


import pydicom as dicom
import numpy as np
import cv2

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import PIL.ImageQt as PQ

ALPHA=0.1
BETA=0

# Ajuste de contraste usando OpenCV
def adjust_contrast(image, alpha, beta):
    adjusted_image = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    return adjusted_image

# Normalización de intensidad a [0, 255]
def normalize_intensity(image):
    normalized_image = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX)
    return normalized_image


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self)
        self.ui= Ui_MainWindow()
        self.ui.setupUi(self)
        self.show()   
        
        self.ui.pushButton.clicked.connect(self.openImageDialog)
        self.ui.pushButton_2.clicked.connect(self.saveimage)
        self.ui.b_normalizar.clicked.connect(self.normalizar)
        self.ui.slider_beta.valueChanged.connect(self.variarbeta)
        self.ui.slider_alpha.valueChanged.connect(self.variaralpha)
        self.setWindowTitle("DICOM Viewer")


    def variarbeta(self):
        
        beta=self.ui.slider_beta.value()
        self.ui.le_beta.setText(str(beta))
        BETA=beta
        scaled_x_float = cv2.convertScaleAbs(self.x_float, alpha=ALPHA, beta=BETA)
        reescaled=(np.maximum(scaled_x_float,0)/scaled_x_float.max())*255
        final_image=np.uint8(reescaled)
        self.final_image=Image.fromarray(final_image)
        self.final_image.save('new_image.jpg')
        self.pixmap = QPixmap('new_image.jpg')
        self.ui.label_2.setPixmap(self.pixmap.scaled(800, 800, Qt.KeepAspectRatio))

    def variaralpha(self):
        global ALPHA
        
        alpha=self.ui.slider_alpha.value()
        self.ui.le_alpha.setText(str(alpha/100))
        ALPHA=alpha/100
        #print(type(self.x_float) )       
        scaled_x_float = cv2.convertScaleAbs(self.x_float, alpha=ALPHA, beta=BETA)
        reescaled=(np.maximum(scaled_x_float,0)/scaled_x_float.max())*255
        final_image=np.uint8(reescaled)
        self.final_image=Image.fromarray(final_image)
        self.final_image.save('new_image.jpg')
        self.pixmap = QPixmap('new_image.jpg')
        self.ui.label_2.setPixmap(self.pixmap.scaled(800, 800, Qt.KeepAspectRatio))
        #adjusted_image.save('new_image.jpg')
        #self.pixmap = QPixmap('new_image.jpg')
        #self.ui.label_2.setPixmap(self.pixmap.scaled(800, 800, Qt.KeepAspectRatio))


    def openImageDialog(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Seleccionar Imagen", "", "Imagen DICOM (*.dcm);;Todos los archivos (*)", options=options)

        if file_name:
            x = dicom.dcmread(file_name)
            self.x_float=x.pixel_array.astype(np.float32)
            #print(type(self.x_float))
            reescaled=(np.maximum(self.x_float,0)/self.x_float.max())*255
            final_image=np.uint8(reescaled)

            self.final_image=Image.fromarray(final_image)

            self.final_image.save('new_image.jpg')

            self.pixmap = QPixmap('new_image.jpg')
            os.remove('new_image.jpg')            
            self.ui.label_2.setPixmap(self.pixmap.scaled(800, 800, Qt.KeepAspectRatio))

    
    def saveimage(self):
        options = QFileDialog.Options()
        default_name = "imagen_guardada.png"
        file_name, _ = QFileDialog.getSaveFileName(self, "Guardar Imagen", default_name, "Imagen PNG (*.png);;Todos los archivos (*)", options=options)
        if file_name:
            pixmap = self.ui.label_2.pixmap()
            pixmap.save(file_name, "PNG")

    def normalizar(self):
        print("xfloat",self.x_float)
        self.x_float=normalize_intensity(self.x_float)

        reescaled=(np.maximum(self.x_float,0)/self.x_float.max())*255
        final_image=np.uint8(reescaled)
        final_image=Image.fromarray(final_image)
        final_image.save('hla.jpg')
        pixmap = QPixmap('hla.jpg')
        #os.remove('new_image.jpg')
        
        self.ui.label_2.setPixmap(pixmap.scaled(800, 800, Qt.KeepAspectRatio))

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    MW = MainWindow()
    MW.show()
    sys.exit(app.exec_())