from PIL import Image
import numpy as np


def dnorm(x, mu, sd):
    return 1 / (np.sqrt(2 * np.pi) * sd) * np.e ** (-np.power((x-mu) / sd, 2) / 2)


def gaussian_kernel(size, sigma=1, verbose=False):
    kernel_1D = np.linspace(-(size // 2), size // 2, size)
    for i in range(size):
        kernel_1D[i] = dnorm(kernel_1D[i], 0, sigma)
    print(kernel_1D)
    kernel_2D = np.outer(kernel_1D.T, kernel_1D.T)
    print(kernel_2D)
    kernel_2D *= 1.0 / kernel_2D.max()
    print(kernel_2D)
    return kernel_2D


def gaussian_kernel_1D(size, sigma=1, verbose=False):
    kernel_1D = np.linspace(-(size // 2), size // 2, size)
    for i in range(size):
        kernel_1D[i] = dnorm(kernel_1D[i], 0, sigma)
    kernel_1D *= 1.0 / kernel_1D.max()
    print(kernel_1D)
    kernel_2D = np.outer(kernel_1D.T, kernel_1D.T)
    print(kernel_2D)
    return kernel_1D


def convolution(image, kernel, average=False, verbose=True):
    print("Image Shape : {}".format(image.size))
    print("Kernel Shape : {}".format(kernel.shape))
    image_row, image_col = image.size
    kernel_row, kernel_col = kernel.shape
    kernel_sum = np.sum(kernel)
    output = image.copy()

    # Create padding
    pad_height = int((kernel_row - 1) / 2)
    pad_width = int((kernel_col - 1) / 2)
    # padded_image[pad_height:padded_image.shape[0] - pad_height, pad_width:padded_image.shape[1] - pad_width] = image
    color = 0 if image.mode == "L" else (0, 0, 0)
    # Create black background, larger than original image
    padded_image = Image.new(image.mode, (image_row + 2 * pad_height, image_col + 2 * pad_width), color)
    # Paste the original image upon the black background to create padding
    padded_image.paste(image, (pad_height, pad_width))
    print("Padded Image Shape : {}".format(padded_image.size))

    for row in range(image_row):
        for col in range(image_col):
            pixel_sum = calculate_pixel_color(padded_image, row, col, kernel)
            output.putpixel((row, col), int(pixel_sum / kernel_sum))
    print("Output Image size : {}".format(output.size))
    return output


def calculate_pixel_color(padded_image, row, col, kernel):
    pixel_sum = 0
    kernel_row, kernel_col = kernel.shape
    for k_row in range(kernel_row):
        for k_col in range(kernel_col):
            pixel_sum += kernel[k_row, k_col] * padded_image.getpixel((row + k_row, col + k_col))
    #pixel_sum /= (kernel_col * kernel_row)
    return pixel_sum


if __name__ == '__main__':
    im_path = "C:/Users/larse/Documents/Skole/VisionPerception38/assets/"
    #im = Image.open(im_path + "einstein.jpg")
    #im.show()
    kernel_gaussian = gaussian_kernel(5, sigma=np.sqrt(5), verbose=True)
    gaussian_1D = gaussian_kernel_1D(5, sigma=np.sqrt(5), verbose=True)
    #im = convolution(im, kernel_gaussian, average=False, verbose=False)
    #im.show()
