from PIL import Image
import math

def fast(img, distinct, r = 3, threshold = 0.7):
    img = img.convert('L')
    print img
    circle_list = [(-r, 0), (r, 0), (0, -r), (0, r)]
    # 1
    for i in range(1, r):
        minv = 1e10
        for j in range(0, r):
            if abs(i * i + j * j - r * r) < minv:
                minv = abs(i * i + j * j - r * r)
                best = (i,j)
        circle_list.append(best)
    l1 = len(circle_list)
    # 4 
    circle_list.append((r,0))
    for i in range(l1 - 1, 3, -1):
        circle_list.append((circle_list[i][0], - circle_list[i][1]))
    # 3
    circle_list.append((0,-r))
    for i in range(4, l1):
        circle_list.append((-circle_list[i][0], - circle_list[i][1]))
    # 2
    circle_list.append((-r,0))
    for i in range(l1 - 1, 3, -1):
        circle_list.append((-circle_list[i][0],circle_list[i][1]))        
    print circle_list

    t = int(threshold * (len(circle_list) - 3))
    ans = []
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            s = 0
            for k in range(4):
                if i + circle_list[k][0] < 0 or i + circle_list[k][0] >= img.size[0] or j + circle_list[k][1] < 0 or j + circle_list[k][1] >= img.size[1]:
                    continue
                s += abs(img.getpixel((i,j)) - img.getpixel((i + circle_list[k][0], j + circle_list[k][1]))) > distinct
            if(s >= 3):
                s = 0
                last = 2
                for k in range(3, len(circle_list)):
                    if i + circle_list[k][0] < 0 or i + circle_list[k][0] >= img.size[0] or j + circle_list[k][1] < 0 or j + circle_list[k][1] >= img.size[1]:
                        continue
                    now = img.getpixel((i,j)) - img.getpixel((i + circle_list[k][0], j + circle_list[k][1]))
                    if now < -distinct:
                        now = -1
                    elif now > distinct:
                        now = 1
                    else:
                        now = 0
                    if now != last:
                        s = 0
                    else:
                        s += 1
                        if s >= t:
                            ans.append((i,j))
                            break
                    last = now
    return ans
            