import numpy as np
import os
from astropy.io import fits
import matplotlib.pyplot as plt
from find_peak import find_peak
from astropy.table import Table

gals=fits.open('Spiral_MPL8_face.fits')
params=gals[1].data
Plate,IFUDESIGN=params['Plate'],params['IFUDESIGN']

filelist1=open('HaEW1.list','w')
filelist2=open('HaEW2.list','w')


Ngal=len(Plate)
Isel=np.zeros(Ngal,dtype='int')

for i,PID in enumerate(Plate):

    mapfile='Ha_EW_maps/Ha_EW_'+str(PID)+'-'+str(IFUDESIGN[i])+'.fits'
  
    if not os.path.isfile(mapfile):
        print('map file does not exist',mapfile)
        continue

    #print(i,'th mapfile','read',mapfile)
    Isel[i]=1

    #Hdus=fits.open(mapfile)
    #Hamaps=Hdus[1].data
    #HaEW1=Hamaps[0,:,:]
    #mask1=Hamaps[2,:,:]
    #HaEW2=Hamaps[3,:,:]
    #mask2=Hamaps[5,:,:]

    #dens1,pdis1,idx1,idy1=find_peak(HaEW1,mask1)
    #Tab1=Table((dens1,pdis1,idx1,idy1),names=('dens','pdis','idx','idy'))
    #print('flux peaks identified on',len(dens1),'non-par Ha flux pixels') 
    
    #dens2,pdis2,idx2,idy2=find_peak(HaEW1,mask1)
    #Tab2=Table((dens2,pdis2,idx2,idy2),names=('dens','pdis','idx','idy'))
    #print('flux peaks identified on',len(dens1),'Gaussian Ha flux pixels')
    filelist1.write('Ha_EW_maps/'+str(PID)+'-'+str(IFUDESIGN[i])+'1.fits\n')
    filelist2.write('Ha_EW_maps/'+str(PID)+'-'+str(IFUDESIGN[i])+'2.fits\n')


    #Tab1.write('Ha_EW_maps/'+str(PID)+'-'+str(IFUDESIGN[i])+'1.fits',format='fits')
    #Tab2.write('Ha_EW_maps/'+str(PID)+'-'+str(IFUDESIGN[i])+'2.fits',format='fits')

filelist1.close()
filelist2.close()

sel=np.where(Isel ==1)
par=params[sel]
hdu2=fits.BinTableHDU(par)
#hdu2.writeto('HII_gal_pars.fits')
