import cv2 as cv
import numpy as np
import winsound
import sys
from PyQt6.QtWidgets import *
# from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QImage, QPixmap

class PanoramaViewer(QLabel):
    def __init__(self, panorama_image):
        super().__init__()
        self.panorama_image = panorama_image
        self.image_width = panorama_image.shape[1]
        self.display_width = 700  # 화면에 표시할 가로 크기
        self.offset = 0
        self.update_display()

    def update_display(self):
        # offset에 따라 이미지의 특정 구간만 보여줌 (360도 회전 없이 시작과 끝에서 멈춤)
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
        self.setGeometry(200, 200, 700, 100)
        
        collectButton = QPushButton("영상 수집", self)
        self.showButton = QPushButton("영상 보기", self)
        self.stitchButton = QPushButton("봉합", self)
        self.saveButton = QPushButton("저장", self)
        quitButton = QPushButton("나가기", self)
        self.label = QLabel("환영합니다!", self)
        
        collectButton.setGeometry(10, 25, 100, 30)
        self.showButton.setGeometry(110, 25, 100, 30)
        self.stitchButton.setGeometry(210, 25, 100, 30)
        self.saveButton.setGeometry(310, 25, 100, 30)
        quitButton.setGeometry(450, 25, 100, 30)
        self.label.setGeometry(10, 70, 600, 170)
        
        self.showButton.setEnabled(False)
        self.stitchButton.setEnabled(False)
        self.saveButton.setEnabled(False)
        
        collectButton.clicked.connect(self.collectFunction)
        self.showButton.clicked.connect(self.showFunction)
        self.stitchButton.clicked.connect(self.stitchFunction)
        self.saveButton.clicked.connect(self.saveFunction)
        quitButton.clicked.connect(self.quitFunction)
        
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
            # 파노라마 이미지가 성공적으로 생성되면, PanoramaViewer를 사용해 스크롤 가능하게 표시
            self.viewer = PanoramaViewer(self.img_stitched)  # PanoramaViewer는 스크롤 가능한 커스텀 QLabel 클래스
            self.setCentralWidget(self.viewer)  # 파노라마 뷰어를 중앙 위젯으로 설정
            self.label.setText("좌우로 드래그하여 파노라마를 보세요.")
        else:
            # 스티칭 실패 시 알림과 함께 메시지 표시
            winsound.Beep(3000, 500)
            self.label.setText("파노라마 제작에 실패하였습니다. 다시 시도하세요.")
        
    def saveFunction(self):
        fname = QFileDialog.getSaveFileName(self, '파일 저장', './')
        if fname[0]:  # 사용자가 파일 이름을 선택한 경우에만 저장 수행
            cv.imwrite(fname[0], self.img_stitched)
    
    def quitFunction(self):
        try:
            self.cap.release()
        except AttributeError:
            # 만약 캡처가 종료된 경우 오류 발생 방지
            pass
        cv.destroyAllWindows()
        self.close()
    
app = QApplication(sys.argv)
win = Panorama()
win.show()
app.exec()
