import random

def dist2(a, b):
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2
def cluster(points, centers):
    has = []
    for i in range(len(centers)):
        has.append([])
    for i in range(len(points)):
        p = points[i]
        minv = float('Inf')
        idx = -1
        for j in range(len(centers)):
            c = centers[j]
            if dist2(p, c) < minv:
                minv = dist2(p, c)
                idx = j
        has[idx].append(i)
    return has
def calcCenters(points, has):
    centers = []
    for i in range(len(has)):
        if len(has[i]) == 0:
            continue
        meanx = 0
        meany = 0
        for idx in has[i]:
            meanx += points[idx][0]
            meany += points[idx][1]
        meanx /= 1.0 * len(has[i])
        meany /= 1.0 * len(has[i])
        centers.append((meanx, meany))
    return centers

def kmeans(points, class_num, iter = 50):
    random.shuffle(points)
    centers = points[:class_num]
    for i in range(iter):
        print 'iter %d' % i
        has = cluster(points, centers)
        centers = calcCenters(points, has)
    # change idx to points
    for t in has:
        for j in range(len(t)):
            t[j] = points[t[j]]
    return has

def getBox(points):
    ret = [1e10, 0, 1e10, 0]
    for p in points:
        ret[0] = min(ret[0], p[0])
        ret[1] = max(ret[1], p[0])
        ret[2] = min(ret[2], p[1])
        ret[3] = max(ret[3], p[1])
    return ret
            