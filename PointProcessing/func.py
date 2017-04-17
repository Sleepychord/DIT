from PIL import Image
import math

def changeBrightness(img, inc):
    ret = img.copy()
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            (r,g,b) = img.getpixel((i,j))
            r1 = max(min(255, r + inc),0)
            g1 = max(min(255, g + inc),0)
            b1 = max(min(255, b + inc),0)
            ret.putpixel((i,j), (r1, g1, b1))
    return ret    

def changeContrast(img, alpha):
    ret = img.copy()
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            (r,g,b) = img.getpixel((i,j))
            r1 = int(round(max(min(255, (r - 127) * alpha + 127),0)))
            g1 = int(round(max(min(255, (g - 127) * alpha + 127),0)))
            b1 = int(round(max(min(255, (b - 127) * alpha + 127),0)))
            ret.putpixel((i,j), (r1, g1, b1))
    return ret   
def contrastStretch(img, m1, m2):
    n1 = [255, 255, 255]
    n2 = [0, 0, 0]
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            pix = img.getpixel((i,j))
            for k in range(3):
                if pix[k] < n1[k]:
                    n1[k] = pix[k]
                if pix[k] > n2[k]:
                    n2[k] = pix[k]
    ret = img.copy()
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            pix = img.getpixel((i,j))
            pix2 = [0, 0, 0]
            for k in range(3):
                pix2[k] = (m2[k] - m1[k]) * (pix[k] - n1[k]) * 1.0 / (n2[k] - n1[k]) + m1[k]
                pix2[k] = int(round(pix2[k]))
            ret.putpixel((i,j), tuple(pix2))
    return ret
def gamma(img, ga):
    ret = img.copy()
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            (r,g,b) = img.getpixel((i,j))
            r1 = int(round(255 * math.pow(r / 255.0, 1.0 / ga)))
            g1 = int(round(255 * math.pow(g / 255.0, 1.0 / ga)))
            b1 = int(round(255 * math.pow(b / 255.0, 1.0 / ga)))
            ret.putpixel((i,j), (r1, g1, b1))
    return ret   

def histogram(img):
    h = [[0] * 256,[0]* 256,[0]* 256]
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            pix = img.getpixel((i,j))
            for k in range(3):
                h[k][pix[k]] += 1
    return h
def cummulativeHistogram(img):
    h = histogram(img)
    for k in range(3):
        for i in range(1, 256):
            h[k][i] = h[k][i - 1] + h[k][i]
    for k in range(3):
        for i in range(256):
            h[k][i] = h[k][i] * 1.0 / h[k][255]
    return h

def histogramEqualization(img, m1, m2, d = [0, 1, 2]):
    '''
        d is the channels to be equalized
    '''
    ret = img.copy()
    p = cummulativeHistogram(img)
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            pix = img.getpixel((i,j))
            pix2 = list(pix)
            for k in d:
                pix2[k] = (m2[k] - m1[k]) * p[k][pix[k]] + m1[k]
                pix2[k] = int(round(pix2[k]))
            ret.putpixel((i,j), tuple(pix2))
    return ret

def histogramMatch(img1, img2, d = [0,1,2]):
    p1 = cummulativeHistogram(img1)
    p2 = cummulativeHistogram(img2)
    for k in d:
        p2_idx = 0
        for i in range(256):
            while p1[k][i] >= p2[k][p2_idx] and p2_idx < 255:
                p2_idx += 1
            p1[k][i] = p2_idx
    ret = img1.copy()
    for i in range(img1.size[0]):
        for j in range(img1.size[1]):
            pix = img1.getpixel((i,j))
            pix2 = list(pix)
            for k in d:
                pix2[k] = p1[k][pix[k]]
            ret.putpixel((i, j), tuple(pix2))
    return ret