# -*- coding: utf-8 -*-
"""
  on Thu Aug 12 11:17:10 2021
This is the script for generating DMD mask patterns for a given HTSI observation.
Input parameters include: 
    S or H matrix type
    Matrix order
    center point of matrix on DMD
    slit width (in terms of mircomirrors)

Output: A set of DMD patterns saved as images for the observation. 
image filenames 'H64_2w_mask_#.PNG' 'S79_3w_mask_#.PNG'
@author: Kate
"""
import sys
import imageio
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from scipy.linalg import hadamard
sys.path.append('C:/Users/Kate/Documents/hadamard/sandbox')
from hadamard_class_v3 import *
HTSI = HTSI_Models()

#%% Generate the DMD patterns from the matrix

# For an S-matrix
def make_S_matrix_masks(order, DMD_size, slit_width, Xo, Yo, folder):
    matrix = HTSI.S_matrix(order) # Generate the S-matrix

    DMD_mask = np.zeros((DMD_size)) # Create an array to represent the DMD mask. Use Zeros as those translate to off mirrors
    mask_set = np.zeros((DMD_size[0],DMD_size[1],order))
    for i in range (0,order):
        row = matrix[i,:]
        row_expanded = np.repeat(row, slit_width)
        mask_size = order*slit_width

        # insert that mask into the DMD mask array
        x1,x2 = Xo-(mask_size/2), Xo+(mask_size/2)
        y1,y2 = np.int(Yo-(mask_size/2)),np.int(Yo+(mask_size/2))
        for j in range (y1, y2):    
            DMD_mask[j, np.int(x1):np.int(x2)]= row_expanded
        mask_set[:,:,i]= DMD_mask 
        mask = DMD_mask.astype(np.uint8)
        name = 'S'+str(order)+'_'+str(slit_width)+'w_mask_'+str(i+1)+'.bmp'
        imageio.imwrite(folder+name, mask)
        
    return mask_set, matrix


# Code for a set of H-matrix DMD masks (pairs of masks)  
def make_H_matrix_masks(order, DMD_size, slit_width, Xo, Yo, folder):
    matrix = hadamard(order, dtype='float64') # generate the H-matrix 

    mask_set_a = np.zeros((DMD_size[0],DMD_size[1],order))
    mask_set_b = np.zeros((DMD_size[0],DMD_size[1],order))
    DMD_mask_a = np.zeros((DMD_size)) # Create an array to represent the DMD mask. Use Zeros as those translate to off mirrors
    DMD_mask_b = np.zeros((DMD_size)) # Create an array to represent the DMD mask. Use Zeros as those translate to off mirrors
    matrix_type = 'H'
    ##For an H-matrix
    
    for i in range (0,order):
        row = matrix[i,:]
        row_expanded = np.repeat(row, slit_width) # Adjusts the elements to account for slit widths
        mask_size = order*slit_width
    
        # Convert the -1s and +1s into pairs of masks with 1s and 0s
        row_a = np.copy(row_expanded) # 1 means on -1 means off
        row_b = np.copy(row_expanded) # 1 means off, -1 means on
        for j in range (0, len(row_expanded)):
            if row_expanded[j] < 0:
                row_a[j] = 0
                row_b[j] = 1 
            else:
                row_b[j] = 0 
                row_a[j] = 1 
    
        x1,x2 = Xo-(mask_size/2), Xo+(mask_size/2) # Coordinates for the mask center
        y1,y2 = np.int(Yo-(mask_size/2)),np.int(Yo+(mask_size/2)) # Coordinates for the mask center
    
        for j in range (y1, y2):    # Insert the matrices into the DMD mask array
            DMD_mask_a[j, np.int(x1):np.int(x2)]= row_a
            DMD_mask_b[j, np.int(x1):np.int(x2)]= row_b

        mask_set_a[:,:,i]= DMD_mask_a
        mask_set_b[:,:,i]= DMD_mask_b 

        mask_a = DMD_mask_a.astype(np.uint8)
        mask_b = DMD_mask_b.astype(np.uint8)

        name_a = str(matrix_type)+str(order)+'_'+str(slit_width)+'w_mask_a'+str(i+1)+'.bmp'
        name_b = str(matrix_type)+str(order)+'_'+str(slit_width)+'w_mask_b'+str(i+1)+'.bmp'

        imageio.imwrite(folder+name_a, mask_a)
        imageio.imwrite(folder+name_b, mask_b)
        
        return mask_set_a, mask_set_b, matrix

#%%   List of possible S-matrix orders: 3,7,11,15,19,23,31,35,43,47,63,71,79,83,103,127,255

DMD_size = (768, 1024) #(1024,2048) #(768, 1024) # XGA or DC2K DMD array size
matrix_type = 'S' # Two options, H or S
order = 83 # Order of the hadamard matrix (or S matrix)
Xo, Yo = DMD_size[1]/2, DMD_size[0]/2   # Coordinates on the DMD to center the Hadamard matrix around

slit_width = 4 # Slit width in number of micromirrors 
folder = 'C:/Users/Kate/Documents/hadamard/mask_sets/' # Change path to fit user needs

if matrix_type == 'S':
    mask_set, matrix = make_S_matrix_masks(order, DMD_size, slit_width, Xo, Yo, folder)
if matrix_type == 'H':
    mask_set_a,mask_set_b, matrix = make_H_matrix_masks(order, DMD_size, slit_width, Xo, Yo, folder)

plt.imshow(matrix, cmap='gray')
plt.axis('off')
plt.title(str(matrix_type)+'-matrix, n= '+str(order))    


#%% Open a file and check that the code worked
name = 'H128_3w_mask_a1.bmp'
im =np.asarray(Image.open(folder+name), dtype='float64')
plt.imshow(im, cmap='gray')


#%% Pseudo code for SAMOS
'''    
    Input paramaters: 
        - drive location for the desired DMD mask images
        - exposure time (for spectral CCD)
        - filter selection
        - grism selection
    
    For all dmd mask images in specified drive location:
        1. Open dmd mask image and send/load to DMD
        2. Capture spectral camera image with specified exposure time. 
            - Additional header info for images will include:
                a. mask type (a string 'H' or 'S')
                b. mask order (an integer)
                c. mask label (a string e.g '112b')
            This info can be taken right from the DMD mask file image name
        3. Capture imaging camera image for specified exposyre time (? might not be necessary)
        
    
    
    
    
'''