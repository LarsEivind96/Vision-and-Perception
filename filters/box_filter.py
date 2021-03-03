from PIL import Image


def create_padding(image, padding_size):
    width, height = image.size
    color = 0 if image.mode == "L" else (0, 0, 0)
    # Create black background, larger than original image
    out_image = Image.new(image.mode, (width + padding_size * 2, height + padding_size * 2), color)
    # Paste the original image upon the black background to create padding
    out_image.paste(image, (padding_size, padding_size))
    return out_image


# Super optimized version with optional kernel size
# This algorithm exploits that the box filter is a separable filter.
# Instead of discarding the sum, the algorithm reuses the previous sum and updates it by subtracting away the old pixel and adding the new pixel in the blurring range
def box_filter(image, kernel_size):
    image = image.copy()
    kernel_len = kernel_size // 2
    padded_image = create_padding(image, kernel_len)

    # Filter image in horizontal direction
    for y in range(kernel_len, padded_image.height - kernel_len):
        pix_sum = 0
        for x in range(kernel_len, padded_image.width - kernel_len):
            if x == kernel_len:
                for x1 in range(x-kernel_len, x+1+kernel_len):
                    pix_sum += padded_image.getpixel((x1, y))
            else:
                pix_sum -= padded_image.getpixel((x-1-kernel_len, y))
                pix_sum += padded_image.getpixel((x+kernel_len, y))
            image.putpixel((x - kernel_len, y - kernel_len), int(pix_sum / kernel_size))

    # Filter image in vertical direction
    padded_image = create_padding(image, kernel_len)
    for x in range(kernel_len, padded_image.width - kernel_len):
        pix_sum = 0
        for y in range(kernel_len, padded_image.height - kernel_len):
            if y == kernel_len:
                for y1 in range(y-kernel_len, y+1+kernel_len):
                    pix_sum += padded_image.getpixel((x, y1))
            else:
                pix_sum -= padded_image.getpixel((x, y-1-kernel_len))
                pix_sum += padded_image.getpixel((x, y+kernel_len))
            image.putpixel((x - kernel_len, y - kernel_len), int(pix_sum / kernel_size))
    return image


# Creates a contour of an image by subtracting the blurred image from the original image.
def contour_optimized(original_image, blurred_image):
    out_image = original_image.copy()
    for y in range(0, out_image.height):
        for x in range(0, out_image.width):
            new_pixel_value = original_image.getpixel((x, y)) - blurred_image.getpixel((x, y))
            out_image.putpixel((x, y), new_pixel_value)
    return out_image


# Sharpens an image by subtracting the blurred image from 2 times the original image.
def sharpen_optimized(original_image, blurred_image):
    out_image = original_image.copy()
    for y in range(0, out_image.height):
        for x in range(0, out_image.width):
            new_pixel_value = 2 * original_image.getpixel((x, y)) - blurred_image.getpixel((x, y))
            out_image.putpixel((x, y), new_pixel_value)
    return out_image




def pixel_value_gray(square):
    tot_sum = 0
    length = len(square)
    for i in range(length):
        for j in range(length):
            tot_sum += square[i][j]
    return tot_sum // length ** 2


# Not optimized at all
def box_filter_unoptimized(image):
    out_image = image.copy()
    for x in range(2, out_image.width - 1):
        for y in range(2, out_image.height - 1):
            square = []
            for x1 in range(x-1, x+2):
                square_row = []
                for y1 in range(y-1, y+2):
                    square_row.append(image.getpixel((x1, y1)))
                square.append(square_row)
            pix = pixel_value_gray(square)
            out_image.putpixel((x, y), pix)
    return out_image


# Minor optimized version
def box_filter_minor_optimization(image):
    out_image = image.copy()
    # Row summation
    for y in range(2, out_image.height - 1):
        for x in range(2, out_image.width - 1):
            pix_sum = 0
            for x1 in range(x-1, x+2):
                pix_sum += image.getpixel((x1, y))
            out_image.putpixel((x, y), int(pix_sum / 3))

    # Column summation
    for x in range(2, out_image.width - 1):
        for y in range(2, out_image.height - 1):
            pix_sum = 0
            for y1 in range(y - 1, y + 2):
                pix_sum += out_image.getpixel((x, y1))
            out_image.putpixel((x, y), int(pix_sum / 3))
    return out_image


if __name__ == '__main__':
    # This works for both rgb images and grayscale images!
    im_path = "C:/Users/larse/Documents/Skole/VisionPerception38/assets/"
    im = Image.open(im_path + "einstein.jpg")
    if not im.mode == "L":
        im = im.convert("L")

    blurred_image = box_filter(im, 5)
    blurred_image.show()
    contour_image = contour_optimized(im, blurred_image)
    contour_image.show()
    sharpen_image = sharpen_optimized(im, blurred_image)
    sharpen_image.show()
