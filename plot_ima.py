
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits

import matplotlib as mpl
mpl.rcParams['lines.linewidth']=3
mpl.rcParams['lines.color']='black'
mpl.rcParams['axes.linewidth']=3
mpl.rcParams['font.size']=20
mpl.rcParams['font.serif'] = "Times New Roman"
mpl.rcParams['legend.framealpha']=1
mpl.rcParams['xtick.major.width']=3
mpl.rcParams['ytick.major.width']=3
#mpl.rcParams['mathtext.default']='bf'
mpl.rcParams['legend.numpoints']=1

%matplotlib inline

alist=fits.open('./astrotask/Ha_EW8439-12704.fits')
a=alist[0].data

xdim,ydim=np.shape(a)
x=np.arange(xdim)
y=np.arange(ydim)
xx,yy=np.meshgrid(x,y)

a_sort=np.sort(a,axis=None)
ind=np.where(a>a_sort[-5])

plt.imshow(a,origin='lower',cmap='jet')
plt.scatter(xx[ind],yy[ind],s=40,color='white',alpha=0.5)
plt.show()
