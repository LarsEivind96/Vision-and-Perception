from PIL import Image
import numpy as np
import time
import box_filter


def dnorm(x, mu, sd):
    return 1 / (np.sqrt(2 * np.pi) * sd) * np.e ** (-np.power((x-mu) / sd, 2) / 2)


def gaussian_kernel_1D(size, sigma=1, verbose=False):
    kernel_1D = np.linspace(-(size // 2), size // 2, size)
    for i in range(size):
        kernel_1D[i] = dnorm(kernel_1D[i], 0, sigma)
    kernel_1D *= 1.0 / kernel_1D.max()
    return kernel_1D


def create_padding(image, kernel_len):
    image_row, image_col = image.size
    pad_height = int((kernel_len - 1) / 2)
    pad_width = int((kernel_len - 1) / 2)
    # padded_image[pad_height:padded_image.shape[0] - pad_height, pad_width:padded_image.shape[1] - pad_width] = image
    color = 0 if image.mode == "L" else (0, 0, 0)
    # Create black background, larger than original image
    padded_image = Image.new(image.mode, (image_row + 2 * pad_height, image_col + 2 * pad_width), color)
    # Paste the original image upon the black background to create padding
    padded_image.paste(image, (pad_height, pad_width))
    return padded_image


# Gaussian optimized by performing blur in horizontal and vertical direction seperately.
def convolution_optimized(image, kernel, average=False, verbose=True):
    kernel_length = len(kernel) // 2
    kernel_sum = np.sum(kernel)
    print(kernel_sum)
    output = image.copy()

    # Create padding
    padded_image = create_padding(image, len(kernel))

    # Filter image in horizontal direction
    for y in range(kernel_length, padded_image.height - kernel_length):
        for x in range(kernel_length, padded_image.width - kernel_length):
            pixel_sum = 0
            for x1 in range(x - kernel_length, x + 1 + kernel_length):
                pixel_sum += kernel[x1 - x + kernel_length] * padded_image.getpixel((x1, y))
            output.putpixel((x - kernel_length, y - kernel_length), int(pixel_sum / kernel_sum))

    # Filter image in vertical direction
    padded_image = create_padding(output, len(kernel))
    for x in range(kernel_length, padded_image.width - kernel_length):
        for y in range(kernel_length, padded_image.height - kernel_length):
            pixel_sum = 0
            for y1 in range(y - kernel_length, y + 1 + kernel_length):
                pixel_sum += kernel[y1 - y + kernel_length] * padded_image.getpixel((x, y1))
            output.putpixel((x - kernel_length, y - kernel_length), int(pixel_sum / kernel_sum))
    return output


if __name__ == '__main__':
    im_path = "C:/Users/larse/Documents/Skole/VisionPerception38/assets/"
    im = Image.open(im_path + "einstein.jpg")
    # Convert to grayscale image
    if not im.mode == "L":
        im = im.convert("L")

    gaussian_1D = gaussian_kernel_1D(5, sigma=np.sqrt(5), verbose=True)
    print("1 dimensional gaussian: {}".format(gaussian_1D))

    start = time.time()
    image = convolution_optimized(im, gaussian_1D, average=False, verbose=True)
    end = time.time()
    print("Execution time optimized gaussian: {}".format(end - start))
    image.show()

    sharpened_image = box_filter.sharpen_optimized(im, image)
    sharpened_image.show()
