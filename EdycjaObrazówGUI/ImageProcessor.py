from PIL import Image, ImageOps, ImageChops, ImageEnhance
import numpy as np

class ImageProcessor:
    def __init__(self, image_path):
        self.image = Image.open(image_path)
        if self.image.mode != 'RGB':
            self.image = self.image.convert('RGB')

    def linear_transform(self, brightness=0, contrast=1, negative=False):
        img = self.image.copy()
        if negative:
            img = ImageOps.invert(img)

        if brightness != 0:
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(1 + brightness / 100)

        if contrast != 1:
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(contrast)

        return img

    def gamma_transform(self, gamma=1.0):
        gamma_map = [int(255 * (i / 255) ** gamma) for i in range(256)]
        gamma_map = gamma_map * 3
        return self.image.point(gamma_map)

    def blend_images(self, other_image_path, mode='normal', alpha=0.5):
        other_img = Image.open(other_image_path).convert('RGB')
        other_img = other_img.resize(self.image.size)

        if mode == 'normal':
            return Image.blend(self.image, other_img, alpha)
        # Additional modes can be added as needed

        return self.image

    def save_image(self, image, output_path):
        image.save(output_path)
