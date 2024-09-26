import sys
import cv2 


cap = cv2.VideoCapture("video.mp4")

if not cap.isOpened():
    sys.exit("카메라 연결 실패")

captures = []
    
while True:
    ret, frame = cap.read()
    
    if ret:
        cv2.imshow("Video display" , frame)
        key = cv2.waitKey(1)
        if key == ord('c'):
            captures.append(frame)
            print(captures)
        elif key == ord('q'):
            break
    
cap.release()
cv2.destroyAllWindows()

## 캡쳐된 프레임 저장
if len(captures) > 0 :
    for i,capture in enumerate(captures):
        cv2.imwrite(f"./outputs/frame-{i}.jpg", capture)
    