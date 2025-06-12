from PIL import Image
# ZAD 1
# a)
def maska():
    img = Image.open("auto.jpg")
    w, h = img.size
    maska = [[1, 0, -1], [2, 0, -2], [1, 0, -1]]
    result = Image.new("RGB", (w, h))
    for i in range(1, w-1):
        for j in range(1, h-1):
            tmp_r = 0
            tmp_g = 0
            tmp_b = 0
            for k in range(-1, 2):
                for l in range(-1, 2):
                    r, g, b = img.getpixel((i+k, j+l))
                    tmp_r += r * maska[k+1][l+1]
                    tmp_g += g * maska[k+1][l+1]
                    tmp_b += b * maska[k+1][l+1]
                tmp_r = max(min(tmp_r, 255), 0)
                tmp_g = max(min(tmp_g, 255), 0)
                tmp_b = max(min(tmp_b, 255), 0)
                result.putpixel((i, j), (tmp_r, tmp_g, tmp_b))
    result.show()
# b)
def negatyw_r():
    img = Image.open("auto.jpg")
    w, h = img.size
    result = Image.new("RGB", (w, h))
    for i in range(w):
        for j in range(h):
            r, g, b = img.getpixel((i, j))
            r = 255 - r
            result.putpixel((i, j), (r, g, b))
    result.show()

def wektor_hist():
    img = Image.open("auto.jpg")
    w, h = img.size
    hist_g = [0] * 256
    for i in range(1, w):
        for j in range(1, h):
            r, g, b = img.getpixel((i, j))
            hist_g[g] += 1
