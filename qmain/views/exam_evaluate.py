from PyPDF2 import PdfFileWriter, PdfFileReader
from pytesseract import pytesseract
from difflib import SequenceMatcher
from PIL import Image
from pdf2image import convert_from_path
from pdf2image.exceptions import *
import matplotlib.pyplot as plt
# from keras.models import load_model
# from keras.preprocessing.image import load_img
# from keras.preprocessing.image import img_to_array
from imutils.perspective import four_point_transform
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2
import os
import io
pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR\\tesseract'


# def checkIfContains(outside, inside):        
#     return (inside[0] > outside[0] and inside[0] + inside[2]  < outside[0] + outside[2] and inside[1] > outside[1] and inside[1] + inside[3] < outside[1] + outside[3])

# def filterRectangles(rects):
#     #Checks if each contour contains some other contous - neccesary to avoid
#     #spotting two "0" inside of 8 etc.
#     rects_filtered = []
#     flag = 0
#     for i in range(0, len(rects)):
#         for j in range(0, len(rects)):
#             if(checkIfContains(rects[j], rects[i])):
#                 flag = 1
#                 break
#         if(flag == 0):
#             rects_filtered.append(rects[i])
#         else:
#             flag = 0
#     return rects_filtered

# def load_image(filename, show=True):
#     img_original = load_img(filename)
#     # load the image
#     img = load_img(filename, grayscale=True, target_size=(28, 28))
#     # convert to array
#     img = img_to_array(img)
#     # reshape into a single sample with 1 channel
#     img = img.reshape(1, 28, 28, 1)
#     # prepare pixel data
#     img = img.astype('float32')
#     img = img / 255.0      
#     return img

# def student_id(filename):
#     sample = cv2.imread(filename)
#     white_image = np.zeros(sample.shape) + 255
#     I = cv2.resize(cv2.cvtColor(sample, cv2.COLOR_BGR2GRAY), (700,600))   
#     B = cv2.adaptiveThreshold(I,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)
#     median = B 
#     for i in range(0,7):
#         median = cv2.medianBlur(median,3)

#     ctr, hierarchy = cv2.findContours(B, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#     ctr = list(filter(lambda el : el.shape[0]>20 and el.shape[0]<500, ctr))

#     for i in range(0,100):
#         cv2.drawContours(white_image, ctr, -1, (0,0,30))
#     rects = []
#     i=0
#     I_1 = B.copy()
#     for c in ctr:
#         peri = cv2.arcLength(c, True)
#         approx = cv2.approxPolyDP(c, 0.02 * peri, True)
#         x, y, w, h = cv2.boundingRect(approx)
#         rect = (x, y, w, h) 
#         rects.append(rect)
#     filtered = filterRectangles(rects)
#     I_2 = B.copy()
#     for i in range(0, len(filtered)):
#         cv2.rectangle(I_2, (filtered[i][0], filtered[i][1]), (filtered[i][0]+filtered[i][2], filtered[i][1]+filtered[i][3]), (0, 255, 0), 1);
#     i=0
#     resized = []
#     id=''
#     filtered.sort(key = lambda x: x[0])
#     for f in filtered:
#         t = cv2.bitwise_not(median[f[1] - int(f[3]*0.1):f[1]+int(f[3]*1.1), f[0] - int(f[2]*0.1):f[0]+int(1.1*f[2])])
#         resized = cv2.resize(t, (40,40))
#         cv2.imwrite("0000"+ str(i) + ".jpg", resized)
#         new = load_image("0000"+ str(i) + ".jpg", resized)
#         model=load_model("qmain/views/d1.h5")
#         digit = model.predict_classes(new)
#         i+=1
#         id += str(digit[0])
#     return id    

def get_mark(path, path_answers):
    img_cv = cv2.imread(path)
    img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
    new = pytesseract.image_to_string(img_rgb)
    true_answers = open(path_answers).read()
    mark = SequenceMatcher(None, new, true_answers).ratio() * 1388 
    return mark

def exam_evaluate_map(path):
    fname = os.path.splitext(os.path.basename(path))[0]
    pdf = PdfFileReader(path)
    pages = convert_from_path(path, 200)
    count = 1
    data = dict()
    for page in pages:
        image_name = 'media/diploma/{}_page_{}.png'.format(fname, count)
        page.save(image_name,'PNG')
        img = Image.open(image_name)
        img = cv2.imread(image_name)
        #cropped_image = img[160:250, 1100:1450]
        cropped_image = img[160:250, 400:850]
        #cv2.imwrite('media/diploma/student_id.png', cropped_image)
        #id = student_id('media/diploma/student_id.png')
        #print(id)
        student_full_name = pytesseract.image_to_string(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB))
        data[student_full_name] = image_name 
        count += 1
    return data

# exam_evaluate_map('media/diploma_page_4.pdf')




def mark(path, answers):
    ANSWER_KEY = answers
    image = cv2.imread(path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 75, 200)

    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    docCnt = None

    if len(cnts) > 0:
     
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
        for c in cnts:
            
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)

            if len(approx) == 4:
                docCnt = approx
                break
                
    paper = four_point_transform(image, docCnt.reshape(4, 2))
    warped = four_point_transform(gray, docCnt.reshape(4, 2))

    thresh = cv2.threshold(warped, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

    
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    questionCnts = []

    
    for c in cnts:
       
        (x, y, w, h) = cv2.boundingRect(c)
        ar = w / float(h)

        if w >= 20 and h >= 20 and ar >= 0.9 and ar <= 1.1:
            questionCnts.append(c)
    
    
    questionCnts = contours.sort_contours(questionCnts,method="top-to-bottom")[0]
    correct = 0

    for (q, i) in enumerate(np.arange(0, len(questionCnts), 5)):
        cnts = contours.sort_contours(questionCnts[i:i + 5])[0]
        bubbled = None
        for (j, c) in enumerate(cnts):
           
            mask = np.zeros(thresh.shape, dtype="uint8")
            cv2.drawContours(mask, [c], -1, 255, -1)

            mask = cv2.bitwise_and(thresh, thresh, mask=mask)
            total = cv2.countNonZero(mask)

            if bubbled is None or total > bubbled[0]:
                bubbled = (total, j)

        color = (0, 0, 255)
        k = ANSWER_KEY[q]

        if k == bubbled[1]:
            color = (0, 255, 0)
            correct += 1

        score = (correct / 5.0) * 100
    return score
