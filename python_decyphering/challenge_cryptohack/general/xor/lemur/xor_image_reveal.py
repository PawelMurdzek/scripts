import os
from PIL import Image
import numpy as np

# Set your image filenames here
image1_path = 'flag.png'
image2_path = 'lemur.png'
output_path = 'xor_revealed.png'

def xor_images(img1_path, img2_path, output_path):
    # Load images
    img1 = Image.open(img1_path).convert('RGB')
    img2 = Image.open(img2_path).convert('RGB')
    
    # Ensure images are the same size
    if img1.size != img2.size:
        raise ValueError('Images must be the same size!')
    
    arr1 = np.array(img1)
    arr2 = np.array(img2)
    
    # XOR the RGB values
    xor_arr = np.bitwise_xor(arr1, arr2)
    xor_img = Image.fromarray(xor_arr.astype('uint8'), 'RGB')
    xor_img.save(output_path)
    print(f'Revealed image saved to: {output_path}')

if __name__ == '__main__':
    # Place image1.png and image2.png in this folder before running
    xor_images(image1_path, image2_path, output_path)
