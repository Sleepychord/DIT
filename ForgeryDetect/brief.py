from PIL import Image, ImageDraw
import math
import random
from kmeans import kmeans, getBox

class Brief:
    def __init__(self, S = 40, box = 2, num = 256):
        self.S = 40
        self.box = 5
        self.points = []
        self.num = 256
        for i in range(num):
            self.points.append((round(random.gauss(0, S / 5.)), round(random.gauss(0, S / 5.)), round(random.gauss(0, S / 5.)), round(random.gauss(0, S / 5.))))
    def boxSum(self,img, p):
        ret = 0
        for i in range(-self.box, self.box + 1):
            for j in range(-self.box, self.box +1):
                x1 = p[0] + i
                y1 = p[1] + j
                if x1 >= 0 and y1 >= 0 and x1 < img.size[0] and y1 < img.size[1]:
                    ret += img.getpixel((x1, y1))
        return ret
    def embed(self, img, p):
        img = img.convert('L')
        ret = [0] * self.num
        for i in range(self.num):
            (x1, y1, x2, y2) = self.points[i]
            x1 += p[0]
            x2 += p[0]
            y1 += p[1]
            y2 += p[1]
            if self.boxSum(img,(x1, y1)) > self.boxSum(img, (x2, y2)):
                ret[i] = 1
        return ret
    
def hamming(l1, l2):
    ret = 0
    for i in range(len(l1)):
        ret += l1[i] ^ l2[i]
    return ret

def briefMatch(img1, p1, img2, p2, limit = 80, dnum = 3):
    descriptors = []
    for i in range(dnum):
        descriptors.append(Brief())
    binarys1 = [] # points * des * binary
    tot = 0
    print len(p1)
    print len(p2)
    for p in p1:
        tot += 1
        print 'construct %d in img1' % tot
        binarys1.append([])
        for des in descriptors:
            binarys1[-1].append(des.embed(img1, p))
    binarys2 = [] # points * des * binary
    for p in p2:
        binarys2.append([])
        for des in descriptors:
            binarys2[-1].append(des.embed(img2, p))    
    # find the nearest
    ret = []
    matched = [False] * len(binarys2)
    for i in range(len(binarys1)):
        print 'match point %d' % i
        pbs1 = binarys1[i]
        minv = 256
        match = 0
        for j in range(len(binarys2)):
            pbs2 = binarys2[j]
            s = 0
            for k in range(len(pbs1)):
                s += hamming(pbs1[k], pbs2[k])
            s /= 1.0 * len(pbs1)
            if s < minv:
                minv = s
                match = j
        if minv < limit:
            matched[match] = True
            ret.append((p1[i], p2[match]))
    # find unmatched points
    unmatch = []
    for i in range(len(binarys2)):
        if not matched[i]:
            unmatch.append(p2[i])
    return ret, unmatch

def visualizeMatch(img1, img2, m, unmatch, class_num = 10, validnum = 3, max_matched = 15):
    row = img1.size[0] + img2.size[0]
    col = max(img1.size[1], img2.size[1])
    ans = Image.new('RGB', (row, col))
    ans.paste(img1, (0, 0))
    ans.paste(img2, (img1.size[0], 0))
    draw = ImageDraw.Draw(ans)
    for match in m:
        draw.line((match[0],match[1][0] + img1.size[0], match[1][1]), fill = (random.randint(0, 16) * 16 ,random.randint(0, 16) * 16, random.randint(0, 16) * 16))
    for t in kmeans(unmatch, class_num):
        if len(t) >= validnum:
            box = getBox(t)
            print box
            s = 0
            for match in m:
                if box[0] <= match[1][0] <= box[1] and box[2] <= match[1][1] <= box[3]: 
                    s += 1
            if s < max_matched:
                draw.rectangle([box[0]+ img1.size[0], box[2], box[1]+ img1.size[0], box[3]], outline = 'red')
    del draw
    ans.save("matches.jpeg", 'jpeg')