from PIL import Image
import numpy as np
import matplotlib.pyplot as plt


def adjust_brightness(img, value):
    """Zmienia jasność obrazu o podaną wartość."""
    img_array = np.array(img, dtype=np.int16)
    img_array = np.clip(img_array + value, 0, 255)
    return Image.fromarray(img_array.astype(np.uint8))


def negative(img):
    """Tworzy negatyw obrazu za pomocą pętli for."""
    w, h = img.size
    neg_img = Image.new("RGB", (w, h))

    for i in range(w):
        for j in range(h):
            r, g, b = img.getpixel((i, j))
            neg_img.putpixel((i, j), (255 - r, 255 - g, 255 - b))

    return neg_img

img = Image.open("bialystok.jpg")

bright_img = adjust_brightness(img, 50)
dark_img = adjust_brightness(img, -50)
negative_img = negative(img)

images = [img, bright_img, dark_img, negative_img]

for image in images:
    plt.imshow(image)
    plt.axis("off")
    plt.show()
