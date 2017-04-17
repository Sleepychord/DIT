from fast import fast
from PIL import Image
from brief import *
if __name__ == "__main__":
    im1 = Image.open("left.jpeg")
    im2 = Image.open("right.jpeg")
    # tmp1 = fast(im1, 45)
    # tmp2 = fast(im2, 45)
    # m,u = briefMatch(im1, tmp1, im2, tmp2)
    # for x in tmp1:
    #     im1.putpixel(x, (255, 255, 255))
    # for x in tmp2:
    #     im2.putpixel(x, (255, 255, 255))

    savef = open('savef.txt','r')
    # savef.write(str((m,u)))
    (m,u) = eval(savef.read())
    visualizeMatch(im1, im2, m, u, class_num = 12, validnum = 3, max_matched = 10)
    # tmp = [(1,1), (2,2), (4,4), (5,5), (8,7), (3,4), (6,9),(10,11)]
    # for t in kmeans(tmp, 3):
    #     print getBox(t)
