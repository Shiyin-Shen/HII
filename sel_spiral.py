import numpy as np
import os
from astropy.io import fits
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
from matplotlib.path import Path
from matplotlib.patches import PathPatch
from astropy.table import Table

hdu=fits.open('dapall-v2_5_3-2.3.0.fits')

dapall=hdu[1].data
MANGAID=dapall['MANGAID']
Plate=dapall['PLATE']
Ra=dapall['OBJRA']
Dec=dapall['OBJDEC']
Ser_N=dapall['NSA_SERSIC_N']
btoa=dapall['NSA_SERSIC_BA']
Phi=dapall['NSA_SERSIC_PHI']
redshift=dapall['NSA_Z']
IFUDESIGN=dapall['IFUDESIGN']
R50=dapall['NSA_SERSIC_TH50']
dtype=dapall['DAPTYPE']

#select non-face/edge on spirals with 127 fibers
sel=np.where((Ser_N < 2) & (btoa > 0.3) & (IFUDESIGN > 12700) & \
             (dtype == 'HYB10-MILESHC-MILESHC') )
Nsel=len(sel[0])
print(Nsel,'spiral galaxies selected')


#output basic parameters into a table
Tab=Table((Plate[sel],IFUDESIGN[sel],MANGAID[sel],Ra[sel],Dec[sel],Ser_N[sel],btoa[sel],Phi[sel],\
        redshift[sel],R50[sel]),names=('Plate','IFUDESIGN','MaNGAID','Ra','Dec','Ser_N','btoa',\
        'Phi','redshift','SR50'))
Tab.write('Spiral_MPL8_face.fits',format='fits')

#output HII EW data from DAP maps
dapdir='/DATA_MANGA/newton/DAP/MPL-8/HYB10-MILESHC-MILESHC/'
outdir='Ha_EW_maps/'

hdr = fits.Header()
hdr['Comment1'] = 'Ha EW Maps from MaNGA DAP, EW1,EW1_var,EW1_mask'
hdr['Comment2'] = 'Ha EW Maps from MaNGA DAP, EW2,EW2_var,EW2_mask'
primary_hdu=fits.PrimaryHDU(header=hdr)

j=0
for i in range(Nsel):

    Isel=sel[0][i]
    mapfilename='manga-'+str(Plate[Isel])+'-'+str(IFUDESIGN[Isel])+'-MAPS-HYB10-MILESHC-MILESHC.fits.gz'
    mapfile=dapdir+str(Plate[Isel])+'/'+str(IFUDESIGN[Isel])+'/'+mapfilename

    if not os.path.isfile(mapfile):
        print('DAP file does not exist',mapfile)
        continue
    
    maps=fits.open(mapfile)
    Ha_EW1=maps[26].data[18,:,:]
    Ha_EW1_var=maps[27].data[18,:,:]
    mask1=maps[28].data[18,:,:]

    Ha_EW2=maps[32].data[18,:,:]
    Ha_EW2_var=maps[33].data[18,:,:]
    mask2=maps[34].data[18,:,:]
    hdu=fits.ImageHDU([Ha_EW1,Ha_EW1_var,mask1,Ha_EW2,Ha_EW2_var,mask2],name='Ha_EW')
    hdu1=fits.HDUList([primary_hdu, hdu])
    outname=outdir+'Ha_EW_'+str(Plate[Isel])+'-'+str(IFUDESIGN[Isel])+'.fits'
    print(outname)
    hdu1.writeto(outname)
    j=j+1
      
print(j,'galaxies velocity maps read')
