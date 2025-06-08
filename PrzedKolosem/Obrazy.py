from PIL import Image

def negatyw():
    img = Image.open('auto.jpg')
    w, h = img.size
    result = Image.new('RGB', (w, h))
    for i in range(w):
        for j in range(h):
            r, g, b = img.getpixel((i, j))
            r = 255 - r
            g = 255 - g
            b = 255 - b
            result.putpixel((i, j), (r, g, b))
    result.show()
    result.save('negatyw.jpg')

def rozjasnienieLiniowe(c):
    img = Image.open('zdj.jpg')
    w, h = img.size
    result = Image.new('RGB', (w, h))
    for i in range(w):
        for j in range(h):
            r, g, b = img.getpixel((i, j))
            r = min(r + c, 255)
            g = min(g + c, 255)
            b = min(b + c, 255)
            result.putpixel((i, j), (r, g, b))
    result.show()

def przyciemnienieLiniowe(c):
    img = Image.open('zdj.jpg')
    w, h = img.size
    result = Image.new('RGB', (w, h))
    for i in range(w):
        for j in range(h):
            r, g, b = img.getpixel((i, j))
            r = max(r - c, 0)
            g = max(g - c, 0)
            b = max(b - c, 0)
            result.putpixel((i, j), (r, g, b))
    result.show()

def mieszanieObrazow():
    img1 = Image.open('auto.jpg')
    img2 = Image.open('droga.jpg')
    w1, h1 = img1.size
    w2, h2 = img2.size
    w_c = min(w1, w2)
    h_c = min(h1, h2)
    result = Image.new('RGB', (w_c, h_c))
    for i in range(w_c):
        for j in range(h_c):
            r1, g1, b1 = img1.getpixel((i, j))
            r2, g2, b2 = img2.getpixel((i, j))
            r = int(min((r1 + r2)/2, 255))
            g = int(min((g1 + g2)/2, 255))
            b = int(min((b1 + b2)/2, 255))
            result.putpixel((i, j), (r, g, b))
    result.show()

def transformacjaPotegowa(a, c):
    img = Image.open('auto.jpg')
    w, h = img.size
    result = Image.new('RGB', (w, h))
    for i in range(w):
        for j in range(h):
            r, g, b = img.getpixel((i, j))
            r = int(min(a * (r/255 ** c) * 255, 255))
            g = int(min(a * (g/255 ** c) * 255, 255))
            b = int(min(a * (b/255 ** c) * 255, 255))
            result.putpixel((i, j), (r, g, b))
    result.show()

def filtry():
    img = Image.open("auto.jpg")
    w, h = img.size
    filter=[[0, 0, 1], [1, 2, 3], [-2, -2, 3]]
    result = Image.new(('RGB'), (w, h))
    for i in range(1, w-1):
        for j in range(1, h-1):
            tmp_r = 0
            tmp_g = 0
            tmp_b = 0
            for k in range(-1, 2):
                for l in range(-1, 2):
                    r, g, b = img.getpixel((i+k, j+l))
                    tmp_r = r * filter[k+1][l+1]
                    tmp_g = g * filter[k+1][l+1]
                    tmp_b = b * filter[k+1][l+1]
            tmp_r = max(min(tmp_r, 255), 0)
            tmp_g = max(min(tmp_g, 255), 0)
            tmp_b = max(min(tmp_b, 255), 0)
            result.putpixel((i, j), (tmp_r, tmp_g, tmp_b))
    result.show()

filtry()