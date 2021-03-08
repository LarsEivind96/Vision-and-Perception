from PIL import Image
import numpy as np
import gaussian_filter
import box_filter


# Remove even rows and columns. Results in an image 1/4 the size of the original image.
def subsample(image):
    # Converts the image to a numpy array for easier manipulation.
    im_array = np.array(image)
    image_row, image_col = im_array.shape

    # Deletes every other column
    for x in range(image_col - 1, -1, -1):
        if x % 2 == 0:
            im_array = np.delete(im_array, x, 1)

    # Deletes every other row
    for y in range(image_row - 1, -1, -1):
        if y % 2 == 0:
            im_array = np.delete(im_array, y, 0)

    # Converts the image array back to an image
    image = Image.fromarray(im_array)
    return image


def up_scale(image):
    # Converts the image to a numpy array for easier manipulation.
    im_array = np.array(image)
    image_row, image_col = im_array.shape

    for x in range(image_col - 1, -1, -1):
        image_row, image_col = im_array.shape
        if x == 0:
            new_col = im_array[:, x]
        else:
            new_col = (im_array[:, x-1] + im_array[:, x]) / 2
        im_array = np.c_[im_array[:, 0:x], new_col, im_array[:, x:image_col]]

    for y in range(image_row - 1, -1, -1):
        image_row, image_col = im_array.shape
        if y == 0:
            new_row = im_array[y:y+1, :]
        else:
            new_row = (im_array[y-1:y, :] + im_array[y:y+1, :]) / 2
        first_part = im_array[0:y, :]
        last_part = im_array[y:image_row, :]
        im_array = np.r_[first_part, new_row, last_part]

    # Converts the image array back to an image
    image = Image.fromarray(im_array)
    return image


# Not functioning properly
def up_scale_bi_linear(image):
    # Converts the image to a numpy array for easier manipulation.
    im_array = np.array(image)
    image_row, image_col = im_array.shape

    # For each column, add another one.
    for x in range(image_col - 1, -1, -1):
        image_row, image_col = im_array.shape

        if x == 0:
            new_col = im_array[:, x]
        else:
            new_col = np.zeros(image_row)
            left_col = im_array[:, x-1]
            right_col = im_array[:, x]
            new_col[0] = (left_col[0] + right_col[0]) / 2
            for i in range(1, len(new_col) - 1):
                new_col[i] = (int(left_col[i-1]) + 2*int(left_col[i]) + int(left_col[i+1]) + int(right_col[i-1]) + 2*int(right_col[i]) + int(right_col[i+1])) / 8
            new_col[-1] = (left_col[-1] + right_col[-1]) / 2

        im_array = np.c_[im_array[:, 0:x], new_col, im_array[:, x:image_col]]

    for y in range(image_row - 1, -1, -1):
        image_row, image_col = im_array.shape
        if y == 0:
            new_row = im_array[y:y+1, :]
        else:
            new_row = im_array[y-1:y, :]
            left_row = im_array[y-1:y, :]
            right_row = im_array[y:y+1, :]
            new_row[0] = (left_row[0] + right_row[0]) / 2
            for i in range(1, len(new_row) - 1):
                new_row[i] = (int(left_row[i - 1]) + 2*int(left_row[i]) + int(left_row[i + 1]) + int(right_row[i - 1]) + int(
                    right_row[i + 1]) + 2*right_row[i]) / 8
            new_row[-1] = (left_row[-1] + right_row[-1]) / 2

        first_part = im_array[0:y, :]
        last_part = im_array[y:image_row, :]
        im_array = np.r_[first_part, new_row, last_part]

    # Converts the image array back to an image
    image = Image.fromarray(im_array)
    return image


def create_pyramid(image):
    rows, cols = image.size
    array_of_images = [image]
    while rows > 8 and cols > 8:
        blurred_image = gaussian_filter.gaussian_filter(image, kernel_size=5)
        image = subsample(blurred_image)
        rows, cols = image.size
        array_of_images.append(image)
    for image in array_of_images:
        image.show()
    return array_of_images


def create_laplacian_pyramid(image):
    rows, cols = image.size
    array_of_images = []
    while rows > 8 and cols > 8:
        blurred_image = gaussian_filter.gaussian_filter(image, kernel_size=5)
        edge_image = box_filter.contour_optimized(image, blurred_image)
        image = subsample(blurred_image)
        array_of_images.append(edge_image)
        rows, cols = image.size
    array_of_images.append(image)
    return array_of_images


def inverse_laplace(image_list):
    nr_of_images = len(image_list)

    image = image_list[nr_of_images - 1]
    for i in range(nr_of_images - 2, -1, -1):
        up_scaled_image = up_scale(image)
        up_scaled_image_array = np.array(up_scaled_image)
        edge_im_array = np.array(image_list[i])
        row_edge, col_edge = edge_im_array.shape
        row_im, col_im = up_scaled_image_array.shape

        if row_im < row_edge:
            up_scaled_image_array = np.r_[up_scaled_image_array[0:1, :], up_scaled_image_array]
        if col_im < col_edge:
            up_scaled_image_array = np.c_[up_scaled_image_array[:, 0:1], up_scaled_image_array]

        new_image_array = edge_im_array + up_scaled_image_array
        image = Image.fromarray(new_image_array)
    image.show()
    return image


def upscale_x_times(image, x):
    for i in range(x):
        image = up_scale(image)
    return image


if __name__ == '__main__':
    im_path = "C:/Users/larse/Documents/Skole/VisionPerception38/assets/"
    im = Image.open(im_path + "einstein.jpg")
    # Convert to grayscale image
    if not im.mode == "L":
        im = im.convert("L")
    im.show()

    # compressed_images = create_pyramid(im)
    compressed_lpl_images = create_laplacian_pyramid(im)
    inverse_laplace(compressed_lpl_images)
    """image = up_scale(im)
    image.show()
    image = up_scale_bi_linear(im)
    image.show()"""
    # upscale_image = upscale_x_times(compressed_lpl_images[len(compressed_lpl_images) - 1], 4)
    # upscale_image.show()
