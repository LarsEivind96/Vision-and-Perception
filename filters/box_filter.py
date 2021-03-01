from PIL import Image
import time


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


def create_padding(image, padding_size):
    width, height = image.size
    color = 0 if image.mode == "L" else (0, 0, 0)
    # Create black background, larger than original image
    out_image = Image.new(image.mode, (width + padding_size * 2, height + padding_size * 2), color)
    # Paste the original image upon the black background to create padding
    out_image.paste(image, (padding_size, padding_size))
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


# Optimized version
def box_filter_optimized(image):
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


# Super optimized version with optional kernel size
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


# Optimized version
def contour_optimized(original_image, blurred_image):
    out_image = original_image.copy()
    for y in range(0, out_image.height):
        for x in range(0, out_image.width):
            new_pixel_value = original_image.getpixel((x, y)) - blurred_image.getpixel((x, y))
            out_image.putpixel((x, y), new_pixel_value)
    return out_image


# Optimized version
def sharpen_optimized(original_image, blurred_image):
    out_image = original_image.copy()
    for y in range(0, out_image.height):
        for x in range(0, out_image.width):
            new_pixel_value = 2 * original_image.getpixel((x, y)) - blurred_image.getpixel((x, y))
            out_image.putpixel((x, y), new_pixel_value)
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


if __name__ == '__main__':
    # This works for both rgb images and grayscale images!
    im_path = "C:/Users/larse/Documents/Skole/VisionPerception38/assets/"
    im = Image.open(im_path + "GoldenRetriever.jpg.crdownload")
    #im = Image.open(im_path + "golden_retriever_full_hd.jpg")
    im = im.convert("L")

    padded_im = create_padding(im, 1)
    start = time.time()
    new_im = contour(padded_im)
    end = time.time()
    print("Execution time contour: {}".format(end - start))
    new_im.show()

    start = time.time()
    new_im = box_filter(im, 7)
    contour_image = contour_optimized(im, new_im)
    end = time.time()
    print("Execution time optimized contour: {}".format(end - start))
    contour_image.show()

    sharpen_image = sharpen_optimized(im, new_im)
    sharpen_image.show()
