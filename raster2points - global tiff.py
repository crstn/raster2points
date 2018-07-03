# coding: utf-8
import numpy as np
import time

from PIL import Image
Image.MAX_IMAGE_PIXELS = None # Disable warnings for pillow DecompressionBombError

import matplotlib as mpl
import matplotlib.pyplot as plt

# Reading the GeoTIFF as a plain image, not caring about the georeference for now; then convert to numpy array
im = Image.open('popsub.tif')
raster = np.array(im)
print(raster.shape)

# Let's take a subset of the 2D array to keep things manageable
# In[97]:
#raster = raster[0:300,0:300]
#raster.shape


# Plot with matplotlib

# plt.imshow(raster)

numpoints = np.sum(raster)
points = np.zeros((numpoints,2), dtype=int)
print(points)

# Using numpy's [nditer](https://docs.scipy.org/doc/numpy-1.13.0/reference/arrays.nditer.html#tracking-an-index-or-multi-index) and [append](https://docs.scipy.org/doc/numpy/reference/generated/numpy.append.html) - see also the [Minimal Example notebook](Minimal%20Example.ipynb).

# make an empty 2D "target array"
points = np.zeros((numpoints,2), dtype=int)

# keep track of where in the target array we have to insert
insertrow = 0

# iterate over the input raster
it = np.nditer(raster, flags=['multi_index'])
while not it.finished:
    entry = np.array([np.array(it.multi_index)])
    block = np.repeat(entry, it[0], axis=0)
    points[insertrow:insertrow+block.shape[0]] = block
    insertrow = insertrow + block.shape[0]
    it.iternext()


print(points)
print(points.size)


# Next, we will randomly move each point around within its cell. We can also choose to keep the "edges" between the cells (set expansion to < 1.0) or allow the points to go outside the cells, which "softenes" the edges, giving the impression of a more smooth surface (set expansion to > 1.0)

expansion = 1.5

seed = np.random.rand(numpoints,2)
seed = seed * expansion

plot = points + seed


plt.scatter(plot[:,0], plot[:,1], s=0.01, alpha=0.5)
#plt.show()

# not working in the notebook...
plt.savefig("dots"+str(time.time())+".png", dpi=900)
