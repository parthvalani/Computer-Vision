import cv2
import numpy as np
from matplotlib import pyplot as plt

import imageio
import image_slicer
from image_slicer import join
from PIL import Image

img = 'face4.bmp'
num_tiles = 25
tiles = image_slicer.slice(img, num_tiles)


for tile in tiles:
    img = imageio.imread(tile.filename)
    hist,bins = np.histogram(img.flatten(),256,[0,256])
    cdf = hist.cumsum()
    cdf_normalized = cdf *hist.max()/ cdf.max()
    plt.plot(cdf_normalized, color = 'g')
    plt.hist(img.flatten(),256,[0,256], color = 'g')
    plt.xlim([0,256])
    plt.legend(('cdf','histogram'), loc = 'upper left')
    cdf_m = np.ma.masked_equal(cdf,0)
    cdf_o = (cdf_m - cdf_m.min())*255/(cdf_m.max()-cdf_m.min())
    cdf = np.ma.filled(cdf_o,0).astype('uint8')
    img3 = cdf[img]
    cv2.imwrite(tile.filename,img3)
    tile.image = Image.open(tile.filename)
image = join(tiles)     
                                        image.save('face8.bmp')
