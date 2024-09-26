import sys
import cv2

img = cv2.imread("./4weeks/gly.jpg")

if img is None:
    sys.exit("파일을 찾을 수 없습니다.")
    
# I = round(0.299*R+0.587*G+0.114*B)
    
gry = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
resized_img = cv2.resize(gry, dsize=(0,0), fx=0.5 , fy=0.5)


cv2.imshow("Coloer img" , img)
cv2.imshow("gry img" , gry) # <--
cv2.imshow("resized img" , resized_img) # <-- 
cv2.waitKey()
cv2.destroyAllWindows()


