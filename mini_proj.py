import numpy as np
import cv2
import sys
import math

def check_if_gray(src):
    if src.any() != None:
        if(len(src.shape)<=2):
            return (True)
        elif len(src.shape)>=3:
            b, g, r = src[:, :, 0], src[:, :, 1], src[:, :, 2] # For RGB image
            if np.array_equal(b, g) and np.array_equal(g, r):
                return (True)
            else:
                return (False)


def distance(x, y, i, j):
    return np.sqrt((x-i)**2 + (y-j)**2)


def gaussian(x, sigma):
    return (1.0 / (2 * math.pi * (sigma ** 2))) * math.exp(- (x ** 2) / (2 * sigma ** 2))


def apply_bilateral_filter(source, filtered_image, x, y, diameter, sigma_i, sigma_s):
    hl = int((diameter-1)/2)
    i_filtered = 0
    Wp = 0
    i = 0
    while i < diameter:
        j = 0
        while j < diameter:
            neighbour_x = int(x - (hl - i))
            neighbour_y = int(y - (hl - j))
            #len= num of rows 
            if neighbour_x >= len(source):
                neighbour_x = len(source)-1
            if neighbour_x < 0:
                neighbour_x=0
            #len of index 0 is the num of colons 
            if neighbour_y >= len(source[0]):
                neighbour_y = len(source[0])-1
            if neighbour_y < 0:
                neighbour_y= 0
            gi = gaussian(int(source[neighbour_x][neighbour_y]) - int(source[x][y]), sigma_i)
            gs = gaussian(distance(neighbour_x, neighbour_y, x, y), sigma_s)
            w = gi * gs
            i_filtered += source[neighbour_x][neighbour_y] * w
            Wp += w
            j += 1
        i += 1
    i_filtered = i_filtered / Wp
    filtered_image[x][y] = int(round(i_filtered))


def bilateral_filter(source, filter_diameter, sigma_i, sigma_s):
    filtered_image = np.zeros(source.shape)

    i = 0
    while i < len(source):
        j = 0
        while j < len(source[0]):
            apply_bilateral_filter(source, filtered_image, i, j, filter_diameter, sigma_i, sigma_s)
            j += 1
        i += 1
    return filtered_image


if __name__ == "__main__":
    src = cv2.imread(str(sys.argv[1]), -1)
    cv2.imwrite("original_image.png", src)
    #sigma_i=24.0 sigma_s=8.0
    is_grayscale =check_if_gray(src) 
    if is_grayscale==True:
        filtered_image = bilateral_filter(src, int(sys.argv[2]), int(sys.argv[3]) , int(sys.argv[4]))
    else:
        b, g, r = src[:, :, 0], src[:, :, 1], src[:, :, 2] # For RGB image
        filtered_image_b = bilateral_filter(b, int(sys.argv[2]), int(sys.argv[3]) , int(sys.argv[4]))
        filtered_image_g = bilateral_filter(g, int(sys.argv[2]), int(sys.argv[3]) , int(sys.argv[4]))
        filtered_image_r = bilateral_filter(r, int(sys.argv[2]), int(sys.argv[3]) , int(sys.argv[4]))
        filtered_image = cv2.merge((filtered_image_b, filtered_image_g,filtered_image_r))
    cv2.imwrite("filtered_image.png", filtered_image)






