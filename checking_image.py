import numpy as np
import cv2
import sys

def check_if_gray(src):
    if src.any() != None:
        if(len(src.shape)<=2):
            print ('grayscale')
        elif len(src.shape)>=3:
            b, g, r = src[:, :, 0], src[:, :, 1], src[:, :, 2] # For RGB image
            if np.array_equal(b, g) and np.array_equal(g, r):
                print ('grayscale')
            else:
                print ('Colored')

if __name__ == "__main__":
    src = cv2.imread(str(sys.argv[1]), -1) #unchanged
    check_if_gray(src)
    cv2.imwrite("original_test.png", src) 
    b_channel, g_channel, r_channel = src[:, :, 0], src[:, :, 1], src[:, :, 2] # For RGB image
    merged= cv2.merge((b_channel,g_channel,r_channel))
    cv2.imwrite("merged_test.png", merged)
    #check if merge works: 
    # jpeg - c: V  g:V
    #png- c: V   g: V
