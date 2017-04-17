from func import *

if __name__ == "__main__":
    im = Image.open("bird_GT.bmp")
    print(PSNR(im, nearestNeibor, 0.35))
    print(PSNR(im, bilinear, 0.35))
    print(PSNR(im, bicubic, 0.35))
    # nearestNeibor(im, (600, 600)).save('s1.jpg', 'jpeg')
    # nearestNeibor(im, (100, 100)).save('s2.jpg', 'jpeg')
