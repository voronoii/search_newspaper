
from PIL import Image
import pytesseract
import argparse
import cv2
import os

tessdata_dir_config = '--tessdata-dir "C:/Program Files (x86)/Tesseract-OCR/tessdata"'
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'

def OCR(imgfile, lang='chi_tra'):
	im = Image.open(imgfile)
	text = pytesseract.image_to_string(im, lang=lang, config=tessdata_dir_config)

	print('+++ Result +++')
	print(text)


def get_prefix_array(string):
    length = len(string)
    array = [0 for i in range(0, len(string))]
    ptn_idx = 0

    for i in range(1, length):
        while ptn_idx > 0 and string[i] != string[ptn_idx]:
            ptn_idx = array[ptn_idx-1]
        if string[i] == string[ptn_idx]:
            ptn_idx += 1
            array[i] = ptn_idx
    return array

def KMP(string, pattern):

    ptn_table = get_prefix_array(pattern)

    length = len(string)
    p_length = len(pattern)
    answer = []
    idx = 0;
    count = 0
    for i in range(0, length):
        while idx > 0 and string[i] != pattern[idx]:
            idx = ptn_table[idx-1]
        if string[i] == pattern[idx]:
            if idx == p_length - 1:
                answer.append(i - p_length + 2)
                count += 1
                idx = ptn_table[idx]
            else:
                idx += 1

    # print("idx : ", max(answer), count)
    answer = sorted(answer)
    return answer, count







import sys
def main():
    
    answer, count = KMP(string, pattern)
    print(count)
    for i in answer: print(i)

    pi = [0 for i in range(0, len(pattern))]
    result = list()
    count = 0
    
    j = 0
    for i in range(1, len(pattern)):
        while (j > 0 and pattern[i] != pattern[j]):
            j = pi[j - 1]
        if (pattern[i] == pattern[j]):
            j += 1
            pi[i] = j
    
    j = 0;
    patternLength = len(pattern)
    textLength = len(string)
    for i in range(0, textLength):
        while (j > 0 and string[i] != pattern[j]):
            j = pi[j - 1]
        if (string[i] == pattern[j]):
            if (j == patternLength - 1):
                ##같은 패턴을 찾았음
                result.append(i - patternLength + 2)
                count += 1
                j = pi[j]
            else:
                j += 1
    
    print(count)
    for c in result:
        print(c)






if __name__ == '__main__':
    main()
