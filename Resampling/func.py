from PIL import Image
import math

def nearestNeibor(img, to_size):
    ret = Image.new(img.mode, to_size)
    sr = img.size[0] * 1.0 / to_size[0] if img.size[0] > to_size[0] else (img.size[0] - 1.0) / to_size[0]
    sc = img.size[1] * 1.0 / to_size[1] if img.size[1] > to_size[1] else (img.size[1] - 1.0) / to_size[1]
    for i in range(to_size[0]):
        for j in range(to_size[1]):
            ret.putpixel((i,j), img.getpixel((round(i * sr), round(j * sc))))
    return ret

def bilinear(img, to_size):
    ret = Image.new(img.mode, to_size)
    sr = img.size[0] * 1.0 / to_size[0]
    sc = img.size[1] * 1.0 / to_size[1]
    for i in range(to_size[0]):
        for j in range(to_size[1]):
            rf = i * sr
            cf = j * sc
            r = int(rf)
            c = int(cf)
            dr = rf - r
            dc = cf - c
            pix2 = [0, 0, 0]
            if(r + 1 >= img.size[0] or c + 1 >= img.size[1]):
                ret.putpixel((i,j), img.getpixel((int(i * sr), int(j * sc))))
            else:
                for k in range(3):
                    pix2[k] += (img.getpixel((r,c))[k] * (1 - dr) * (1 - dc) +
                        img.getpixel((r + 1, c))[k] * dr * (1 - dc) +
                        img.getpixel((r, c + 1))[k] * (1 - dr) * dc +
                        img.getpixel((r + 1, c + 1))[k] * dr * dc)
                    pix2[k] = int(round(pix2[k]))
                ret.putpixel((i, j), tuple(pix2))
    return ret
def bicubic_p(x):
    # q = lambda x:x if x > 0 else 0
    # return 1.0/6 * (q(x + 2)**3 + 4 * q(x + 1)**3 - 6 * q(x)**3 - 4*q(x - 1**3))
    a = -0.5
    if abs(x) < 1:
        return (a + 2) * abs(x)**3 - (a + 3) * x * x + 1
    elif abs(x) < 2:
        return a * abs(x)**3 - 5 * a * x * x + 8 * a * abs(x) - 4 * a
    else: 
        return 0
def bicubic(img, to_size):
    ret = Image.new(img.mode, to_size)
    sr = img.size[0] * 1.0 / to_size[0]
    sc = img.size[1] * 1.0 / to_size[1]
    for i in range(to_size[0]):
        for j in range(to_size[1]):
            rf = i * sr
            cf = j * sc
            r = int(rf)
            c = int(cf)
            dr = rf - r
            dc = cf - c
            pix2 = [0, 0, 0]
            if(r - 1 < 0 or c - 1 < 0 or r + 2 >= img.size[0] or c + 2 >= img.size[1]):
                ret.putpixel((i,j), img.getpixel((int(i * sr), int(j * sc))))
            else:
                for k in range(3):
                    for m in range(-1, 3):
                        for n in range(-1, 3):
                            # if r + m >= 0 and c + n >= 0 and r + m < img.size[0] and c + n < img.size[1]:
                            pix2[k] += img.getpixel((r + m, c + n))[k] * bicubic_p(dr - m) * bicubic_p(dc - n)
                    pix2[k] = int(round(pix2[k]))
                ret.putpixel((i, j), tuple(pix2))
    return ret

def PSNR(img, method, alpha = 0.25):
    small = method(img, (int(img.size[0] * alpha), int(img.size[1] * alpha)))
    res = method(small, img.size)
    mse = 0
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            for k in range(3):
                mse += (img.getpixel((i,j))[k] - res.getpixel((i,j))[k])**2
    mse /= 3. * img.size[0] * img.size[1]
    return 10 * math.log(255.0 * 255 / mse) / math.log(10)