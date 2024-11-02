import sys
import winsound
from PyQt6.QtWidgets import QMainWindow, QLabel , QPushButton, QApplication

class BeepSound(QMainWindow):
    def __init__(self):
        super().__init__()
        
        short_beep_btn = QPushButton("짧게 삑", self)
        long_beep_btn = QPushButton("길게 삑", self)
        quit_btn = QPushButton("나가기", self)
        label = QLabel("환영합니다!" , self)
        
        self.setGeometry(200, 200, 500, 100)
        self.setGeometry(200, 200, 500, 100)
        self.setGeometry(200, 200, 500, 100)
        
    def short_beep(self):
        self.label.setText("주파수 1000으로 0.5초 동안 삑소리를 냅니다.")
        
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = BeepSound()
    win.show()
    app.exec()
        
        