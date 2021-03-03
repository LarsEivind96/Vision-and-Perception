# Vision-and-Perception

This repository contains code for manipulating images. It is inspired by the course Vision and Perception at La Sapienza, Rome. 

## Box Blur
The box blur is the easiest blurring algorithm, where each pixel in the resulting image has a value equal to the average value of its surrounding pixels in the input image.

My algorithm is optimized in a number of ways, compared to the basic box blur algorithm:
1. It is possible to choose kernel size. A large kernel leads to a very blurred image, and a small kernel leads to an image quite similar to the original image.
2. The box blur is a separable filter. The complexity is lowered from O(Nr^2) to O(Nr) by performing two 1D passes of the separable filter, one horizontal and one vertical. 
3. Instead of discarding the sum for each pixel, the algorithm re-uses the previous sum and updates it by subtracting away the old pixel and adding the new pixel in the blurring range. This lowers the complexity from O(Nr) to O(N)

## Gaussian Blur
The Gaussian blur is a blurring algorithm used as a preprocessing stage in computer vision algorithms in order to enhance image structures at different scales. It differs from the box blur algorithm in the way that the pixels close to the current pixel are weighted greater than the pixels far from the current pixel. It is common to use the gaussian blur algorithm with edge detection. 

## Edge detection (Contour)
My edge detection algortithm is as simple as it gets. It takes the original image and the blurred image (box blur / gaussian blur etc.), and outputs the difference between these two images. The result is an image only consisting of edges! On pixel level, the algorithm is as follows: ***P(x, y) = OP(x, y) - BP(x, y)***, where P is the resulting pixel value, OP is the original pixel value and BP is the blurred pixel value. 

## Sharpening
My sharpening algorithm is as simple as the edge detection algorithm. Basically it takes the original image and adds the edge-detected image. On pixel level, the algorithm is as follows: ***P(x, y) = 2 * OP(x, y) - BP(x, y)***, where P is the resulting pixel value, OP is the original pixel value and BP is the blurred pixel value. 
