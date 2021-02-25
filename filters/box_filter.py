from PIL import Image
import os


def loop_through_pixels(image):
    for x in range(image.width):
        for y in range(image.height):
            print(image.getpixel((x, y)))


def black_white_converter(image, threshold):
    # Converts image to greyscale
    out_image = image.convert("L")
    for x in range(out_image.width):
        for y in range(out_image.height):
            if out_image.getpixel((x, y)) < threshold:
                out_image.putpixel((x, y), 0)
            else:
                out_image.putpixel((x, y), 255)
    return out_image


def create_padding(image):
    width, height = image.size
    color = 0 if image.mode == "L" else (0, 0, 0)
    # Create black background, larger than original image
    out_image = Image.new(image.mode, (width + 2, height + 2), color)
    # Paste the original image upon the black background to create padding
    out_image.paste(image, (1, 1))
    return out_image


def calculate_pixel_value(square):
    r = 0
    g = 0
    b = 0
    for i in range(len(square)):
        for j in range(len(square)):
            r += square[i][j][0]
            g += square[i][j][1]
            b += square[i][j][2]
    r = r // len(square) ** 2
    g = g // len(square) ** 2
    b = b // len(square) ** 2
    pixel = (r, g, b)
    return pixel


def pixel_value_gray(square):
    tot_sum = 0
    length = len(square)
    for i in range(length):
        for j in range(length):
            tot_sum += square[i][j]
    return tot_sum // length ** 2


def box_filter(image):
    out_image = image.copy()
    for x in range(2, out_image.width - 1):
        for y in range(2, out_image.height - 1):
            square = []
            for x1 in range(x-1, x+2):
                square_row = []
                for y1 in range(y-1, y+2):
                    square_row.append(image.getpixel((x1, y1)))
                square.append(square_row)
            pix = pixel_value_gray(square) if image.mode == "L" else calculate_pixel_value(square)
            out_image.putpixel((x, y), pix)
    return out_image


def contour(image):
    out_image = image.copy()

    for x in range(2, out_image.width - 1):
        for y in range(2, out_image.height - 1):
            square = []
            for x1 in range(x-1, x+2):
                square_row = []
                for y1 in range(y-1, y+2):
                    square_row.append(image.getpixel((x1, y1)))
                square.append(square_row)
            if image.mode == "L":
                pix = pixel_value_gray(square)
                new_tuple = image.getpixel((x, y)) - pix
            else:
                pix = calculate_pixel_value(square)
                new_tuple = (image.getpixel((x, y))[0] - pix[0], image.getpixel((x, y))[1] - pix[1],
                             image.getpixel((x, y))[2] - pix[2])
            out_image.putpixel((x, y), new_tuple)
    return out_image


def sharpen(image):
    out_image = image.copy()
    for x in range(2, out_image.width - 1):
        for y in range(2, out_image.height - 1):
            square = []
            for x1 in range(x-1, x+2):
                square_row = []
                for y1 in range(y-1, y+2):
                    square_row.append(image.getpixel((x1, y1)))
                square.append(square_row)
            if image.mode == "L":
                pix = pixel_value_gray(square)
                new_tuple = 2 * image.getpixel((x, y)) - pix
            else:
                pix = calculate_pixel_value(square)
                new_tuple = (2*image.getpixel((x, y))[0] - pix[0], 2*image.getpixel((x, y))[1] - pix[1], 2*image.getpixel((x, y))[2] - pix[2])
            out_image.putpixel((x, y), new_tuple)
    return out_image


def box_filter2(image):
    kernel_size = 3
    kernel_len = kernel_size // 2
    out_image = image.copy()
    for x in range(kernel_len + 1, out_image.width - kernel_len):
        for y in range(kernel_len + 1, out_image.height - kernel_len):
            square = []
            for x1 in range(x-kernel_len, x+1+kernel_len):
                square_row = []
                for y1 in range(y-kernel_len, y+1+kernel_len):
                    square_row.append(image.getpixel((x1, y1)))
                square.append(square_row)
            pix = pixel_value_gray(square) if image.mode == "L" else calculate_pixel_value(square)
            out_image.putpixel((x, y), pix)
    return out_image


if __name__ == '__main__':
    # This works for both rgb images and grayscale images!
    im_path = "C:/Users/larse/Documents/Skole/VisionPerception38/assets/"
    im = Image.open(im_path + "GoldenRetriever.jpg.crdownload")
    im1 = Image.open(im_path + "einstein.jpg")
    im.show()

    # loop_through_pixels(im)
    # new_im = black_white_converter(im, 120)
    padded_im = create_padding(im)
    new_im = box_filter2(padded_im)
    new_im.show()
    new_im = contour(padded_im)
    new_im.show()
    new_im = sharpen(padded_im)
    new_im.show()
