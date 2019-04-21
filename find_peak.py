import numpy as np
import os
from astropy.io import fits
import matplotlib.pyplot as plt

def find_peak(mapdata,mask=[]):
     
    """
        Produces find the local peak of a map. e.g. Ha
        
        :param mapdata:  flux map [Nx,Ny]
        :param mask:  mask file[Nx,Ny]
        :Only the pixel without mask will be calculated
        :output dens: flux density in sorted order
        :out pdis: distance to the nearest flux pixels
        :out idx: image x coordinate
        :out idy: image y coordinate
    """
        
    xdim,ydim=mapdata.shape
    # if no mask, create a mask        
    if len(mask) == 0:
        mask=np.zeros((xdim,ydim),dtype=int)

    sel=np.where(mask == 0)
    mapsel=mapdata[sel]
    Nsel=mapsel.size
    ind=mapsel.argsort()
    
    #density parameter
    dens=mapsel[ind]   
    idx=sel[0][ind]
    idy=sel[1][ind]
        
    # distance parameter
    pdis=np.ndarray(Nsel)
    for i in range(Nsel-1):
        tdis=((idx[i]-idx[i+1:Nsel])**2+(idy[i]-idy[i+1:Nsel])**2)**0.5
        pdis[i]=tdis.min()
        
        # the global maximum point
        tdis=((idx[Nsel-1]-idx)**2+(idy[Nsel-1]-idy)**2)**0.5
        pdis[Nsel-1]=tdis.max()
    return dens,pdis,idx,idy

class Ha_map():
    
    def __init__(self,mapdata,mask=[]):
        xdim,ydim=mapdata.shape
        # if no mask, create a mask        
        if len(mask) == 0:
            mask=np.zeros((xdim,ydim),dtype=int)
        self.mapdata=mapdata
        self.mask=mask


    def find_peak(self):
        
        dens,pdis,idx,idy=find_peak(self.mapdata,mask=self.mask)
        self.dens=dens
        self.pdis=pdis
        self.idx=idx
        self.idy=idy
