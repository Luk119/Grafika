from PIL import Image, ImageOps, ImageChops, ImageFilter, ImageEnhance
import numpy as np
import matplotlib.pyplot as plt

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
        gamma_map = [int(255 * (i / 255) ** gamma) for i in range(256)] * 3
        return self.image.point(gamma_map)

    def blend_images(self, other_image_path, mode='normal', alpha=0.5):
        other_img = Image.open(other_image_path).convert('RGB')
        other_img = other_img.resize(self.image.size)

        if mode == 'normal':
            return Image.blend(self.image, other_img, alpha)
        elif mode == 'add':
            return ImageChops.add(self.image, other_img, scale=1.0)
        elif mode == 'subtract':
            return ImageChops.subtract(self.image, other_img)
        elif mode == 'multiply':
            return ImageChops.multiply(self.image, other_img)
        elif mode == 'screen':
            return ImageChops.screen(self.image, other_img)
        elif mode == 'overlay':
            return ImageChops.overlay(self.image, other_img)
        elif mode == 'soft_light':
            return ImageChops.soft_light(self.image, other_img)
        elif mode == 'hard_light':
            return ImageChops.hard_light(self.image, other_img)
        elif mode == 'darken':
            return ImageChops.darker(self.image, other_img)
        elif mode == 'lighten':
            return ImageChops.lighter(self.image, other_img)
        elif mode == 'difference':
            return ImageChops.difference(self.image, other_img)
        elif mode == 'exclusion':
            return ImageChops.invert(ImageChops.difference(
                ImageChops.invert(self.image),
                ImageChops.invert(other_img)))
        elif mode in ['divide', 'dodge', 'burn', 'and', 'or', 'xor']:
            return self._blend_numpy_mode(self.image, other_img, mode)
        else:
            return self.image

    def _blend_numpy_mode(self, img1, img2, mode):
        arr1 = np.asarray(img1).astype(np.float32)
        arr2 = np.asarray(img2).astype(np.float32)

        if mode == 'divide':
            result = np.clip((arr1 / (arr2 + 1)) * 255, 0, 255)
        elif mode == 'dodge':
            result = np.clip(255 * arr1 / (255 - arr2 + 1), 0, 255)
        elif mode == 'burn':
            result = 255 - np.clip(255 * (1 - arr1 / 255) / (arr2 / 255 + 1e-6), 0, 255)
        elif mode == 'and':
            result = np.bitwise_and(arr1.astype(np.uint8), arr2.astype(np.uint8))
        elif mode == 'or':
            result = np.bitwise_or(arr1.astype(np.uint8), arr2.astype(np.uint8))
        elif mode == 'xor':
            result = np.bitwise_xor(arr1.astype(np.uint8), arr2.astype(np.uint8))
        else:
            result = arr1

        return Image.fromarray(result.astype(np.uint8))

    def adjust_contrast(self, factor=1.0):
        enhancer = ImageEnhance.Contrast(self.image)
        return enhancer.enhance(factor)

    def generate_histogram(self):
        r, g, b = self.image.split()
        plt.figure(figsize=(10, 5))
        plt.plot(r.histogram(), color='red', label='Red')
        plt.plot(g.histogram(), color='green', label='Green')
        plt.plot(b.histogram(), color='blue', label='Blue')
        plt.title('Color Histogram')
        plt.xlabel('Pixel Value')
        plt.ylabel('Frequency')
        plt.legend()
        plt.grid(True)
        plt.show()

    def equalize_histogram(self):
        img_yuv = self.image.convert('YCbCr')
        y, u, v = img_yuv.split()
        y_eq = ImageOps.equalize(y)
        img_yuv_eq = Image.merge('YCbCr', (y_eq, u, v))
        return img_yuv_eq.convert('RGB')

    def scale_histogram(self, min_out=0, max_out=255):
        img_array = np.array(self.image)
        min_in = img_array.min()
        max_in = img_array.max()
        scaled = (img_array - min_in) * ((max_out - min_out) / (max_in - min_in)) + min_out
        return Image.fromarray(np.clip(scaled, 0, 255).astype(np.uint8))

    def low_pass_filter(self, filter_type='average', size=3):
        if filter_type == 'average':
            return self.image.filter(ImageFilter.BoxBlur(size))
        elif filter_type == 'gaussian':
            return self.image.filter(ImageFilter.GaussianBlur(size))
        else:
            return self.image

    def high_pass_filter(self, filter_type='laplace1'):
        img_gray = self.image.convert('L')
        img_array = np.array(img_gray)

        kernels = {
            'roberts_x': np.array([[0, 0, 0], [0, 1, 0], [0, 0, -1]]),
            'roberts_y': np.array([[0, 0, 0], [0, 0, 1], [0, -1, 0]]),
            'prewitt_x': np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]]),
            'prewitt_y': np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]]),
            'sobel_x': np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]),
            'sobel_y': np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]]),
            'laplace1': np.array([[0, -1, 0], [-1, 4, -1], [0, -1, 0]]),
            'laplace2': np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]]),
            'laplace3': np.array([[1, -2, 1], [-2, 4, -2], [1, -2, 1]])
        }

        kernel = kernels.get(filter_type)
        if kernel is None:
            return self.image

        filtered = self._apply_convolution(img_array, kernel)
        return Image.fromarray(filtered)

    def _apply_convolution(self, img_array, kernel):
        height, width = img_array.shape
        pad_h, pad_w = kernel.shape[0] // 2, kernel.shape[1] // 2
        padded = np.pad(img_array, ((pad_h, pad_h), (pad_w, pad_w)), mode='constant')
        output = np.zeros_like(img_array)

        for y in range(height):
            for x in range(width):
                region = padded[y:y + kernel.shape[0], x:x + kernel.shape[1]]
                output[y, x] = np.sum(region * kernel)

        return np.clip(output, 0, 255).astype(np.uint8)

    def statistical_filter(self, filter_type='median', size=3):
        if filter_type == 'min':
            return self.image.filter(ImageFilter.MinFilter(size))
        elif filter_type == 'max':
            return self.image.filter(ImageFilter.MaxFilter(size))
        elif filter_type == 'median':
            return self.image.filter(ImageFilter.MedianFilter(size))
        else:
            return self.image

    def save_image(self, image, output_path):
        image.save(output_path)

if __name__ == "__main__":
    processor = ImageProcessor("kredens.jpg")
    processor.save_image(processor.linear_transform(brightness=20), "bright.jpg")
    processor.save_image(processor.gamma_transform(gamma=1.5), "gamma.jpg")
    processor.save_image(processor.blend_images("regał.jpg", mode='multiply', alpha=0.7), "blended.jpg")
    processor.generate_histogram()
    processor.save_image(processor.equalize_histogram(), "equalized.jpg")
    processor.save_image(processor.high_pass_filter(filter_type='sobel_x'), "sobel_x.jpg")
    processor.save_image(processor.statistical_filter(filter_type='median', size=5), "median.jpg")
