# from matplotlib import path
# import matplotlib.pyplot as plt
# import numpy as np
#
# first = -3
# size = (3-first)/100
#
# xv,yv = np.meshgrid(np.linspace(-3,3,100),
# 						  np.linspace(-3,3,100))
#
# p = path.Path([(0,0), (0, 1), (1, 1), (1, 0)])  # square with legs length 1 and bottom left corner at the origin
#
# flags = p.contains_points(np.hstack((xv.flatten()[:,np.newaxis],yv.flatten()[:,np.newaxis])))
#
# grid = np.zeros((101,101),dtype='bool')
# grid[((xv.flatten()-first)/size).astype('int'),((yv.flatten()-first)/size).astype('int')] = flags
#
# xi,yi = np.random.randint(-300,300,100)/100,np.random.randint(-300,300,100)/100
# vflag = grid[((xi-first)/size).astype('int'),((yi-first)/size).astype('int')]
#
# plt.imshow(grid.T,origin='lower',interpolation='nearest',cmap='binary')
# plt.scatter(((xi-first)/size).astype('int'),((yi-first)/size).astype('int'),c=vflag,cmap='Greens',s=90)
# plt.show()

from matplotlib import path
import numpy as np

terretorialWaters_Lat_Long_Malaysia = [
	[6.9, 99.3],
	[6.9, 102.7],
	[5.5, 103.91],
	[0.99, 105.28],
	[0.99, 99.3]
]

latLongSamples = [
	[1, 88],
	[2, 99],
	[3, 100],
	[4, 102],
	[5, 105]
]

print(str(terretorialWaters_Lat_Long_Malaysia[1][0]))

# p = path.Path([(6.9,99.3), (6.9, 102.7), (5.5, 103.91), (1.24, 105.28), (1.24, 99.3)])  # square with legs length 1 and bottom left corner at the origin
# flags = p.contains_points([(6.2, 100)])

p = path.Path(np.array(terretorialWaters_Lat_Long_Malaysia))
flags = p.contains_points(np.array(latLongSamples))

print(flags)
# array([ True], dtype=bool)