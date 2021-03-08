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
    for x in range(image_col - 1, -1, -2):
        im_array = np.delete(im_array, x, 1)

    # Deletes every other row
    for y in range(image_row - 1, -1, -2):
        im_array = np.delete(im_array, y, 0)

    print(im_array.shape)
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
        rows, cols = image.size
        if rows > 8 and cols > 8:
            array_of_images.append(edge_image)
        else:
            array_of_images.append(image)
    for image in array_of_images:
        image.show()
    return array_of_images


if __name__ == '__main__':
    im_path = "C:/Users/larse/Documents/Skole/VisionPerception38/assets/"
    im = Image.open(im_path + "einstein.jpg")
    # Convert to grayscale image
    if not im.mode == "L":
        im = im.convert("L")

    #im.show()
    #subsample_im = subsample(im)
    #subsample_im.show()

    compressed_images = create_pyramid(im)
    # compressed_lpl_images = create_laplacian_pyramid(im)
    # compressed_im.show()
