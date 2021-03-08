# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
#import tensorflow as tf
from PIL import Image
from filters import box_filter
from filters import gaussian_filter
# mnist = tf.keras.datasets.mnist


def run_box_filter(image):
    image.show()
    padded_im = box_filter.create_padding(image)
    new_im = box_filter.box_filter(padded_im)
    new_im.show()
    new_im = box_filter.contour(padded_im)
    new_im.show()
    new_im = box_filter.sharpen(padded_im)
    new_im.show()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    im = Image.open("assets/GoldenRetriever.jpg.crdownload")
    run_box_filter(im)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
