#!/usr/bin/ python
import numpy as np
import os
from astropy.io import fits
import matplotlib.pyplot as plt

def peak_loc(filelist,ipeak=1):
    '''
    get the flux peak location for a list of peak files
    '''
    
    Nfile=len(filelist)
    print(Nfile,'peakfile')
    xdis=np.zeros(Nfile)
    ydis=np.zeros(Nfile)
    ppdis=np.zeros(Nfile)
    pdens=np.zeros(Nfile)
    
    for i in range(Nfile):
        fname=filelist[i]
        HDU=fits.open(fname)
        Tab=HDU[1].data
        dens,pdis,idx,idy=Tab['dens'],Tab['pdis'],Tab['idx'],Tab['idy']
    
        Pind=pdis.argsort()
        pid=0-ipeak
        xdis[i]=idx[pid]
        ydis[i]=idy[pid]
        ppdis[i]=pdis[pid]
        pdens[i]=dens[pid]

    return xdis,ydis,ppdis,pdens

def rand_loc(filelist,Nrand=1):

    '''
    Take the random pixels for a group of Ha images
    '''
    Nfile=len(filelist)
    print(Nfile,'peakfile')
    xdis=np.zeros((Nrand,Nfile))
    ydis=np.zeros((Nrand,Nfile))
    ppdis=np.zeros((Nrand,Nfile))
    pdens=np.zeros((Nrand,Nfile))
    
    for i in range(Nfile):
        fname=filelist[i]
        HDU=fits.open(fname)
        Tab=HDU[1].data
        dens,pdis,idx,idy=Tab['dens'],Tab['pdis'],Tab['idx'],Tab['idy']
    
        Npix=len(dens)
        Irand=np.random.randint(0,Npix,Nrand)
        xdis[:,i]=idx[Irand]
        ydis[:,i]=idy[Irand]
        ppdis[:,i]=pdis[Irand]
        pdens[:,i]=dens[Irand]

    return xdis,ydis,ppdis,pdens


if __name__ == '__main__':
    
    filelist=np.loadtxt('HaEW1.list',dtype='str')

    hdu=fits.open('HII_gal_pars.fits')
    pars=hdu[1].data
    R50=pars['SR50']
    
    pxdis,pydis,ppdis,pdens=peak_loc(filelist)
    rxdis,rydis,rpdis,rdens=rand_loc(filelist,Nrand=20)
    
    # Ha peak radius in arcsec
    prad=((pxdis-37)**2+(pydis-37)**2)**0.5*0.5
    # Ha peak radius in R50
    prad2=prad/R50

    # random pixel rad in arcsec
    rrad=((rxdis-37)**2+(rydis-37)**2)**0.5*0.5
    rrad2=rrad/R50

    
    rhist=np.histogram(rrad.reshape(-1),bins=range(18))
    phist=np.histogram(prad,bins=range(18))
    prob=phist[0]/rhist[0]*20
    perror=(phist[0]*(phist[0]+rhist[0])/rhist[0]**3)**0.5*20
    
    plt.figure(1)
    plt.clf()
    plt.plot(np.arange(17)+0.5,prob,'o')
    plt.errorbar(np.arange(17)+0.5,prob,yerr=perror)

    rhist2=np.histogram(rrad2.reshape(-1),bins=np.arange(20)*0.2)
    phist2=np.histogram(prad2,bins=np.arange(20)*0.2)
    prob2=phist2[0]/rhist2[0]*20
    perror2=(phist2[0]*(phist2[0]+rhist2[0])/rhist2[0]**3)**0.5*20

   
    plt.figure(2)
    plt.clf()
    plt.plot(np.arange(19)*0.2+0.1,prob2,'o')
    plt.errorbar(np.arange(19)*0.2+0.1,prob2,yerr=perror2)
    plt.show() 
