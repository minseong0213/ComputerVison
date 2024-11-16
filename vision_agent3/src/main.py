import cv2 as cv
import numpy as np
import winsound

import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QImage, QPixmap

class PanoramaViewer(QLabel):
    def __init__(self, panorama_image):
        super().__init__()
        self.panorama_image = panorama_image
        self.image_width = panorama_image.shape[1]
        self.display_width = 700  
        self.offset = 0
        self.update_display()

    def update_display(self):

        start_x = max(0, min(self.offset, self.image_width - self.display_width))
        view = self.panorama_image[:, start_x:start_x + self.display_width]
        
        q_image = QImage(view.tobytes(), view.shape[1], view.shape[0], view.shape[1] * 3, QImage.Format.Format_BGR888)
        self.setPixmap(QPixmap.fromImage(q_image))

    def mousePressEvent(self, event):
        self.last_x = event.pos().x()

    def mouseMoveEvent(self, event):
        dx = event.pos().x() - self.last_x
        self.last_x = event.pos().x()
        self.offset = self.offset - dx  # offset 업데이트
        self.update_display()

class Panorama(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("파노라마 영상")
        self.setGeometry(200, 200, 700, 200)
        
        self.collectButton = QPushButton("영상 수집", self)
        self.showButton = QPushButton("영상 보기", self)
        self.stitchButton = QPushButton("봉합", self)
        self.saveButton = QPushButton("저장", self)
        quitButton = QPushButton("나가기", self)
        self.label = QLabel("환영합니다!", self)
        
        self.collectButton.setGeometry(10, 25, 100, 30)
        self.showButton.setGeometry(110, 25, 100, 30)
        self.stitchButton.setGeometry(210, 25, 100, 30)
        self.saveButton.setGeometry(310, 25, 100, 30)
        quitButton.setGeometry(450, 25, 100, 30)
        self.label.setGeometry(10, 70, 600, 170)
        
        self.showButton.setEnabled(False)
        self.stitchButton.setEnabled(False)
        self.saveButton.setEnabled(False)
        
        self.collectButton.clicked.connect(self.collectFunction)
        self.showButton.clicked.connect(self.showFunction)
        self.stitchButton.clicked.connect(self.stitchFunction)
        self.saveButton.clicked.connect(self.saveFunction)
        quitButton.clicked.connect(self.quitFunction)
        
        self.collectButton.setObjectName("collectButton")  
        
    def collectFunction(self):
        self.showButton.setEnabled(False)
        self.stitchButton.setEnabled(False)
        self.saveButton.setEnabled(False)
        self.label.setText('c를 여러번 눌러 수집하고 끝나면 q를 눌러 비디오를 끔')
        
        self.cap = cv.VideoCapture(0, cv.CAP_DSHOW)
        if not self.cap.isOpened(): sys.exit('카메라 연결 실패')
        
        self.imgs = []
        while True:
            ret, frame = self.cap.read()
            if not ret: break
            
            cv.imshow("video display", frame)
            
            key = cv.waitKey(1)
            if key == ord('c'):
                self.imgs.append(frame)
            elif key == ord('q'):
                self.cap.release()
                cv.destroyWindow('video display')
                break
            
            if len(self.imgs) >= 2:
                self.showButton.setEnabled(True)
                self.stitchButton.setEnabled(True)
                self.saveButton.setEnabled(True)
                    
    def showFunction(self):
        self.label.setText('수집된 영상은 ' + str(len(self.imgs)) + '장 입니다.')
        stack = cv.resize(self.imgs[0], dsize=(0, 0), fx=0.25, fy=0.25)
        for i in range(1, len(self.imgs)):
            stack = np.hstack((stack, cv.resize(self.imgs[i], dsize=(0, 0), fx=0.25, fy=0.25)))
        cv.imshow("Image collection", stack)
        

    def stitchFunction(self):
        stitcher = cv.Stitcher_create()
        status, self.img_stitched = stitcher.stitch(self.imgs)
        
        if status == cv.STITCHER_OK:
            self.viewer_window = QMainWindow()  
            self.viewer_window.setWindowTitle("파노라마 뷰어")
            self.viewer_window.setGeometry(300, 300, 700, 400)  
            
            self.viewer = PanoramaViewer(self.img_stitched) 
            self.viewer_window.setCentralWidget(self.viewer)  
            

            self.collectButton.setEnabled(False)  
            self.viewer_window.show()  
            
            self.viewer_window.closeEvent = self.enable_collect_button
            
            self.label.setText("파노라마가 성공적으로 생성되었습니다. 새 창에서 확인하세요.")
        else:
            self.label.setText("파노라마 제작에 실패하였습니다. 다시 시도하세요.")

    def enable_collect_button(self, event):
        collect_button = self.findChild(QPushButton, "collectButton")
        if collect_button:
            collect_button.setEnabled(True)
        event.accept()  

    def saveFunction(self):
        fname = QFileDialog.getSaveFileName(self, '파일 저장', './','Images (*.png *.jpg *.bmp)')
        if fname[0]:  
            cv.imwrite(fname[0], self.img_stitched)
    
    def quitFunction(self):
        try:
            self.cap.release()
        except AttributeError:
            pass
        cv.destroyAllWindows()
        self.close()
    
app = QApplication(sys.argv)
win = Panorama()
win.show()
app.exec()
