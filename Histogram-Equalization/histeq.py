from IPython.display import display, Math

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
img = Image.open('face1.bmp')
plt.imshow(img, cmap='gray')
img = np.asarray(img)
# put pixels in a 1D array by flattening out img array
flat = img.flatten()

i = Math(r'P_x(j) = \sum_{i=0}^{j} P_x(i)')
# formula for creating the histogram
display(i)


# create our own histogram function
def get_histogram(image, bins):
    # array with size of bins, set to zeros
    histogram = np.zeros(bins)

    # loop through pixels and sum up counts of pixels
    for pixel in image:
        histogram[pixel] += 1

    # return our final result
    return histogram


hist = get_histogram(flat, 256)

plt.plot(hist)
# create our cumulative sum function
def cumsum(a):
    a = iter(a)
    b = [next(a)]
    for i in a:
        b.append(b[-1] + i)
    return np.array(b)
# execute the fn
cs = cumsum(hist)

# display the result
plt.plot(cs)
# formula to calculate cumulation sum
j = Math(r's_k = \sum_{j=0}^{k} {\frac{n_j}{N}}')
display(j)
# re-normalize cumsum values to be between 0-255

# numerator & denomenator
nj = (cs - cs.min()) * 255
N = cs.max() - cs.min()

# re-normalize the cdf
cs = nj / N

plt.plot(cs)
# cast it back to uint8 since we can't use floating point values in images
cs = cs.astype('uint8')

plt.plot(cs)
# get the value from cumulative sum for every index in flat, and set that as img_new
img_new = cs[flat]

# we see a much more evenly distributed histogram
plt.hist(img_new, bins=50)
# put array back into original shape since we flattened it
img_new = np.reshape(img_new, img.shape)
# set up side-by-side image display
fig = plt.figure()
fig.set_figheight(15)
fig.set_figwidth(15)

fig.add_subplot(1,2,1)
plt.imshow(img, cmap='gray')

# display the new image
fig.add_subplot(1,2,2)
plt.imshow(img_new, cmap='gray')

plt.show(block=True)
top = tk.Tk()
B = tk.Button(top, text ="Histogram Equalization", command = get_histogram(flat,256))
C = tk.Button(top, text ="Local Adaptive Histogram Equalization", command = Localadaptive(flat,256))

B.pack()
C.pack()
top.mainloop()
