from func import *

if __name__ == "__main__":
    im = Image.open("bird_GT.bmp")
    # contrastStretch(im, [100,100,100], [200,200,200]).save("p3.jpg", "jpeg")
    # gamma(im, 2).save("p4.jpg", "jpeg")
    histogramEqualization(im, [0,0,0],[255,255,255]).save("p5.jpg", "jpeg")