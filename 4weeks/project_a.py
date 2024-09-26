import sys

import cv2
import numpy as np

def convert_gray(img):
    R, G ,B = cv2.split(img)
    cvt_img = np.round(0.299*R+0.587*G+0.114*B).astype(np.uint8) ## np.round() => float64형식
                                                                 ## imshow()는 일반적으로 uint8 형식을 지원 따라서 현재 배열을 uint8 형식로 변환해야함 
    return cvt_img

img = cv2.imread("./4weeks/gly.jpg")

if img is None:
    sys.exit("파일을 찾을 수 없습니다.")
    
# I = round(0.299*R+0.587*G+0.114*B)
# TODO : 컬러 사진을 흑백사진으로 변환하기

cvt_img = convert_gray(img)

cv2.imshow("img", cvt_img)
cv2.waitKey()
cv2.destroyAllWindows()



